"""
Strategic Supplier Classification - Scoring Model Implementation
Replicates the weighted scoring algorithm used for supplier segmentation

This implementation demonstrates the mathematical model used to classify
1,120+ suppliers across multiple business units with customized weighting schemes.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class SupplierScoringModel:
    """
    Implementation of the strategic supplier classification scoring algorithm
    """
    
    def __init__(self):
        self.suppliers_data = None
        self.scores = None
        self.classifications = None
        
        # Define business unit weights based on methodology
        self.bu_weights = {
            'Business_Unit_A': {
                'W0': 100,  # BU Scale factor
                'W2': 30,   # Sole source weight
                'W3': 20,   # Single source weight  
                'W4': 1,    # Multi source weight
                'W5': 25,   # Ramp time weight
                'W6': 10,   # Spend weight
                'W7': 25,   # Partnership weight
                'W8': 5,    # Innovation weight
                'W9': 5     # Supply risk weight
            },
            'Business_Unit_B': {
                'W0': 100,
                'W2': 5,    # Lower dependency focus
                'W3': 5,
                'W4': 1,
                'W5': 20,   # Faster ramp requirements
                'W6': 10,
                'W7': 25,
                'W8': 10,   # Higher innovation focus
                'W9': 20    # Higher risk sensitivity
            }
        }
        
        # Segmentation thresholds (percentiles)
        self.segmentation_thresholds = {
            'Strategic': 95,     # Top 5%
            'Critical': 85,      # Next 10% (85-95%)
            'Operational': 45,   # Next 40% (45-85%)
            'Transactional': 0   # Bottom 40% (0-45%)
        }
    
    def generate_sample_supplier_data(self, n_suppliers=1000):
        """
        Generate realistic supplier data for demonstration purposes
        """
        np.random.seed(42)
        
        business_units = ['Business_Unit_A', 'Business_Unit_B']
        bu_weights = [0.75, 0.25]  # Approximate distribution
        
        suppliers = []
        
        for i in range(n_suppliers):
            supplier_id = f"SUP_{i+1:04d}"
            business_unit = np.random.choice(business_units, p=bu_weights)
            
            # Generate supplier characteristics
            supplier = {
                'Supplier_ID': supplier_id,
                'Business_Unit': business_unit,
                'Annual_Spend': np.random.lognormal(mean=12, sigma=1.5),  # Spend in thousands
                'Sole_Source_Parts': np.random.poisson(2),
                'Single_Source_Parts': np.random.poisson(5),
                'Multi_Source_Parts': np.random.poisson(15),
                'Ramp_Time_Months': np.random.choice([3, 6, 9, 12, 18, 24], 
                                                   p=[0.1, 0.3, 0.25, 0.2, 0.1, 0.05]),
                'Partnership_Score': np.random.choice([1, 2, 3], p=[0.2, 0.6, 0.2]),  # 1=Poor, 2=Good, 3=Excellent
                'Innovation_Score': np.random.choice([1, 2, 3], p=[0.3, 0.5, 0.2]),   # 1=Low, 2=Medium, 3=High
                'Supply_Risk_Score': np.random.choice([1, 2, 3], p=[0.4, 0.4, 0.2])   # 1=Low, 2=Medium, 3=High
            }
            
            # Calculate derived metrics
            total_parts = supplier['Sole_Source_Parts'] + supplier['Single_Source_Parts'] + supplier['Multi_Source_Parts']
            supplier['Sole_Source_Ratio'] = supplier['Sole_Source_Parts'] / max(total_parts, 1)
            supplier['Single_Source_Ratio'] = supplier['Single_Source_Parts'] / max(total_parts, 1)
            supplier['Multi_Source_Ratio'] = supplier['Multi_Source_Parts'] / max(total_parts, 1)
            
            suppliers.append(supplier)
        
        self.suppliers_data = pd.DataFrame(suppliers)
        return self.suppliers_data
    
    def calculate_supplier_score(self, supplier_row, business_unit):
        """
        Calculate supplier score using the weighted algorithm
        """
        weights = self.bu_weights[business_unit]
        
        # BU Impact factor (simplified as constant for this example)
        bu_impact = weights['W0'] / 100
        bu_scale = 1.0  # Normalized scale factor
        
        # Part sourcing components
        sourcing_component = (
            weights['W2'] * supplier_row['Sole_Source_Ratio'] +
            weights['W3'] * supplier_row['Single_Source_Ratio'] + 
            weights['W4'] * supplier_row['Multi_Source_Ratio']
        ) / 100
        
        # Ramp time component (normalized)
        ramp_component = weights['W5'] * (1 - 1 / (1 + (supplier_row['Ramp_Time_Months'] / 12) ** 2)) / 100
        
        # Spend component (normalized)
        spend_component = weights['W6'] * (1 - 1 / (1 + supplier_row['Annual_Spend'] / 100)) / 100
        
        # Partnership component
        partnership_component = weights['W7'] * (supplier_row['Partnership_Score'] / 3) / 100
        
        # Innovation component  
        innovation_component = weights['W8'] * (supplier_row['Innovation_Score'] / 3) / 100
        
        # Supply risk component (inverted - lower risk = higher score)
        risk_component = weights['W9'] * ((4 - supplier_row['Supply_Risk_Score']) / 3) / 100
        
        # Total score calculation
        total_score = bu_impact * bu_scale * (
            sourcing_component + ramp_component + spend_component + 
            partnership_component + innovation_component + risk_component
        )
        
        return total_score * 100  # Scale to 0-100 range
    
    def classify_suppliers(self):
        """
        Calculate scores and classify all suppliers
        """
        if self.suppliers_data is None:
            raise ValueError("No supplier data available. Please generate or load data first.")
        
        # Calculate scores for each supplier
        scores = []
        for idx, supplier in self.suppliers_data.iterrows():
            score = self.calculate_supplier_score(supplier, supplier['Business_Unit'])
            scores.append(score)
        
        self.suppliers_data['Score'] = scores
        
        # Classify suppliers based on score percentiles
        classifications = []
        for score in scores:
            percentile = (self.suppliers_data['Score'] <= score).mean() * 100
            
            if percentile >= self.segmentation_thresholds['Strategic']:
                classification = 'Strategic'
            elif percentile >= self.segmentation_thresholds['Critical']:
                classification = 'Critical'
            elif percentile >= self.segmentation_thresholds['Operational']:
                classification = 'Operational'
            else:
                classification = 'Transactional'
            
            classifications.append(classification)
        
        self.suppliers_data['Classification'] = classifications
        return self.suppliers_data
    
    def analyze_segmentation_results(self):
        """
        Analyze and summarize segmentation results
        """
        if self.suppliers_data is None or 'Classification' not in self.suppliers_data.columns:
            raise ValueError("Suppliers must be classified first.")
        
        # Overall distribution
        overall_dist = self.suppliers_data['Classification'].value_counts().sort_index()
        overall_pct = (overall_dist / len(self.suppliers_data) * 100).round(1)
        
        print("Overall Supplier Segmentation Results:")
        print("=" * 45)
        for category in ['Strategic', 'Critical', 'Operational', 'Transactional']:
            count = overall_dist.get(category, 0)
            pct = overall_pct.get(category, 0.0)
            print(f"{category:15}: {count:4d} suppliers ({pct:4.1f}%)")
        
        # Business Unit breakdown
        print(f"\nTotal Suppliers Classified: {len(self.suppliers_data)}")
        print("\nBusiness Unit Breakdown:")
        print("=" * 35)
        
        bu_breakdown = self.suppliers_data.groupby(['Business_Unit', 'Classification']).size().unstack(fill_value=0)
        print(bu_breakdown)
        
        # Score statistics
        print(f"\nScore Statistics:")
        print("=" * 20)
        print(f"Mean Score: {self.suppliers_data['Score'].mean():.2f}")
        print(f"Std Dev:    {self.suppliers_data['Score'].std():.2f}")
        print(f"Min Score:  {self.suppliers_data['Score'].min():.2f}")
        print(f"Max Score:  {self.suppliers_data['Score'].max():.2f}")
        
        return {
            'overall_distribution': overall_dist,
            'bu_breakdown': bu_breakdown,
            'score_stats': self.suppliers_data['Score'].describe()
        }
    
    def identify_top_suppliers(self, n_top=20):
        """
        Identify top suppliers by classification and score
        """
        top_suppliers = self.suppliers_data.nlargest(n_top, 'Score')[
            ['Supplier_ID', 'Business_Unit', 'Classification', 'Score', 'Annual_Spend', 
             'Partnership_Score', 'Innovation_Score', 'Supply_Risk_Score']
        ].round(2)
        
        print(f"\nTop {n_top} Suppliers by Score:")
        print("=" * 50)
        print(top_suppliers.to_string(index=False))
        
        return top_suppliers
    
    def analyze_classification_drivers(self):
        """
        Analyze what drives different classifications
        """
        classification_analysis = self.suppliers_data.groupby('Classification').agg({
            'Score': ['mean', 'std'],
            'Annual_Spend': 'mean',
            'Ramp_Time_Months': 'mean',
            'Partnership_Score': 'mean',
            'Innovation_Score': 'mean',
            'Supply_Risk_Score': 'mean',
            'Sole_Source_Ratio': 'mean'
        }).round(2)
        
        print("\nClassification Driver Analysis:")
        print("=" * 40)
        print(classification_analysis)
        
        return classification_analysis
    
    def create_segmentation_visualization(self):
        """
        Create visualizations of segmentation results
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Overall distribution pie chart
        classification_counts = self.suppliers_data['Classification'].value_counts()
        colors = ['gold', 'lightcoral', 'lightblue', 'lightgreen']
        axes[0,0].pie(classification_counts.values, labels=classification_counts.index, 
                     autopct='%1.1f%%', colors=colors, startangle=90)
        axes[0,0].set_title('Supplier Classification Distribution', fontweight='bold')
        
        # 2. Score distribution by classification
        for classification in ['Strategic', 'Critical', 'Operational', 'Transactional']:
            subset = self.suppliers_data[self.suppliers_data['Classification'] == classification]
            if not subset.empty:
                axes[0,1].hist(subset['Score'], alpha=0.6, label=classification, bins=20)
        axes[0,1].set_xlabel('Score')
        axes[0,1].set_ylabel('Frequency')
        axes[0,1].set_title('Score Distribution by Classification', fontweight='bold')
        axes[0,1].legend()
        
        # 3. Business unit breakdown
        bu_breakdown = pd.crosstab(self.suppliers_data['Business_Unit'], 
                                  self.suppliers_data['Classification'])
        bu_breakdown.plot(kind='bar', stacked=True, ax=axes[1,0], color=colors)
        axes[1,0].set_title('Classification by Business Unit', fontweight='bold')
        axes[1,0].set_xlabel('Business Unit')
        axes[1,0].set_ylabel('Number of Suppliers')
        axes[1,0].tick_params(axis='x', rotation=45)
        
        # 4. Score vs Annual Spend scatter
        scatter_colors = {'Strategic': 'gold', 'Critical': 'lightcoral', 
                         'Operational': 'lightblue', 'Transactional': 'lightgreen'}
        for classification in scatter_colors:
            subset = self.suppliers_data[self.suppliers_data['Classification'] == classification]
            if not subset.empty:
                axes[1,1].scatter(subset['Annual_Spend'], subset['Score'], 
                                c=scatter_colors[classification], label=classification, alpha=0.6)
        axes[1,1].set_xlabel('Annual Spend (thousands)')
        axes[1,1].set_ylabel('Score')
        axes[1,1].set_title('Score vs Annual Spend by Classification', fontweight='bold')
        axes[1,1].legend()
        axes[1,1].set_xscale('log')
        
        plt.tight_layout()
        plt.show()
        
        return fig

