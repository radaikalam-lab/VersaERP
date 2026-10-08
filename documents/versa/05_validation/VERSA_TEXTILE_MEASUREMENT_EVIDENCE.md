# VERSA ERP — TEXTILE MEASUREMENT & DUAL-UOM EVIDENCE

## 1. Executive Summary

Textile manufacturing operates simultaneously across multiple non-linear measurement dimensions (mass, linear length, surface area, yarn count, tension, moisture, and density). A standard linear ERP conversion factor (e.g. $1\text{ Box} = 10\text{ Pcs}$) fails because fabric dimensions dynamically shift across wet processing, tension relaxation, and environmental humidity.

This artifact compiles the empirical measurement standards, formulas, and conversion classifications discovered across the textile archaeology corpus.

---

## 2. Core Textile Measurement Units & Systems

### 2.1 Mass & Packaging UOMs
- **Kilogram (`kg`):** Universal transaction and inventory base unit for raw cotton, yarn cones, greige fabric rolls, dyes/chemicals, and scrap.
- **Gram (`g`):** Precision laboratory testing unit for GSM cutting and lab-dip dyestuff weighing.
- **Bale (`Bale`):** Standard raw cotton trading unit in India ($1\text{ Indian Cotton Bale} = 170\text{ kg} = 374.78\text{ lbs}$).
- **Cone (`Cone`):** Physical yarn spool unit (typically $1.89\text{ kg}$ to $2.20\text{ kg}$ per cone).
- **Roll / Thaan (`Roll`):** Physical continuous knitted or woven fabric piece ($18\text{ kg}$ to $26\text{ kg}$ for circular knit; $50\text{ m}$ to $120\text{ m}$ for woven).
- **Bag (`Bag`):** Standard yarn packaging unit ($1\text{ Bag} = 24\text{ Cones} \approx 45.36\text{ kg}$ to $50.0\text{ kg}$).

### 2.2 Linear Length & Surface Dimensions
- **Meter (`m`):** Standard metric unit for cuttable fabric length and garment consumption.
- **Yard (`yd`):** Traditional commercial unit for fabric export contracts and ASTM 4-point inspection ($1\text{ yd} = 0.9144\text{ m}$).
- **Inch (`in`):** Standard cuttable width specification unit (e.g. 58", 60", 72").
- **Centimeter (`cm`):** Garment size tech pack measurement unit (Chest width, HSP to hem, sleeve length).

### 2.3 Yarn Numbering / Count Systems
- **English Cotton Count ($N_e$):** Indirect system (number of $840\text{-yard}$ hanks per $1\text{ lb}$ of mass). Higher number = finer yarn. Example: $30s, 34s, 40s, 60s$.
- **Metric Count ($N_m$):** Indirect system (meters per gram of mass).
- **Denier ($D$):** Direct system (mass in grams of $9,000\text{ meters}$ of yarn). Used for synthetic filament (Polyester, Nylon, Spandex/Elastane). Example: $75D, 150D, 20D$ Spandex.
- **Tex / Decitex ($dtex$):** ISO standard direct system (mass in grams per $1,000\text{ m}$ / $10,000\text{ m}$).

### 2.4 Fabric Structural & Quality Metrics
- **GSM ($g/m^2$):** Grams per square meter. Primary weight classification for knitwear and finished fabric.
- **GLM ($g/linear\ m$):** Grams per linear meter: $\text{GLM} = \text{GSM} \times (\text{Width in meters})$.
- **Cuttable Width:** Total fabric open width minus selvedges / stenter pinholes (typically nominal width minus $1.0 - 1.5\text{ inches}$).
- **Count Strength Product (CSP):** Yarn breaking strength metric (Lea strength in lbs $\times$ Actual yarn count $N_e$). Standard combed cotton requires $\ge 2800\text{ CSP}$.
- **Moisture Regain %:** Ratio of moisture weight to dry weight. Standard commercial regain for Cotton = $8.5\%$, Polyester = $0.4\%$, Viscose = $11.0\%$.

---

## 3. Classification of Measurement Conversions

### A. Deterministic Conversions (Static Mathematical Constants)
These conversions are mathematically immutable and can be executed universally across any module:
$$\text{Meters} = \text{Yards} \times 0.9144$$
$$\text{Inches} = \text{Centimeters} \div 2.54$$
$$\text{Kilograms} = \text{Pounds (lbs)} \times 0.45359237$$
$$\text{Denier} = \text{Tex} \times 9 = \frac{5315}{N_e}$$

### B. Context-Dependent Conversions (Formula-Driven per Item Specification)
These conversions depend on static master specifications (Target GSM and Cuttable Width) of a specific fabric item:
$$\text{Theoretical Fabric Length (meters)} = \frac{\text{Fabric Weight (kg)} \times 1000}{\text{GSM} \times (\text{Cuttable Width (inches)} \times 0.0254)}$$

$$\text{Theoretical Fabric Weight (kg)} = \frac{\text{Fabric Length (meters)} \times (\text{Cuttable Width (inches)} \times 0.0254) \times \text{GSM}}{1000}$$

*Invariant Rule:* In `Versa Fabric Roll` (ENT-018), observed physical weight and measured length must satisfy this relationship within a **$\pm 5.0\%$ tolerance band** to prevent inventory weight manipulation.

### C. Process-Dependent Conversions (Non-Linear Manufacturing Transitions)
These conversions cannot be predicted purely from static math because physical state changes during wet processing:
- **Knitting (Greige):** Greige fabric has higher width and lower GSM before relaxation.
- **Scouring & Bleaching:** Loss of natural cotton waxes, pectins, and sizing materials ($3.0\% - 5.5\%$ weight loss).
- **Dyeing:** Dyestuff and chemical salt absorption ($1.0\% - 3.0\%$ weight pickup depending on shade depth).
- **Stentering & Compacting:** Mechanical stretching or overfeeding alters length, width, and final GSM significantly (e.g. lengthwise shrinkage locked to $\le -5.0\%$).

*Versa Rule:* Process-dependent state transitions must **never** use static multiplication factors. They must record the actual measured output weight and output length at the conclusion of each `Versa Job Work Order` / process stage.

---

## 4. Architectural Guidance for Multi-UOM Implementation

1. **Inventory Base UOM:** Keep `kg` as the authoritative inventory base unit in the ERPNext Stock Ledger for yarn and fabric.
2. **Secondary Physical UOM:** Maintain `length_meters` as an auditable attribute on `Versa Fabric Roll` without creating a fragmented second inventory ledger.
3. **Transaction Dual Display:** Display both Weight (kg) and Length (meters) on dispatch notes and delivery challans, using the verified roll-level physical data.
