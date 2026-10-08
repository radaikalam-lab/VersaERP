from graphmodel.domain.models import (
    AssertionStatus,
    Conflict,
    ConflictStatus,
    ConflictType,
    Evidence,
    GraphLayer,
    Node,
    Provenance,
    Relationship,
    SemanticAssertion,
    generate_canonical_id,
    generate_provenance_id,
)
from graphmodel.graph.store import Graph
from graphmodel.semantics.models import (
    MappingType,
    SemanticAttribute,
    SemanticEntity,
    SemanticGraphResult,
    SemanticMapping,
    SemanticRelationship,
)
from graphmodel.semantics.rules import SemanticMappingRules


class SemanticGraphConstructor:
    """Constructs a canonical Semantic Graph from an observed Physical Graph.
    
    Adheres strictly to the Epistemic Non-Authority boundary:
    Physical observation -> Conservative rule-based derivation -> Semantic graph & mappings.
    Maintains full traceability, evidence grounding, deterministic identity, and conflict preservation.
    """

    def __init__(
        self,
        rules: SemanticMappingRules | None = None,
        source_id: str = "semantic_engine_01",
    ) -> None:
        self.rules = rules or SemanticMappingRules()
        self.source_id = source_id

    def construct(
        self,
        physical_graph: Graph,
        evidence_sources: list[Evidence] | None = None,
    ) -> SemanticGraphResult:
        """Construct a validated semantic graph and associated mappings from a physical graph."""
        evidence_map = {e.source_id: e for e in (evidence_sources or [])}

        provenance = Provenance(
            id=generate_provenance_id("semantic_graph_construction", self.source_id),
            source_ids=(self.source_id,),
            method="deterministic_physical_to_semantic_mapping",
            confidence=0.90,
            assumptions=(
                "Table structures represent candidate domain entity concepts",
                "Foreign keys represent candidate entity associations",
            ),
        )

        semantic_graph = Graph(layer=GraphLayer.SEMANTIC)
        entities: list[Node] = []
        attributes: list[Node] = []
        relationships: list[Relationship] = []
        mappings: list[SemanticMapping] = []
        assertions: list[SemanticAssertion] = []
        conflicts: list[Conflict] = []
        evidence_out: list[Evidence] = []

        # 1. Identify primary key columns per table
        table_pk_columns: dict[str, set[str]] = {}
        for node in physical_graph.nodes.values():
            if node.type == "constraint" and node.properties.get("constraint_type") == "PRIMARY KEY":
                tname = node.properties.get("table")
                cols = set(node.properties.get("columns", []))
                if tname:
                    table_pk_columns[tname] = cols

        # 2. Extract and map tables to Semantic Entities
        table_nodes = sorted(
            [n for n in physical_graph.nodes.values() if n.type == "table"],
            key=lambda n: n.id,
        )

        # Track concept name to physical table mapping for conflict detection
        concept_to_tables: dict[str, list[Node]] = {}

        for tnode in table_nodes:
            raw_tname = tnode.properties.get("name", tnode.id)
            concept_name = self.rules.to_pascal_case(raw_tname)
            concept_to_tables.setdefault(concept_name, []).append(tnode)

        # Conflict Detection: Multiple tables mapping to same candidate concept name
        for concept_name, mapped_tnodes in concept_to_tables.items():
            if len(mapped_tnodes) > 1:
                conflict_id = generate_canonical_id(
                    "conflict", "semantic", self.source_id, concept_name, *[t.id for t in mapped_tnodes]
                )
                conflicts.append(
                    Conflict(
                        id=conflict_id,
                        conflict_type=ConflictType.SEMANTIC_CONFLICT,
                        status=ConflictStatus.DETECTED,
                        assertion_ids=tuple(
                            generate_canonical_id(GraphLayer.SEMANTIC, "assertion", "entity", t.id)
                            for t in mapped_tnodes
                        ),
                        source_ids=tuple(t.id for t in mapped_tnodes),
                        detection_method="duplicate_semantic_concept_mapping",
                        description=f"Multiple physical tables {sorted(t.id for t in mapped_tnodes)} map to same semantic concept '{concept_name}'",
                    )
                )

        # Map each table to entity
        table_id_to_entity: dict[str, SemanticEntity] = {}

        for tnode in table_nodes:
            raw_tname = tnode.properties.get("name", tnode.id)
            schema_name = tnode.properties.get("schema", "public")
            database_name = tnode.properties.get("database", "postgres")
            concept_name = self.rules.to_pascal_case(raw_tname)

            # If there's a collision on concept name from different schemas/tables, qualify concept
            if len(concept_to_tables[concept_name]) > 1:
                entity_canonical_id = generate_canonical_id(
                    GraphLayer.SEMANTIC, "entity", database_name, schema_name, concept_name
                )
            else:
                entity_canonical_id = generate_canonical_id(GraphLayer.SEMANTIC, "entity", concept_name)

            # Collect columns for this table
            col_edges = sorted(
                [
                    r
                    for r in physical_graph.relationships.values()
                    if r.source == tnode.id and r.type == "HAS_COLUMN"
                ],
                key=lambda r: (r.properties.get("ordinal_position", 0), r.target),
            )

            attribute_ids: list[str] = []
            entity_attributes: list[SemanticAttribute] = []
            pk_cols = table_pk_columns.get(raw_tname, set())

            for cedge in col_edges:
                cnode = physical_graph.get_node(cedge.target)
                if not cnode:
                    continue
                raw_col_name = cnode.properties.get("name", cnode.id)
                attr_name = self.rules.to_attribute_name(raw_col_name)
                is_pk = raw_col_name in pk_cols or cnode.properties.get("is_identity", False)

                attr_canonical_id = generate_canonical_id(
                    GraphLayer.SEMANTIC, "attribute", entity_canonical_id, attr_name
                )
                attribute_ids.append(attr_canonical_id)

                sem_attr = SemanticAttribute(
                    id=attr_canonical_id,
                    name=attr_name,
                    entity_id=entity_canonical_id,
                    data_type=cnode.properties.get("data_type", "unknown"),
                    is_identifier=is_pk,
                    nullable=cnode.properties.get("nullable", True),
                    physical_column_id=cnode.id,
                    status=AssertionStatus.DERIVED,
                    provenance=provenance,
                    properties={
                        "character_length": cnode.properties.get("character_length"),
                        "default_expression": cnode.properties.get("default_expression"),
                        "native_data_type": cnode.properties.get("native_data_type"),
                        "numeric_precision": cnode.properties.get("numeric_precision"),
                        "numeric_scale": cnode.properties.get("numeric_scale"),
                        "ordinal_position": cnode.properties.get("ordinal_position"),
                    },
                )
                entity_attributes.append(sem_attr)

                # Column mapping record
                col_mapping_id = generate_canonical_id(
                    GraphLayer.SEMANTIC, "mapping", "column_to_attribute", cnode.id, attr_canonical_id
                )
                c_evidence = evidence_map.get(cnode.id)
                mappings.append(
                    SemanticMapping(
                        id=col_mapping_id,
                        physical_id=cnode.id,
                        semantic_id=attr_canonical_id,
                        mapping_type=MappingType.COLUMN_TO_ATTRIBUTE,
                        status=AssertionStatus.DERIVED,
                        evidence_ids=(c_evidence.id,) if c_evidence else (),
                        provenance=provenance,
                        confidence=0.95,
                        properties={"column_name": raw_col_name, "attribute_name": attr_name},
                    )
                )

                # Attribute assertion
                attr_assertion_id = generate_canonical_id(
                    GraphLayer.SEMANTIC, "assertion", "attribute", cnode.id
                )
                assertions.append(
                    SemanticAssertion(
                        id=attr_assertion_id,
                        candidate_concept=attr_name,
                        target_id=attr_canonical_id,
                        layer=GraphLayer.SEMANTIC,
                        evidence=(c_evidence,) if c_evidence else (),
                        provenance=provenance,
                        method="column_to_attribute_normalization",
                        confidence=0.95,
                        status=AssertionStatus.DERIVED,
                        properties={"physical_column": cnode.id, "entity_id": entity_canonical_id},
                    )
                )

            sem_entity = SemanticEntity(
                id=entity_canonical_id,
                name=concept_name,
                status=AssertionStatus.DERIVED,
                layer=GraphLayer.SEMANTIC,
                physical_table_id=tnode.id,
                attributes=tuple(attribute_ids),
                provenance=provenance,
                properties={
                    "comment": tnode.properties.get("comment"),
                    "physical_table": raw_tname,
                    "schema": schema_name,
                },
            )
            table_id_to_entity[tnode.id] = sem_entity

            # Add entity node and attribute nodes to graph
            e_node = sem_entity.to_node()
            entities.append(e_node)
            semantic_graph.add_node(e_node)

            for a in entity_attributes:
                a_node = a.to_node()
                attributes.append(a_node)
                semantic_graph.add_node(a_node)
                # Add containment edge
                rel_attr_id = generate_canonical_id(
                    GraphLayer.SEMANTIC, "rel", "has_attribute", e_node.id, a_node.id
                )
                semantic_graph.add_relationship(
                    Relationship(
                        id=rel_attr_id,
                        source=e_node.id,
                        type="HAS_ATTRIBUTE",
                        target=a_node.id,
                        layer=GraphLayer.SEMANTIC,
                        properties={"is_identifier": a.is_identifier},
                        status=AssertionStatus.DERIVED,
                        provenance=provenance,
                    )
                )

            # Table mapping record
            t_evidence = evidence_map.get(tnode.id)
            if t_evidence:
                evidence_out.append(t_evidence)

            tbl_mapping_id = generate_canonical_id(
                GraphLayer.SEMANTIC, "mapping", "table_to_entity", tnode.id, entity_canonical_id
            )
            mappings.append(
                SemanticMapping(
                    id=tbl_mapping_id,
                    physical_id=tnode.id,
                    semantic_id=entity_canonical_id,
                    mapping_type=MappingType.TABLE_TO_ENTITY,
                    status=AssertionStatus.DERIVED,
                    evidence_ids=(t_evidence.id,) if t_evidence else (),
                    provenance=provenance,
                    confidence=0.90,
                    properties={"table_name": raw_tname, "concept_name": concept_name},
                )
            )

            # Entity assertion
            entity_assertion_id = generate_canonical_id(
                GraphLayer.SEMANTIC, "assertion", "entity", tnode.id
            )
            assertions.append(
                SemanticAssertion(
                    id=entity_assertion_id,
                    candidate_concept=concept_name,
                    target_id=entity_canonical_id,
                    layer=GraphLayer.SEMANTIC,
                    evidence=(t_evidence,) if t_evidence else (),
                    provenance=provenance,
                    method="table_to_entity_heuristic",
                    confidence=0.90,
                    status=AssertionStatus.DERIVED,
                    properties={"physical_table": tnode.id},
                )
            )

        # 3. Extract and map views to Semantic Entities
        view_nodes = sorted(
            [n for n in physical_graph.nodes.values() if n.type == "view"],
            key=lambda n: n.id,
        )
        for vnode in view_nodes:
            raw_vname = vnode.properties.get("name", vnode.id)
            concept_name = self.rules.to_pascal_case(raw_vname)
            view_entity_id = generate_canonical_id(GraphLayer.SEMANTIC, "entity", concept_name)

            v_entity = SemanticEntity(
                id=view_entity_id,
                name=concept_name,
                status=AssertionStatus.DERIVED,
                layer=GraphLayer.SEMANTIC,
                physical_table_id=vnode.id,
                attributes=(),
                provenance=provenance,
                properties={"definition": vnode.properties.get("definition"), "is_view_derived": True},
            )
            v_node = v_entity.to_node()
            entities.append(v_node)
            if v_node.id not in semantic_graph.nodes:
                semantic_graph.add_node(v_node)

            v_evidence = evidence_map.get(vnode.id)
            v_mapping_id = generate_canonical_id(
                GraphLayer.SEMANTIC, "mapping", "view_to_entity", vnode.id, view_entity_id
            )
            mappings.append(
                SemanticMapping(
                    id=v_mapping_id,
                    physical_id=vnode.id,
                    semantic_id=view_entity_id,
                    mapping_type=MappingType.VIEW_TO_ENTITY,
                    status=AssertionStatus.DERIVED,
                    evidence_ids=(v_evidence.id,) if v_evidence else (),
                    provenance=provenance,
                    confidence=0.85,
                    properties={"view_name": raw_vname, "concept_name": concept_name},
                )
            )

        # 4. Map Foreign Key REFERENCES relationships to Semantic Relationships
        fk_relationships = sorted(
            [r for r in physical_graph.relationships.values() if r.type == "REFERENCES"],
            key=lambda r: (r.id, r.source, r.target),
        )

        for fk_rel in fk_relationships:
            # fk_rel.source is constraint node, fk_rel.target is target table node
            constraint_node = physical_graph.get_node(fk_rel.source)
            if not constraint_node:
                continue

            src_table_name = constraint_node.properties.get("table")
            tgt_table_node = physical_graph.get_node(fk_rel.target)
            if not tgt_table_node:
                continue

            # Find source table node
            src_table_node = next(
                (
                    n
                    for n in table_nodes
                    if n.properties.get("name") == src_table_name
                    and n.properties.get("schema") == constraint_node.properties.get("schema")
                ),
                None,
            )
            if not src_table_node:
                continue

            src_entity = table_id_to_entity.get(src_table_node.id)
            tgt_entity = table_id_to_entity.get(tgt_table_node.id)

            if not src_entity or not tgt_entity:
                continue

            rel_type = self.rules.infer_relationship_type(
                source_table=src_table_name,
                target_table=tgt_table_node.properties.get("name", ""),
                fk_columns=tuple(constraint_node.properties.get("columns", ())),
                target_columns=tuple(constraint_node.properties.get("foreign_columns", ())),
                fk_properties=fk_rel.properties,
            )

            sem_rel_id = generate_canonical_id(
                GraphLayer.SEMANTIC, "relationship", rel_type, src_entity.id, tgt_entity.id
            )

            sem_rel = SemanticRelationship(
                id=sem_rel_id,
                source_entity_id=src_entity.id,
                type=rel_type,
                target_entity_id=tgt_entity.id,
                physical_constraint_id=constraint_node.id,
                cardinality="MANY_TO_ONE",
                status=AssertionStatus.DERIVED,
                layer=GraphLayer.SEMANTIC,
                provenance=provenance,
                properties={
                    "column_pairs": fk_rel.properties.get("column_pairs", []),
                    "foreign_columns": fk_rel.properties.get("foreign_columns", []),
                    "on_delete": fk_rel.properties.get("on_delete"),
                    "on_update": fk_rel.properties.get("on_update"),
                    "source_columns": fk_rel.properties.get("source_columns", []),
                },
            )
            rel_edge = sem_rel.to_relationship()
            relationships.append(rel_edge)
            semantic_graph.add_relationship(rel_edge)

            # Mapping record for foreign key
            fk_evidence = evidence_map.get(constraint_node.id)
            fk_mapping_id = generate_canonical_id(
                GraphLayer.SEMANTIC, "mapping", "fk_to_relationship", constraint_node.id, sem_rel_id
            )
            mappings.append(
                SemanticMapping(
                    id=fk_mapping_id,
                    physical_id=constraint_node.id,
                    semantic_id=sem_rel_id,
                    mapping_type=MappingType.FK_TO_RELATIONSHIP,
                    status=AssertionStatus.DERIVED,
                    evidence_ids=(fk_evidence.id,) if fk_evidence else (),
                    provenance=provenance,
                    confidence=0.90,
                    properties={
                        "constraint_name": constraint_node.properties.get("name"),
                        "relationship_type": rel_type,
                        "source_entity": src_entity.name,
                        "target_entity": tgt_entity.name,
                    },
                )
            )

            # Assertion for semantic relationship
            rel_assertion_id = generate_canonical_id(
                GraphLayer.SEMANTIC, "assertion", "relationship", constraint_node.id
            )
            assertions.append(
                SemanticAssertion(
                    id=rel_assertion_id,
                    candidate_concept=rel_type,
                    target_id=sem_rel_id,
                    layer=GraphLayer.SEMANTIC,
                    evidence=(fk_evidence,) if fk_evidence else (),
                    provenance=provenance,
                    method="fk_to_relationship_heuristic",
                    confidence=0.90,
                    status=AssertionStatus.DERIVED,
                    properties={
                        "physical_constraint": constraint_node.id,
                        "source_entity_id": src_entity.id,
                        "target_entity_id": tgt_entity.id,
                    },
                )
            )

        # Sort all result elements deterministically
        sorted_entities = sorted(entities, key=lambda n: n.id)
        sorted_attributes = sorted(attributes, key=lambda n: n.id)
        sorted_relationships = sorted(relationships, key=lambda r: (r.id, r.source, r.type, r.target))
        sorted_mappings = sorted(mappings, key=lambda m: m.id)
        sorted_assertions = sorted(assertions, key=lambda a: a.id)
        sorted_conflicts = sorted(conflicts, key=lambda c: c.id)
        sorted_evidence = sorted(evidence_out, key=lambda e: e.id)

        diagnostics = {
            "attributes_count": len(sorted_attributes),
            "conflicts_count": len(sorted_conflicts),
            "entities_count": len(sorted_entities),
            "evidence_count": len(sorted_evidence),
            "mappings_count": len(sorted_mappings),
            "relationships_count": len(sorted_relationships),
            "semantic_assertions_count": len(sorted_assertions),
        }

        return SemanticGraphResult(
            graph=semantic_graph,
            entities=sorted_entities,
            attributes=sorted_attributes,
            relationships=sorted_relationships,
            mappings=sorted_mappings,
            assertions=sorted_assertions,
            conflicts=sorted_conflicts,
            evidence=sorted_evidence,
            provenance=provenance,
            diagnostics=diagnostics,
        )
