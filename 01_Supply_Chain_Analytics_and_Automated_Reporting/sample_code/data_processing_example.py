"""
Supply Chain Analytics - Data Processing Example
Demonstrates data processing pipeline for component health monitoring analysis

This example shows how supply chain data would be processed and analyzed
for trend identification and automated reporting.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class SupplyChainAnalyzer:
    """
    A class for processing and analyzing supply chain component health data
    """
    
    def __init__(self):
        self.data = None
        self.processed_data = None
        
    def generate_sample_data(self, num_records=1000):
        """
        Generate sample supply chain data for demonstration
        """
        np.random.seed(42)
        
        # Date range for the analysis
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 12, 31)
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Sample data generation
        markets = ['AUTOMOTIVE', 'COMMUNICATIONS_EQUIPMENT', 'ENTERPRISE_SYSTEMS', 
                  'INDUSTRIAL', 'PERSONAL_ELECTRONICS']
        material_groups = ['WWMG', 'CCG']
        priority_levels = [2, 3, 4, 5]
        planners = [f'Planner_{i:02d}' for i in range(1, 21)]
        
        data = []
        
        for _ in range(num_records):
            record = {
                'Date': np.random.choice(date_range),
                'Market': np.random.choice(markets),
                'Material_Group': np.random.choice(material_groups),
                'Material_ID': f'MAT_{np.random.randint(10000, 99999)}',
                'Planner': np.random.choice(planners),
                'Priority_Level': np.random.choice(priority_levels),
                'Tracking_Count': np.random.poisson(15),
                'ESD_Planning_Status': np.random.choice(['On_Time', 'Late_7_days', 'Late_15_days', 'Late_30_days']),
                'Market_Max_Qty': np.random.exponential(100),
                'Supply_Risk_Score': np.random.uniform(1, 5)
            }
            data.append(record)
        
        self.data = pd.DataFrame(data)
        return self.data
    
    def clean_and_process_data(self):
        """
        Clean and process the raw supply chain data
        """
        if self.data is None:
            raise ValueError("No data to process. Please load data first.")
        
        df = self.data.copy()
        
        # Data cleaning
        df['Date'] = pd.to_datetime(df['Date'])
        df['Year_Month'] = df['Date'].dt.to_period('M')
        df['Week'] = df['Date'].dt.isocalendar().week
        
        # Create derived metrics
        df['Risk_Category'] = pd.cut(df['Supply_Risk_Score'], 
                                   bins=[0, 2, 3, 4, 5], 
                                   labels=['Low', 'Medium', 'High', 'Critical'])
        
        # Market Max Quantity categories
        df['Qty_Category'] = pd.cut(df['Market_Max_Qty'], 
                                  bins=[0, 50, 150, 300, float('inf')], 
                                  labels=['Small', 'Medium', 'Large', 'XLarge'])
        
        # ESD Planning delay in days
        esdmapping = {'On_Time': 0, 'Late_7_days': 7, 'Late_15_days': 15, 'Late_30_days': 30}
        df['Planning_Delay_Days'] = df['ESD_Planning_Status'].map(esdmapping)
        
        self.processed_data = df
        return df
    
    def calculate_trend_metrics(self):
        """
        Calculate key metrics for trend analysis
        """
        df = self.processed_data
        
        # Overall trend metrics by date
        daily_trends = df.groupby('Date').agg({
            'Tracking_Count': 'sum',
            'Priority_Level': 'mean',
            'Planning_Delay_Days': 'mean',
            'Supply_Risk_Score': 'mean'
        }).reset_index()
        
        # Market-wise analysis
        market_trends = df.groupby(['Date', 'Market']).agg({
            'Tracking_Count': 'sum',
            'Market_Max_Qty': 'sum'
        }).reset_index()
        
        # Material group analysis
        material_trends = df.groupby(['Year_Month', 'Material_Group']).agg({
            'Tracking_Count': 'sum',
            'Priority_Level': 'mean',
            'Planning_Delay_Days': 'mean'
        }).reset_index()
        
        # Planner performance metrics
        planner_performance = df.groupby('Planner').agg({
            'Tracking_Count': 'sum',
            'Planning_Delay_Days': 'mean',
            'Supply_Risk_Score': 'mean'
        }).round(2)
        
        return {
            'daily_trends': daily_trends,
            'market_trends': market_trends,
            'material_trends': material_trends,
            'planner_performance': planner_performance
        }
    
    def identify_outliers_and_alerts(self):
        """
        Identify outliers and generate alerts for follow-up
        """
        df = self.processed_data
        
        # Define alert conditions
        alerts = []
        
        # High delay alerts
        high_delay = df[df['Planning_Delay_Days'] > 15]
        if not high_delay.empty:
            alerts.append({
                'Alert_Type': 'High_Planning_Delay',
                'Count': len(high_delay),
                'Affected_Planners': high_delay['Planner'].unique().tolist()
            })
        
        # High risk score alerts
        high_risk = df[df['Supply_Risk_Score'] > 4.0]
        if not high_risk.empty:
            alerts.append({
                'Alert_Type': 'High_Supply_Risk',
                'Count': len(high_risk),
                'Affected_Materials': high_risk['Material_ID'].unique()[:10].tolist()
            })
        
        # Low tracking volume (potential issues)
        daily_tracking = df.groupby('Date')['Tracking_Count'].sum()
        low_tracking_days = daily_tracking[daily_tracking < daily_tracking.quantile(0.1)]
        
        if not low_tracking_days.empty:
            alerts.append({
                'Alert_Type': 'Low_Tracking_Volume',
                'Count': len(low_tracking_days),
                'Dates': low_tracking_days.index.strftime('%Y-%m-%d').tolist()
            })
        
        return alerts
    
    def generate_top_rankings(self):
        """
        Generate top rankings for materials, planners, and markets
        """
        df = self.processed_data
        
        # Top 10 materials by tracking count
        top_materials = df.groupby('Material_ID')['Tracking_Count'].sum().nlargest(10)
        
        # Top planners by volume handled
        top_planners = df.groupby('Planner')['Tracking_Count'].sum().nlargest(10)
        
        # Market distribution
        market_distribution = df.groupby('Market')['Tracking_Count'].sum().sort_values(ascending=False)
        
        return {
            'top_materials': top_materials,
            'top_planners': top_planners,
            'market_distribution': market_distribution
        }

def main():
    """
    Main execution function demonstrating the analysis pipeline
    """
    print("Supply Chain Analytics - Data Processing Pipeline")
    print("=" * 55)
    
    # Initialize analyzer
    analyzer = SupplyChainAnalyzer()
    
    # Step 1: Generate sample data
    print("\n1. Generating sample supply chain data...")
    data = analyzer.generate_sample_data(1000)
    print(f"Generated {len(data)} records")
    print("\nSample data preview:")
    print(data.head())
    
    # Step 2: Clean and process data
    print("\n2. Processing and cleaning data...")
    processed_data = analyzer.clean_and_process_data()
    print("Data processing completed")
    print(f"Data shape: {processed_data.shape}")
    
    # Step 3: Calculate trend metrics
    print("\n3. Calculating trend metrics...")
    metrics = analyzer.calculate_trend_metrics()
    print("Key metrics calculated:")
    print(f"- Daily trends: {len(metrics['daily_trends'])} data points")
    print(f"- Market trends: {len(metrics['market_trends'])} data points")
    print(f"- Planner performance: {len(metrics['planner_performance'])} planners")
    
    # Step 4: Identify alerts
    print("\n4. Identifying alerts and outliers...")
    alerts = analyzer.identify_outliers_and_alerts()
    print(f"Generated {len(alerts)} alert types:")
    for alert in alerts:
        print(f"- {alert['Alert_Type']}: {alert['Count']} items")
    
    # Step 5: Generate rankings
    print("\n5. Generating top rankings...")
    rankings = analyzer.generate_top_rankings()
    print("Top 5 Materials by Tracking Count:")
    print(rankings['top_materials'].head())
    
    print("\nTop 5 Planners by Volume:")
    print(rankings['top_planners'].head())
    
    print("\nMarket Distribution:")
    print(rankings['market_distribution'])
    
    print("\n" + "=" * 55)
    print("Analysis pipeline completed successfully!")
    
    return analyzer, metrics, alerts, rankings

if __name__ == "__main__":
    analyzer, metrics, alerts, rankings = main()