"""
Supply Chain Analytics - Visualization Logic
Demonstrates dashboard visualization capabilities equivalent to Spotfire implementation

This example shows how to create interactive visualizations for supply chain monitoring
and trend analysis using Python libraries.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Set style for better-looking plots
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

class SupplyChainVisualizer:
    """
    A class for creating supply chain analytics visualizations
    Replicates the functionality shown in the original Spotfire dashboard
    """
    
    def __init__(self, data):
        self.data = data
        self.fig_size = (12, 8)
        
    def create_overall_trend_chart(self, save_path=None):
        """
        Create overall EHM trend analysis chart (equivalent to main dashboard view)
        """
        # Group data by date and priority level
        daily_trends = self.data.groupby(['Date', 'Priority_Level'])['Tracking_Count'].sum().reset_index()
        daily_pivot = daily_trends.pivot(index='Date', columns='Priority_Level', values='Tracking_Count').fillna(0)
        
        # Create stacked area chart
        fig = plt.figure(figsize=self.fig_size)
        ax = fig.add_subplot(111)
        
        # Stacked area plot
        daily_pivot.plot.area(ax=ax, alpha=0.7, stacked=True)
        
        ax.set_title('Overall Trend Analysis by Date', fontsize=16, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Count (Tracking ID)', fontsize=12)
        ax.legend(title='Priority Level', bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig
    
    def create_market_analysis_chart(self, save_path=None):
        """
        Create market-wise trend analysis (equivalent to "Trend Analysis by Market" tab)
        """
        # Group by market and date
        market_trends = self.data.groupby(['Date', 'Market'])['Tracking_Count'].sum().reset_index()
        
        # Create subplot for each market
        markets = self.data['Market'].unique()
        n_markets = len(markets)
        cols = 3
        rows = (n_markets + cols - 1) // cols
        
        fig, axes = plt.subplots(rows, cols, figsize=(15, 4*rows))
        axes = axes.flatten() if n_markets > 1 else [axes]
        
        for i, market in enumerate(markets):
            market_data = market_trends[market_trends['Market'] == market]
            
            if i < len(axes):
                ax = axes[i]
                ax.plot(market_data['Date'], market_data['Tracking_Count'], 
                       linewidth=2, marker='o', markersize=4)
                ax.set_title(f'{market}', fontweight='bold')
                ax.set_xlabel('Date')
                ax.set_ylabel('Count')
                ax.grid(True, alpha=0.3)
                ax.tick_params(axis='x', rotation=45)
        
        # Hide unused subplots
        for i in range(n_markets, len(axes)):
            axes[i].set_visible(False)
        
        plt.suptitle('Trend Analysis by Market', fontsize=16, fontweight='bold')
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig
    
    def create_planner_performance_dashboard(self, save_path=None):
        """
        Create planner performance analysis (equivalent to "Current tab for Individual")
        """
        # Calculate planner metrics
        planner_metrics = self.data.groupby('Planner').agg({
            'Tracking_Count': 'sum',
            'Planning_Delay_Days': 'mean',
            'Supply_Risk_Score': 'mean'
        }).round(2)
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # 1. Pie chart by planner (tracking count)
        top_planners = planner_metrics['Tracking_Count'].nlargest(8)
        other_sum = planner_metrics['Tracking_Count'].sum() - top_planners.sum()
        
        if other_sum > 0:
            plot_data = list(top_planners.values) + [other_sum]
            plot_labels = list(top_planners.index) + ['Others']
        else:
            plot_data = top_planners.values
            plot_labels = top_planners.index
        
        axes[0,0].pie(plot_data, labels=plot_labels, autopct='%1.1f%%', startangle=90)
        axes[0,0].set_title('Distribution by Planner', fontweight='bold')
        
        # 2. Planning delay trend
        delay_trend = self.data.groupby('Date')['Planning_Delay_Days'].mean()
        axes[0,1].plot(delay_trend.index, delay_trend.values, linewidth=2, color='orange')
        axes[0,1].set_title('Average Planning Delay Trend', fontweight='bold')
        axes[0,1].set_ylabel('Average Delay (Days)')
        axes[0,1].grid(True, alpha=0.3)
        
        # 3. Risk score distribution
        self.data['Supply_Risk_Score'].hist(bins=20, ax=axes[1,0], alpha=0.7, color='red')
        axes[1,0].set_title('Supply Risk Score Distribution', fontweight='bold')
        axes[1,0].set_xlabel('Risk Score')
        axes[1,0].set_ylabel('Frequency')
        
        # 4. Top materials treemap simulation (using bar chart)
        top_materials = self.data.groupby('Material_ID')['Tracking_Count'].sum().nlargest(10)
        top_materials.plot(kind='barh', ax=axes[1,1])
        axes[1,1].set_title('Top 10 Materials by Tracking Count', fontweight='bold')
        axes[1,1].set_xlabel('Tracking Count')
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig
    
    def create_interactive_plotly_dashboard(self):
        """
        Create interactive Plotly dashboard (modern equivalent to Spotfire)
        """
        # Prepare data for interactive charts
        daily_trends = self.data.groupby(['Date', 'Priority_Level'])['Tracking_Count'].sum().reset_index()
        market_trends = self.data.groupby(['Date', 'Market'])['Tracking_Count'].sum().reset_index()
        
        # Create subplot figure
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Overall Trend by Priority Level', 'Market Trends', 
                          'Planning Delay Distribution', 'Risk vs Tracking Volume'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # 1. Overall trend with priority levels
        for priority in sorted(daily_trends['Priority_Level'].unique()):
            priority_data = daily_trends[daily_trends['Priority_Level'] == priority]
            fig.add_trace(
                go.Scatter(x=priority_data['Date'], y=priority_data['Tracking_Count'],
                          mode='lines+markers', name=f'Priority {priority}',
                          stackgroup='one'),
                row=1, col=1
            )
        
        # 2. Market trends
        for market in market_trends['Market'].unique():
            market_data = market_trends[market_trends['Market'] == market]
            fig.add_trace(
                go.Scatter(x=market_data['Date'], y=market_data['Tracking_Count'],
                          mode='lines', name=market, visible='legendonly'),
                row=1, col=2
            )
        
        # 3. Planning delay distribution
        fig.add_trace(
            go.Histogram(x=self.data['Planning_Delay_Days'], name='Delay Distribution',
                        showlegend=False),
            row=2, col=1
        )
        
        # 4. Risk vs Volume scatter
        risk_volume = self.data.groupby('Material_ID').agg({
            'Supply_Risk_Score': 'mean',
            'Tracking_Count': 'sum'
        }).reset_index()
        
        fig.add_trace(
            go.Scatter(x=risk_volume['Supply_Risk_Score'], y=risk_volume['Tracking_Count'],
                      mode='markers', name='Materials',
                      marker=dict(size=8, opacity=0.6),
                      showlegend=False),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            title_text="Supply Chain Analytics Interactive Dashboard",
            title_x=0.5,
            height=700,
            showlegend=True
        )
        
        fig.update_xaxes(title_text="Date", row=1, col=1)
        fig.update_xaxes(title_text="Date", row=1, col=2)
        fig.update_xaxes(title_text="Planning Delay (Days)", row=2, col=1)
        fig.update_xaxes(title_text="Supply Risk Score", row=2, col=2)
        
        fig.update_yaxes(title_text="Count (Tracking ID)", row=1, col=1)
        fig.update_yaxes(title_text="Count (Tracking ID)", row=1, col=2)
        fig.update_yaxes(title_text="Frequency", row=2, col=1)
        fig.update_yaxes(title_text="Tracking Count", row=2, col=2)
        
        return fig
    
    def create_alert_monitoring_chart(self, alerts_data, save_path=None):
        """
        Create alert monitoring visualization
        """
        if not alerts_data:
            print("No alerts to visualize")
            return None
        
        # Prepare alert data for visualization
        alert_types = [alert['Alert_Type'] for alert in alerts_data]
        alert_counts = [alert['Count'] for alert in alerts_data]
        
        # Create alert dashboard
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Alert counts bar chart
        bars = ax1.bar(alert_types, alert_counts, color=['red', 'orange', 'yellow'])
        ax1.set_title('Active Alerts by Type', fontweight='bold', fontsize=14)
        ax1.set_ylabel('Count')
        ax1.tick_params(axis='x', rotation=45)
        
        # Add count labels on bars
        for bar, count in zip(bars, alert_counts):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{count}', ha='center', va='bottom', fontweight='bold')
        
        # Alert severity pie chart
        severity_colors = ['red', 'orange', 'yellow']
        ax2.pie(alert_counts, labels=alert_types, autopct='%1.1f%%', 
                colors=severity_colors, startangle=90)
        ax2.set_title('Alert Distribution', fontweight='bold', fontsize=14)
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig

def demonstrate_visualizations():
    """
    Demonstrate all visualization capabilities
    """
    # Import the data processor
    from data_processing_example import SupplyChainAnalyzer
    
    print("Supply Chain Analytics - Visualization Demonstration")
    print("=" * 60)
    
    # Generate and process sample data
    analyzer = SupplyChainAnalyzer()
    data = analyzer.generate_sample_data(1000)
    processed_data = analyzer.clean_and_process_data()
    alerts = analyzer.identify_outliers_and_alerts()
    
    # Initialize visualizer
    visualizer = SupplyChainVisualizer(processed_data)
    
    print("\n1. Creating Overall Trend Analysis Chart...")
    visualizer.create_overall_trend_chart()
    
    print("\n2. Creating Market Analysis Charts...")
    visualizer.create_market_analysis_chart()
    
    print("\n3. Creating Planner Performance Dashboard...")
    visualizer.create_planner_performance_dashboard()
    
    print("\n4. Creating Alert Monitoring Visualization...")
    visualizer.create_alert_monitoring_chart(alerts)
    
    print("\n5. Creating Interactive Plotly Dashboard...")
    interactive_fig = visualizer.create_interactive_plotly_dashboard()
    interactive_fig.show()
    
    print("\n" + "=" * 60)
    print("All visualizations completed successfully!")
    print("These charts replicate the functionality shown in the original Spotfire dashboard")

if __name__ == "__main__":
    demonstrate_visualizations()