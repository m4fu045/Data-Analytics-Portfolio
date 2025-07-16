# Supplier Scoring Algorithm

## Overview
Multi-criteria weighted scoring model for strategic supplier classification across business units.

## Core Formula

```
Score = BU_Impact × BU_Scale × [
    W₂ × Sole_Source_Ratio + 
    W₃ × Single_Source_Ratio + 
    W₄ × Multi_Source_Ratio +
    W₅ × Ramp_Time_Component + 
    W₆ × Spend_Component +
    W₇ × Partnership_Component + 
    W₈ × Innovation_Component + 
    W₉ × Risk_Component
]
```

## Component Calculations

### 1. Source Type Components
- **Sole Source Ratio** = Sole_Source_Parts / Total_Parts
- **Single Source Ratio** = Single_Source_Parts / Total_Parts  
- **Multi Source Ratio** = Multi_Source_Parts / Total_Parts

### 2. Ramp Time Component
```
Ramp_Component = 1 - 1/(1 + (Ramp_Time_Months/12)²)
```
- Normalizes ramp time impact (0-1 scale)
- Longer ramp times = higher dependency scores

### 3. Spend Component
```
Spend_Component = 1 - 1/(1 + Annual_Spend/100)
```
- Logarithmic scaling for spend impact
- Prevents large spenders from dominating scores

### 4. Qualitative Components
- **Partnership** = Partnership_Score / 3 (1-3 scale normalized)
- **Innovation** = Innovation_Score / 3 (1-3 scale normalized)  
- **Risk** = (4 - Risk_Score) / 3 (inverted: lower risk = higher score)

## Scoring Scale
- **Final Score Range**: 0-100
- **Higher scores** = More strategic importance
- **Lower scores** = More transactional nature

## Implementation Notes
- All components normalized to 0-1 scale before weighting
- Business unit factors applied as multipliers
- Algorithm handles missing data with default values