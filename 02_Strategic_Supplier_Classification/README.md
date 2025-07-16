# Strategic Supplier Classification Model
*Data-Driven Supplier Segmentation and Risk Assessment*

## 📋 Project Overview

**Industry:** Fortune 500 Technology Hardware Manufacturing  
**Duration:** December 2023 - March 2024  
**Role:** Project Manager / Supply Chain Data Analyst  
**Tools:** Python, Mathematical Modeling, Excel, Data Integration  

# 🎯 Business Challenge

### Problem Statement:
- **Scale Challenge:** Classify and manage 1,000+ suppliers across multiple business units
- **Inconsistent Methodology:** Different business units using varied supplier evaluation criteria
- **Resource Allocation:** Need to prioritize supplier relationships and management efforts
- **Risk Management:** Lack of standardized supplier risk assessment framework

### Business Impact:
- Inefficient supplier relationship management
- Suboptimal resource allocation across strategic vs. transactional suppliers
- Inconsistent supplier development and monitoring approaches
- Difficulty in identifying critical supplier dependencies

## 💡 Solution Design

### Objectives:
1. **Standardized Classification:** Develop unified supplier segmentation methodology
2. **Multi-criteria Analysis:** Integrate quantitative and qualitative assessment factors
3. **Business Unit Customization:** Tailor weighting schemes for different operational needs
4. **Automated Scoring:** Create scalable evaluation system for ongoing assessments

### Technical Approach:
- **Multi-factor Scoring Algorithm:** Weighted evaluation across 7 key criteria
- **Business Unit Optimization:** Custom weight configurations for Print vs. Personal Systems
- **Data Integration:** Combine spend data, risk assessments, and relationship metrics
- **Segmentation Framework:** Four-tier classification system with clear action plans

## 📊 Methodology & Implementation

### 1. **Evaluation Criteria Framework**

#### Quantitative Metrics:
- **Annual Spend Volume:** Financial impact and purchasing leverage
- **Supply Dependency:** Source type analysis (Sole/Single/Multi-source)
- **Supplier Ramp Time:** New supplier onboarding complexity (months)

#### Qualitative Assessments:
- **Partnership Quality:** Relationship strength and collaboration level
- **Innovation Potential:** Supplier's R&D capabilities and future value
- **Supply Risk:** Geographic, financial, and operational risk factors

### 2. **Weighted Scoring Algorithm**

```
Score = (BU_Impact/100) × (BU_Scale/3) × [
    W₂×(Sole_Source_Ratio) + W₃×(Single_Source_Ratio) + W₄×(Multi_Source_Ratio) +
    W₅×(1 - 1/(1 + (Ramp_Time/12)²)) + W₆×(1 - 1/(1 + Spend/100)) +
    W₇×(Partnership_Score/3) + W₈×(Innovation_Score/3) + W₉×(Supply_Risk_Score/3)
]
```

### 3. **Business Unit Customization**

#### Business Unit A Weights:
- **Part Source Type:** 30% (High dependency focus)
- **Time to Ramp:** 25% (Critical for manufacturing continuity)
- **Partnership:** 25% (Long-term relationship emphasis)
- **Spend:** 10% (Volume less critical than dependency)
- **Innovation:** 5%, **Supply Risk:** 5%

#### Business Unit B Weights:
- **Supply Risk:** 20% (Higher risk sensitivity)
- **Time to Ramp:** 20% (Rapid scaling requirements)
- **Part Source Type:** 15% (More supplier options available)
- **Partnership:** 25%, **Innovation:** 10%, **Spend:** 10%

### 4. **Segmentation Categories**

#### Strategic (<5% of suppliers)
- **Characteristics:** High dependency, high expenditure, complex switching
- **Strategy:** Partnership development, long-term contracts, joint innovation
- **Management:** Executive-level relationship management

#### Critical (15% of suppliers)
- **Characteristics:** Specialized capabilities, potential future partners
- **Strategy:** Performance monitoring, capability development
- **Management:** Senior procurement team oversight