def main():
    """
    Main execution function demonstrating the supplier classification model
    """
    print("Strategic Supplier Classification Model")
    print("=" * 50)
    
    # Initialize the model
    model = SupplierScoringModel()
    
    # Generate sample data
    print("\n1. Generating sample supplier data...")
    suppliers = model.generate_sample_supplier_data(1000)
    print(f"Generated data for {len(suppliers)} suppliers")
    
    # Classify suppliers
    print("\n2. Calculating scores and classifying suppliers...")
    classified_suppliers = model.classify_suppliers()
    print("Classification completed")
    
    # Analyze results
    print("\n3. Analyzing segmentation results...")
    results = model.analyze_segmentation_results()
    
    # Identify top suppliers
    print("\n4. Identifying top suppliers...")
    top_suppliers = model.identify_top_suppliers(10)
    
    # Analyze classification drivers
    print("\n5. Analyzing classification drivers...")
    drivers = model.analyze_classification_drivers()
    
    # Create visualizations
    print("\n6. Creating segmentation visualizations...")
    model.create_segmentation_visualization()
    
    print("\n" + "=" * 50)
    print("Supplier classification analysis completed successfully!")
    
    return model, results, top_suppliers, drivers

if __name__ == "__main__":
    model, results, top_suppliers, drivers = main()