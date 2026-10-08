# VERSA ERP MULTI-TIER QUALITY ASSURANCE (QA/QC) CONTRACT SPECIFICATION

## 1. Objective & Design Principles

In the textile and garment manufacturing industry, quality cannot be reduced to a binary pass/fail checkbox. Quality is an **evidence-producing operational discipline** characterized by versioned specifications, standardized lab test methods (ISO, ASTM, AATCC), multi-point physical readings, statistical tolerance limits, and strict quarantine gates.

This contract defines the data structures, inspection lifecycles, and disposition rules for the Versa Quality subsystem.

---

## 2. Multi-Tier Quality Architecture

```text
  [ Versa QC Spec ] (Versioned master: Material Type, Product Type, Buyer Standard)
          │
          ▼
  [ Versa QC Parameter ] (Target, Min Limit, Max Limit, UOM, Test Method, Severity)
          │
          ▼
  [ Versa QC Result ] (Inspection Event: Receipt, Job Work, Batch, Roll Barcode)
          │
          ▼
  [ Versa QC Measurement ] (Actual numeric/categorical readings, Pass/Fail/Deviation)
          │
          ▼
  [ Inspection Disposition Engine ]
     ┌──────────────────────┬──────────────────────┬──────────────────────┐
     ▼                      ▼                      ▼                      ▼
[ Accepted ]     [ Accepted with Concession ] [ Quarantine ]         [ Rejected ]
```

---

## 3. Textile Domain-Specific Quality Parameters & Standards

### 3.1 Yarn Quality Standards (Spinning / Yarn Inward)

| Parameter Code | Parameter Name | Test Method | Typical UOM | Target / Range | Severity |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `YRN_COUNT_ACTUAL` | Actual Yarn Count (Ne) | ASTM D1907 | Ne | Nominal $\pm 1.5\%$ | Critical |
| `YRN_CSP` | Count Strength Product (CSP) | Lea Test (ASTM D1578) | lbs $\times$ count | $\ge 2800$ (Combed) | Major |
| `YRN_TWIST_TPI` | Twist Per Inch (TPI) | ASTM D1422 | TPI | $22.0 \pm 1.0$ | Minor |
| `YRN_MOISTURE_PCT` | Moisture Regain % | Oven Dry Method | % | $7.0\% - 8.5\%$ | Major |
| `YRN_UNEVEN_U_PCT` | Yarn Unevenness (U%) | Uster Tester 5/6 | % | $\le 9.5\%$ | Major |
| `YRN_THIN_THICK_NEP` | Imperfections (IPI) | Uster Tester (-50%/+50%/+200%) | /km | $\le 80$ | Minor |

### 3.2 Fabric Quality Standards (Knitting & Finishing)

| Parameter Code | Parameter Name | Test Method | Typical UOM | Target / Range | Severity |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `FAB_GSM_ACTUAL` | Measured GSM | ASTM D3776 / GSM Cutter | $g/m^2$ | Nominal $\pm 3.0\%$ | Critical |
| `FAB_WIDTH_CUTTABLE` | Cuttable Width | ASTM D3774 | Inches | Nominal $-0.5 / +1.5$ | Critical |
| `FAB_SHRINK_LEN_PCT`| Lengthwise Shrinkage % | AATCC 135 / ISO 6330 | % | $\le -5.0\%$ | Critical |
| `FAB_SHRINK_WID_PCT`| Widthwise Shrinkage % | AATCC 135 / ISO 6330 | % | $\le -5.0\%$ | Critical |
| `FAB_SPIRALITY_PCT` | Spirality / Torque % | AATCC 179 | % | $\le 4.0\%$ | Major |
| `FAB_COLOR_DELTA_E` | Shade Difference ($\Delta E$) | Spectrophotometer (CIE $L^*a^*b^*$) | $\Delta E$ | $\le 0.8$ (CMC 2:1) | Critical |
| `FAB_DEFECT_SCORE` | 4-Point Defect Score | ASTM D5430 | Points/100 sq yd | $\le 20$ (Grade A) | Major |

### 3.3 Dyeing & Chemical Fastness Standards

