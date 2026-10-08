# VERSA ERP — WET PROCESSING DOMAIN EVIDENCE

## 1. Executive Summary

Wet processing (pretreatment, dyeing, bio-polishing, printing, stentering, and finishing) is the most capital-intensive, chemically complex, and environmentally regulated phase of textile manufacturing in Tamil Nadu (Tiruppur, Erode, Perundurai SIPCOT, Salem).

This document captures the empirical wet processing workflows, recipe management paradigms, machine operating parameters, and environmental governance requirements extracted during the repository archaeology.

---

## 2. Standard Wet Processing Sequence & Transformations

```text
[ Greige Fabric (Knitted / Woven) ]
        │
        ▼ (Mechanical Pretreatment)
[ Singeing ] ── (Gas flame removes protruding surface fuzz/fibers)
        │
        ▼ (Chemical Pretreatment)
[ Desizing & Scouring ] ── (Enzymatic removal of starch/sizing; Caustic soda saponification of natural oils/waxes)
        │
        ▼
[ Bleaching ] ── (Hydrogen peroxide $H_2O_2$ oxidative decolorization for optical whiteness; weight loss: 3–5%)
        │
        ▼ (Optional for high-luster/strength)
[ Mercerization ] ── (High-concentration NaOH swelling; improves dye affinity and tensile strength)
        │
        ▼
[ Dyeing / Color Fixation ] ── (Softflow Jet / Winch / Airflow: Reactive dyes for cotton, Disperse for polyester; Liquor ratio 1:4 to 1:8)
        │
        ▼
[ Washing & Bio-Polishing ] ── (Cellulase enzyme wash removes pilling; acetic acid neutralization)
        │
        ▼
[ Hydro-Extraction / Slitting ] ── (Centrifugal moisture reduction to ~50%; tubular fabric open-width slitting)
        │
        ▼
[ Stenter (Heat-Setting) ] ── (Thermo-fixation at 160°C–195°C; width stretching, overfeed %, chemical softener application)
        │
        ▼
[ Compacting / Sanforizing ] ── (Felt calendar compaction locks dimensional stability; length shrinkage $\le -5\%$)
        │
        ▼
[ Finished Fabric Rolls ] ── (100% 4-point inspection, lab testing, barcode tagging)
```

---

## 3. Recipe Management & Chemical Inputs

### 3.1 Liquor Ratio Concept
In textile wet processing, all chemical dosing is calculated relative to total dry fabric batch weight:
$$\text{Total Liquor Volume (Liters)} = \text{Batch Fabric Weight (kg)} \times \text{Liquor Ratio (e.g. 1:6)}$$

### 3.2 Dyestuff & Auxiliary Calculation
Chemical components are specified in two distinct units:
1. **On Weight of Fabric (`% OWF`):** Applied to primary dyestuffs and exhaustion chemicals:
   $$\text{Dyestuff Mass (g)} = \text{Fabric Weight (kg)} \times \left(\frac{\text{Recipe } \%}{100}\right) \times 1000$$
2. **Grams per Liter (`g/L`):** Applied to bath conditioning chemicals (Sequestering agents, leveling agents, wetting agents, defoamers):
   $$\text{Chemical Mass (g)} = \text{Total Liquor Volume (L)} \times \text{Chemical Concentration (g/L)}$$

---

## 4. Machine Telemetry & Quality Critical Parameters

| Process Stage | Key Machine Parameters | Critical Quality Metrics | Rejection / Risk Factor |
| :--- | :--- | :--- | :--- |
| **Dyeing (Jet/Softflow)** | Heating rate (°C/min), dwell time (min), pump pressure (bar), cooling rate | Shade matching ($\Delta E \le 0.8$ CMC 2:1), surface pH ($6.0 - 7.5$) | Patchy dyeing, shade variation, rope marks. |
| **Bio-Polishing** | Bath temperature (55°C), pH (4.5–5.0), enzyme incubation time (45 min) | Pilling resistance (ASTM D3512 $\ge$ Grade 4.0), fabric weight loss | Excessive strength loss (bursting strength failure). |
| **Stenter Finishing** | Chamber temps (6–8 zones, 160°C–190°C), speed (m/min), overfeed %, padder pressure | Cuttable width (inches), bowing/skewing %, handle/feel | Insufficient heat setting, yellowing of white fabric. |
| **Compactor** | Steam pressure (bar), shoe temp (°C), overfeed %, compaction pressure | Lengthwise & widthwise shrinkage ($\le -5.0\%$), spirality ($\le 4.0\%$) | High residual shrinkage after garment washing. |

---

## 5. Environmental Governance: ETP & Zero Liquid Discharge (ZLD)

In Tiruppur and Erode, environmental compliance is a strict legal precondition for textile processing:
- **Zero Liquid Discharge (ZLD) Mandate:** 100% of industrial effluent must be recycled through multi-stage RO (Reverse Osmosis) and Multiple Effect Evaporators (MEE), with brine crystallization of sodium sulfate / sodium chloride for reuse in dyeing.
- **Job Worker AVL Gating:** A dyeing subcontractor must possess an active PCB (Pollution Control Board) license and verified ZLD plant connectivity. In Versa, this is governed by `Versa Job Worker.compliance_status == 'Compliant'` (Invariant `job_worker_avl_check`).

---

## 6. Architecture Boundary: Generic Versa Process Model vs Vertical Specifics

| Concept | Classification in Versa | Home DocType / Module |
| :--- | :--- | :--- |
| **Subcontract Process Stage** | **Generic Process Model** | `Versa Job Work Order` (`process` selection) |
| **Allowed Loss & Scrap %** | **Generic Process Model** | `Versa Job Work Order` (`allowed_loss_pct`) |
| **Process Quality Standards** | **Domain Quality Spec** | `Versa QC Spec` & `Versa QC Parameter` |
| **Shade Reference & Recipe Code** | **Textile Master** | `Versa Shade` (`recipe_code`, `lab_dip_no`) |
| **Live Stenter / SCADA IoT Data** | **Deferred Future Vertical** | *Shop-Floor Intelligence (Phase 8+)* |
| **ZLD Chemical Salt Recycling Balance** | **Deferred Future Vertical** | *Advanced Chemical Extension* |
