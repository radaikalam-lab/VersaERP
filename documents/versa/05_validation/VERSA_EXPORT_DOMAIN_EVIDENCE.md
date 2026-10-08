# VERSA ERP — EXPORT, PACKING & LOGISTICS DOMAIN EVIDENCE

## 1. Executive Summary

Tiruppur accounts for over 50% of India's cotton knitwear garment exports. Apparel export operations are characterized by rigid buyer compliance, complex ratio packing, barcode serialization down to individual cartons, container CBM utilization calculations, and strict export trade documentation.

This artifact compiles the export, cartonization, and shipping semantics extracted from the repository archaeology.

---

## 2. Commercial Export Transaction Chain

```text
[ Buyer Export Purchase Order ]
              │
              ▼
[ Versa Sales Order ] (Commercial Root: Incoterms, Currency, Buyer Style Ref)
              │
              ▼
[ Versa Order Matrix ] (Size x Colour x Shade breakdown)
              │
              ▼
[ Production Batches & Finishing ]
              │
              ▼
[ Versa Packing Plan ] (Solid / Ratio Carton Allocation)
              │
              ▼
[ Versa Carton ] (Serialized QR/Barcode, Gross/Net Weight, CBM)
              │
              ▼
[ ERPNext Delivery Note ] (Dispatch from Factory Gate)
              │
              ▼
[ ERPNext Sales Invoice ] (Export Commercial Invoice with GST LUT / Drawback)
              │
              ▼
[ Container Stuffing & Shipping Bill ] (Port of Loading: Tuticorin / Chennai / Cochin)
```

---

## 3. Garment Packing Paradigms & Cartonization

In global apparel retail, buyers specify exact carton packing configurations:

### 3.1 Packing Types
1. **Solid Colour Solid Size (SCSS):**
   - Each carton contains only one colourway and one size (e.g. Carton #1: 24 pcs Red Size M).
2. **Solid Colour Ratio Size (SCRS):**
   - Each carton contains one colourway with a pre-defined size ratio matching store distribution (e.g. Ratio 1:2:2:1 for S:M:L:XL = 24 pcs/carton).
3. **Assorted Colour Ratio Size (ACRS):**
   - Each carton contains multiple colourways and multiple sizes (e.g. 2 Red S, 4 Red M, 2 Navy S, 4 Navy M).

### 3.2 Carton Barcode & Weight Auditing
- Every `Versa Carton` receives a globally unique serialized barcode (`CTN-YYYY-#####`).
- **Physical Weight Audit Invariant:**
  $$\text{Expected Gross Weight} = \text{Tare Weight of Empty Carton} + \sum (\text{Qty} \times \text{Garment Piece Weight})$$
  $$\text{Weight Tolerance Check} = |\text{Observed Scale Weight} - \text{Expected Gross Weight}| \le 0.15\text{ kg}$$
  *Purpose:* Prevents missing garment pieces or foreign object contamination (e.g. broken needle fragments) prior to export container stuffing.

---

## 4. Container Volumetric & Stuffing Calculations

Export logistics optimize freight costs by calculating Cubic Meters (CBM):
$$\text{Carton CBM} = \frac{\text{Length (cm)} \times \text{Width (cm)} \times \text{Height (cm)}}{1,000,000}$$
$$\text{Total Shipment CBM} = \sum (\text{Planned Total Cartons} \times \text{Carton CBM})$$

### Standard Ocean Container Capacities:
- **20ft General Purpose (GP):** Usable Volume: $28 - 30\text{ CBM}$ | Max Payload: $21,500\text{ kg}$
- **40ft High Cube (HC):** Usable Volume: $68 - 70\text{ CBM}$ | Max Payload: $26,500\text{ kg}$

---

## 5. Export Trade Documentation & Compliance Fields

| Document | Primary Data Elements | Versa & ERPNext Mapping |
| :--- | :--- | :--- |
| **Commercial Invoice** | Invoice No, Date, Buyer PO, Style No, Total Pcs, FOB Unit Price, Incoterms (FOB/CIF/CFR), Payment Terms (LC, DA, DP), Bank AD Code, GST LUT/Bond reference. | ERPNext `Sales Invoice` with Versa Custom Fields (`versa_style`, `versa_packing_plan`). |
| **Packing List** | Carton Numbers (1 to N), Carton-wise Item/Size/Colour breakdown, Gross Weight, Net Weight, Total CBM, Container & Seal Number. | Auto-generated from `Versa Packing Plan` (ENT-025) and `Versa Carton` (ENT-022). |
| **Shipping Bill** | Port of Loading (e.g. INMAA - Chennai, INTUT - Tuticorin), Port of Discharge, HS Codes (Chapter 61/62 Knitted/Woven Garments), RoDTEP / Duty Drawback claim codes. | Linked to `Delivery Note` & `Sales Invoice`. |
| **Certificate of Origin** | Country of Origin (India), GSP / Free Trade Agreement declarations. | Export report template. |

---

## 6. Strategic Validation of Versa Authority Model

The archaeology confirms that:
1. **The Sales Order must remain the commercial root** for export manufacturing.
2. **`Versa Packing Plan` and `Versa Carton` correctly model the physical logistics layer** without duplicating ERPNext inventory ledgers.
3. Packing and container dispatch seamlessly link to standard ERPNext `Delivery Note` and `Sales Invoice`.
