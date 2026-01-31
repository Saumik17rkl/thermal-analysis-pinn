# Thermal Analysis 

**Python Physics Model · Flask API · PINN Extension**

---

## 📌 Project Overview

This project implements a **physics-based thermal resistance model** for a processor–heat-sink system, validates it against a provided Excel reference, exposes it via a **Flask API**, and extends it with a **Physics-Informed Neural Network (PINN)** for spatial temperature field estimation.

The work strictly follows the **step-by-step methodology** described in the provided *Thermal_Reference.pdf* and uses *Heat_Sink_Design_Ref.xlsx* **only for validation**, not as a source of physics.

---

## 🎯 Objectives (Mapped to Assessment)

### 1. Python Thermal Model

* Implement junction-to-ambient thermal resistance network
* Compute:

  * TIM resistance
  * Heat sink conduction resistance
  * Forced convection resistance
  * Total thermal resistance
  * Junction temperature
* Match results with Excel reference

### 2. Flask API

* Wrap the validated physics model into a REST API
* Accept geometry, material, and airflow inputs
* Return full resistance breakdown + junction temperature

### 3. PINN (Physics-Informed Neural Network)

* Use the validated thermal model as a **physics backbone**
* Learn spatial temperature distribution inside the heat sink
* Enforce governing PDE and boundary conditions via loss functions

---

## 🧠 Design Philosophy

* **Physics first, ML second**
* Deterministic model is the source of truth
* PINN is an extension, **not a replacement**
* Clear separation of concerns:

  * Core physics
  * API layer
  * PINN layer

---

## 📁 Project Structure

```
assignment/
│
├── app/                     # Flask API layer
│   ├── main.py
│   ├── routes/
│   ├── services/
│   └── schemas/
│
├── core/                    # Deterministic thermal physics
│   ├── constants.py
│   ├── geometry.py
│   ├── tim.py
│   ├── conduction.py
│   ├── convection.py
│   ├── resistance_network.py
│   └── solver.py
│
├── pinn/                    # Physics-Informed Neural Network
│   ├── domain.py
│   ├── model.py
│   ├── losses.py
│   ├── trainer.py
│   ├── inference.py
│   └── validation.py
│
├── validation/              # Excel validation artifacts
│   ├── reference_inputs.json
│   └── validation_notes.md
│
├── tests/                   # Unit & API tests
│
├── docs/
│   └── implementation_steps.md
│
├── requirements.txt
└── README.md
```

---

## 🔬 Thermal Model Details
## Use of Reference Documents

The following reference files are used during design and validation,
but are not runtime dependencies of the application:

- ET_Assessment_CSE.pdf: Defines assessment scope and requirements
- Thermal_Reference.pdf: Source of governing equations and assumptions
- Heat_Sink_Design_Ref.xlsx: Used to validate numerical results

All equations from the references are explicitly implemented
in the `core/` module. The Excel file is used only to verify
numerical correctness and is not read programmatically.

### Thermal Resistance Network

```
Junction → Case → TIM → Heat Sink → Ambient
```

[
R_{total} = R_{jc} + R_{TIM} + R_{hs}
]

Where:

* ( R_{hs} = R_{cond} + R_{conv} )

### Key Physics Implemented

* 1D conduction through heat sink base
* Forced convection through fin channels
* Reynolds number–based regime selection
* Sieder–Tate (laminar) and Dittus–Boelter (turbulent) correlations
* Junction temperature:
  [
  T_j = T_{ambient} + Q \cdot R_{total}
  ]

---

## ✅ Validation

* Model validated against *Heat_Sink_Design_Ref.xlsx*
* Reference results:

  * Heat sink resistance ≈ **0.373 °C/W**
  * Junction temperature ≈ **80.96 °C**
* Deviations < 1% (rounding / area interpretation)
* Details documented in `validation/validation_notes.md`

---

## 🌐 Flask API

### API Responsibilities

* No physics logic inside routes
* Thin wrapper over validated core model

### Typical Output

* RTIM
* Rcond
* Rconv
* Rhs
* Rtotal
* Junction temperature

---

## 🤖 PINN Extension

### Why PINN?

* Deterministic model gives **scalar temperatures**
* PINN estimates **spatial temperature field** ( T(x, y, z) )

### Governing Physics

* Steady-state heat equation:
  [
  \nabla \cdot (k \nabla T) = 0
  ]

### Boundary Conditions

* Prescribed heat flux at die interface
* Convective BC on fin surfaces
* Physics-consistency loss ties PINN to lumped model output

### Validation

* Energy conservation
* Agreement with lumped thermal resistance model
* Physical temperature gradients

---

## ▶️ How to Run (High Level)

1. Install dependencies

   ```
   pip install -r requirements.txt
   ```

2. Run core model / tests

   ```
   pytest
   ```

3. Run Flask API

   ```
   python app/main.py
   ```

4. (Optional) Train PINN

   ```
   python pinn/trainer.py
   ```

---

## 🧪 Testing

* Unit tests for:

  * Geometry
  * Conduction
  * Convection
  * Resistance network
* API tests for response correctness

---

## 🧾 Notes

* All physics equations come from the provided PDF reference
* Excel is used strictly for validation
* PINN is implemented only after physics model validation
* The structure is designed for **clarity, auditability, and extensibility**

---

## 👤 Author

**Saumik Chakraborty**
B.Tech CSE (Final Year)
Focus: Python · AI/ML · Engineering Systems
# thermal-analysis-pinn