#### Operational (40% of suppliers)
- **Characteristics:** High expenditure, competitive market, multiple alternatives
- **Strategy:** Performance optimization, competitive sourcing
- **Management:** Category management approach

#### Transactional (40% of suppliers)
- **Characteristics:** Low risk, many alternatives, easy switching
- **Strategy:** Cost optimization, efficiency focus, e-procurement
- **Management:** Automated processing, minimal touch

## 📈 Results & Impact

### Quantified Outcomes:
- **1,000+ suppliers successfully classified** across all business units
- **Balanced distribution achieved:** Strategic (4%), Critical (9%), Operational (30%), Transactional (55%)
- **Improved resource allocation:** Focus strategic management on top 13% of suppliers
- **Standardized framework:** Consistent evaluation methodology across business units

### Business Benefits:
- **Enhanced Supplier Strategy:** Clear differentiation between supplier tiers
- **Optimized Resource Allocation:** Focused management attention on high-value relationships
- **Risk Mitigation:** Systematic identification of critical supplier dependencies
- **Performance Measurement:** Standardized KPIs for supplier evaluation

### Segmentation Results by Business Unit:
```
Business Unit    Strategic  Critical  Operational  Transactional  Exit
Unit A             25        61         263          513          6
Unit B             10        23          48          109          8
Combined            7        16          26            2          3
Total              42       100         337          624         17
```

## 🔧 Technical Implementation

### Data Sources Integration:
- **Financial Systems:** Annual spend data, payment terms, cost trends
- **Procurement Systems:** Supplier master data, contract information
- **Risk Assessment:** Geographic risk, financial stability, operational metrics
- **Relationship Management:** Partnership scores, innovation assessments

### Automation Features:
- **Automated Data Collection:** Integration with ERP and procurement systems
- **Dynamic Scoring:** Real-time updates based on new data inputs
- **Alert System:** Notifications for supplier status changes
- **Reporting Dashboard:** Executive and operational reporting capabilities

### Validation & Quality Assurance:
- **Stakeholder Review:** Cross-functional validation of classification results
- **Sensitivity Analysis:** Testing of different weight configurations
- **Business Logic Validation:** Alignment with strategic business objectives
- **Continuous Improvement:** Quarterly review and methodology refinement

## 📁 Project Structure

```
02_Strategic_Supplier_Classification/
├── README.md                    # This documentation
├── methodology/
│   ├── scoring_algorithm.md     # Detailed algorithm explanation
│   ├── weight_optimization.md   # Business unit customization approach
│   └── validation_framework.md # Quality assurance methodology
├── sample_code/
│   ├── supplier_scoring_model.py    # Core algorithm implementation
│   ├── segmentation_analysis.py    # Classification and analysis logic
│   └── visualization_dashboard.py  # Results visualization
├── data_samples/
│   ├── sample_supplier_data.csv     # Anonymized sample dataset
│   └── scoring_results_example.csv # Example classification outputs
└── presentations/
    └── methodology_overview.pdf    # Executive summary presentation
```

## 🎯 Key Learnings

### Technical Skills Developed:
- **Mathematical Modeling:** Multi-criteria decision analysis and weighted scoring
- **Data Integration:** Combining quantitative metrics with qualitative assessments
- **Algorithm Design:** Scalable scoring system for large supplier populations
- **Business Intelligence:** Executive reporting and insight generation

### Business Insights:
- **Supplier Portfolio Management:** Importance of differentiated supplier strategies
- **Cross-functional Collaboration:** Working with procurement, finance, and operations teams
- **Change Management:** Implementing new classification methodology across organizations
- **Strategic Thinking:** Balancing current performance with future potential

### Methodology Innovation:
- **Adaptive Weighting:** Customizing evaluation criteria by business context
- **Holistic Assessment:** Combining financial, operational, and strategic factors
- **Scalable Framework:** Methodology applicable to diverse supplier populations
- **Continuous Improvement:** Built-in mechanisms for ongoing refinement

