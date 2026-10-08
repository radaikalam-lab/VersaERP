
from graphmodel.domain.models import AssertionStatus, GraphLayer, Node, Relationship
from graphmodel.domain.requirements import (
    Actor,
    BusinessRule,
    Capability,
    Constraint,
    Event,
    Process,
    Requirement,
    RequirementRelationship,
)
from graphmodel.graph.store import Graph


class RequirementsGraphBuilder:
    """Constructs canonical Graph representations from Requirements and Functional Design models."""

    def __init__(self) -> None:
        self.requirements: list[Requirement] = []
        self.actors: list[Actor] = []
        self.rules: list[BusinessRule] = []
        self.processes: list[Process] = []
        self.events: list[Event] = []
        self.constraints: list[Constraint] = []
        self.capabilities: list[Capability] = []
        self.relationships: list[RequirementRelationship] = []

    def add_requirement(self, req: Requirement) -> "RequirementsGraphBuilder":
        self.requirements.append(req)
        return self

    def add_actor(self, actor: Actor) -> "RequirementsGraphBuilder":
        self.actors.append(actor)
        return self

    def add_rule(self, rule: BusinessRule) -> "RequirementsGraphBuilder":
        self.rules.append(rule)
        return self

    def add_process(self, process: Process) -> "RequirementsGraphBuilder":
        self.processes.append(process)
        return self

    def add_event(self, event: Event) -> "RequirementsGraphBuilder":
        self.events.append(event)
        return self

    def add_constraint(self, constraint: Constraint) -> "RequirementsGraphBuilder":
        self.constraints.append(constraint)
        return self

    def add_capability(self, capability: Capability) -> "RequirementsGraphBuilder":
        self.capabilities.append(capability)
        return self

    def add_relationship(self, rel: RequirementRelationship) -> "RequirementsGraphBuilder":
        self.relationships.append(rel)
        return self

    def build(self) -> Graph:
        graph = Graph(layer=GraphLayer.REQUIREMENTS)

        for req in self.requirements:
            node = Node(
                id=req.id,
                type="Requirement",
                layer=GraphLayer.REQUIREMENTS,
                properties={
                    "statement": req.statement,
                    "entities": list(req.entities),
                    "actors": list(req.actors),
                    "rules": list(req.rules),
                    **req.properties,
                },
                status=req.status,
                provenance=req.provenance,
            )
            graph.add_node(node)

        for actor in self.actors:
            graph.add_node(
                Node(
                    id=actor.id,
                    type="Actor",
                    layer=GraphLayer.REQUIREMENTS,
                    properties={"name": actor.name, "role_type": actor.role_type, "description": actor.description, **actor.properties},
                    status=AssertionStatus.OBSERVED,
                )
            )

        for rule in self.rules:
            graph.add_node(
                Node(
                    id=rule.id,
                    type="BusinessRule",
                    layer=GraphLayer.REQUIREMENTS,
                    properties={"name": rule.name, "statement": rule.statement, "expression": rule.expression, **rule.properties},
                    status=AssertionStatus.OBSERVED,
                )
            )

        for proc in self.processes:
            graph.add_node(
                Node(
                    id=proc.id,
                    type="Process",
                    layer=GraphLayer.REQUIREMENTS,
                    properties={"name": proc.name, "description": proc.description, "steps": list(proc.steps), **proc.properties},
                    status=AssertionStatus.OBSERVED,
                )
            )

        for evt in self.events:
            graph.add_node(
                Node(
                    id=evt.id,
                    type="Event",
                    layer=GraphLayer.REQUIREMENTS,
                    properties={"name": evt.name, "payload_schema": evt.payload_schema, "triggered_by": evt.triggered_by, **evt.properties},
                    status=AssertionStatus.OBSERVED,
                )
            )

        for const in self.constraints:
            graph.add_node(
                Node(
                    id=const.id,
                    type="Constraint",
                    layer=GraphLayer.REQUIREMENTS,
                    properties={"name": const.name, "constraint_type": const.constraint_type, "target": const.target, **const.properties},
                    status=AssertionStatus.OBSERVED,
                )
            )

        for cap in self.capabilities:
            graph.add_node(
                Node(
                    id=cap.id,
                    type="Capability",
                    layer=GraphLayer.REQUIREMENTS,
                    properties={"name": cap.name, "description": cap.description, "parameters": cap.parameters, **cap.properties},
                    status=AssertionStatus.OBSERVED,
                )
            )

        for rel in self.relationships:
            if rel.source_id in graph.nodes and rel.target_id in graph.nodes:
                graph.add_relationship(
                    Relationship(
                        id=rel.id,
                        source=rel.source_id,
                        type=rel.type,
                        target=rel.target_id,
                        layer=GraphLayer.REQUIREMENTS,
                        properties=rel.properties,
                        status=AssertionStatus.OBSERVED,
                    )
                )

        return graph