| Parameter Code | Parameter Name | Test Method | Typical UOM | Target / Range | Severity |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `DYE_PH_VALUE` | Fabric Surface pH | ISO 3071 / AATCC 81 | pH | $6.0 - 7.5$ | Major |
| `DYE_WASH_FASTNESS` | Colour Fastness to Washing | ISO 105-C06 (A2S) | Grade (1-5) | $\ge 4.0$ | Critical |
| `DYE_RUB_DRY` | Rubbing Fastness (Dry) | ISO 105-X12 (Crockmeter) | Grade (1-5) | $\ge 4.0$ | Major |
| `DYE_RUB_WET` | Rubbing Fastness (Wet) | ISO 105-X12 (Crockmeter) | Grade (1-5) | $\ge 3.0 - 3.5$ | Major |
| `DYE_LIGHT_FASTNESS`| Colour Fastness to Light | ISO 105-B02 (Xenon Arc) | Blue Wool (1-8) | $\ge 4.0$ | Major |

### 3.4 Garment Quality & AQL Standards (Final Inspection)

| Parameter Code | Parameter Name | Test Method | Inspection Standard | Severity |
| :--- | :--- | :--- | :--- | :--- |
| `GAR_CHEST_WIDTH` | Chest Width Measurement | Measurement Tape vs Tech Pack | Spec $\pm 0.5$ cm | Major |
| `GAR_BODY_LENGTH` | Body Length (HSP to Hem) | Measurement Tape vs Tech Pack | Spec $\pm 0.5$ cm | Major |
| `GAR_SEAM_STRENGTH` | Seam Tensile Strength | ASTM D1683 | $\ge 120$ N | Critical |
| `GAR_CRITICAL_DEFECT`| Sharp needles, holes, stains | Visual 100% / AQL 0.0 | Max 0 defects | Critical (Auto-Fail) |
| `GAR_MAJOR_DEFECT` | Misalignment, shade bar | AQL 1.5 / 2.5 (ISO 2859-1) | Within AQL table | Major |
| `GAR_MINOR_DEFECT` | Loose threads, slight skip | AQL 4.0 (ISO 2859-1) | Within AQL table | Minor |

---

## 4. Inspection Lifecycle & Disposition Governance

```text
                                 [ Inspection Performed ]
                                            │
                                            ▼
                    ┌───────────────────────┴───────────────────────┐
                    │ Are all Critical & Major parameters passing?  │
                    └───────────────────────┬───────────────────────┘
                                            │
                          ┌─────────────────┴─────────────────┐
                         YES                                 NO
                          │                                   │
                          ▼                                   ▼
                   [ Status: ACCEPTED ]           ┌───────────┴───────────┐
                          │                       │ Is defect commercial  │
                          ▼                       │ or reworkable?        │
              [ Release to Active Stock /         └───────────┬───────────┘
                Production / Shipment ]                       │
                                            ┌─────────────────┴─────────────────┐
                                      YES (Minor deviation)            NO (Unusable / Off-spec)
                                            │                                   │
                                            ▼                                   ▼
                              [ Status: CONCESSION ]                 [ Status: REJECTED ]
                                            │                                   │
                                            ▼                                   ▼
                              [ Requires QA Head + Buyer Concession ] [ Quarantine / Debit / Return ]
```

---

## 5. Traceability & Lineage Invariants

1. **Lot/Roll Lineage Rule:** Every `Versa QC Result` must link to at least one physical tracking identifier (`Versa Fabric Roll.roll_barcode`, `Batch.name`, or `Versa Carton.carton_barcode`).
2. **Defect Score Grading Invariant (ASTM D5430 4-Point System):**
   $$\text{Points per 100 sq yds} = \frac{\text{Total Defect Points} \times 3600}{\text{Inspected Length (yds)} \times \text{Cuttable Width (inches)}}$$
   - **Grade A:** Score $\le 20.0 \implies$ `Status: Accepted`
   - **Grade B:** $20.1 < \text{Score} \le 28.0 \implies$ `Status: Concession`
   - **Grade C / Reject:** Score $> 28.0 \implies$ `Status: Rejected`

