import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Set visualization style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("Set2")

class SupplierVisualizationDashboard:
    """
    Comprehensive visualization suite for supplier segmentation analysis
    """
    
    def __init__(self, suppliers_data):
        self.data = suppliers_data
        self.segment_colors = {
            'Strategic': '#FF6B6B',      # Red
            'Critical': '#4ECDC4',       # Teal  
            'Operational': '#45B7D1',    # Blue
            'Transactional': '#96CEB4'   # Green
        }
    
    def create_segmentation_overview(self, save_path=None):
        """
        Create overview dashboard with key segmentation metrics
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # 1. Segment Distribution Pie Chart
        segment_counts = self.data['Classification'].value_counts()
        colors = [self.segment_colors[seg] for seg in segment_counts.index]
        
        axes[0,0].pie(segment_counts.values, labels=segment_counts.index, 
                     autopct='%1.1f%%', colors=colors, startangle=90)
        axes[0,0].set_title('Supplier Distribution by Segment', fontweight='bold', fontsize=12)
        
        # 2. Score Distribution by Segment
        for segment in self.segment_colors:
            segment_data = self.data[self.data['Classification'] == segment]
            if not segment_data.empty:
                axes[0,1].hist(segment_data['Score'], alpha=0.6, 
                              label=segment, color=self.segment_colors[segment], bins=15)
        axes[0,1].set_xlabel('Score')
        axes[0,1].set_ylabel('Frequency')
        axes[0,1].set_title('Score Distribution by Segment', fontweight='bold', fontsize=12)
        axes[0,1].legend()
        
        # 3. Spend Concentration by Segment
        spend_by_segment = self.data.groupby('Classification')['Annual_Spend'].sum()
        spend_by_segment = spend_by_segment.reindex(['Strategic', 'Critical', 'Operational', 'Transactional'])
        colors_ordered = [self.segment_colors[seg] for seg in spend_by_segment.index]
        
        bars = axes[1,0].bar(spend_by_segment.index, spend_by_segment.values, color=colors_ordered)
        axes[1,0].set_title('Total Spend by Segment', fontweight='bold', fontsize=12)
        axes[1,0].set_ylabel('Total Annual Spend (K)')
        axes[1,0].tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            axes[1,0].text(bar.get_x() + bar.get_width()/2., height,
                          f'{height/1000:.0f}K', ha='center', va='bottom')
        
        # 4. Business Unit Distribution
        bu_segment = pd.crosstab(self.data['Business_Unit'], self.data['Classification'])
        bu_segment.plot(kind='bar', stacked=True, ax=axes[1,1], 
                       color=[self.segment_colors[col] for col in bu_segment.columns])
        axes[1,1].set_title('Segment Distribution by Business Unit', fontweight='bold', fontsize=12)
        axes[1,1].set_xlabel('Business Unit')
        axes[1,1].set_ylabel('Number of Suppliers')
        axes[1,1].tick_params(axis='x', rotation=45)
        axes[1,1].legend(title='Segment')
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig
    
    def create_risk_analysis_dashboard(self, save_path=None):
        """
        Create risk analysis visualization dashboard
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # 1. Risk Score Distribution by Segment
        risk_pivot = self.data.groupby(['Classification', 'Supply_Risk_Score']).size().unstack(fill_value=0)
        risk_pivot.plot(kind='bar', stacked=True, ax=axes[0,0], 
                       color=['lightgreen', 'orange', 'red'])
        axes[0,0].set_title('Supply Risk Distribution by Segment', fontweight='bold')
        axes[0,0].set_xlabel('Segment')
        axes[0,0].set_ylabel('Number of Suppliers')
        axes[0,0].legend(title='Risk Score', labels=['Low (1)', 'Medium (2)', 'High (3)'])
        axes[0,0].tick_params(axis='x', rotation=45)
        
        # 2. Risk vs Spend Scatter Plot
        scatter_colors = [self.segment_colors[seg] for seg in self.data['Classification']]
        scatter = axes[0,1].scatter(self.data['Supply_Risk_Score'], self.data['Annual_Spend'], 
                                   c=scatter_colors, alpha=0.6, s=50)
        axes[0,1].set_xlabel('Supply Risk Score')
        axes[0,1].set_ylabel('Annual Spend (K)')
        axes[0,1].set_title('Risk vs Spend Analysis', fontweight='bold')
        axes[0,1].set_yscale('log')
        
        # 3. Sole Source Dependency Analysis
        sole_source_data = self.data[self.data['Sole_Source_Parts'] > 0]
        sole_source_by_segment = sole_source_data['Classification'].value_counts()
        colors = [self.segment_colors[seg] for seg in sole_source_by_segment.index]
        
        axes[1,0].bar(sole_source_by_segment.index, sole_source_by_segment.values, color=colors)
        axes[1,0].set_title('Sole Source Suppliers by Segment', fontweight='bold')
        axes[1,0].set_ylabel('Number of Suppliers')
        axes[1,0].tick_params(axis='x', rotation=45)
        
        # 4. Risk Heat Map
        risk_heatmap = self.data.groupby(['Classification', 'Supply_Risk_Score']).size().unstack(fill_value=0)
        risk_heatmap_pct = risk_heatmap.div(risk_heatmap.sum(axis=1), axis=0) * 100
        
        sns.heatmap(risk_heatmap_pct, annot=True, fmt='.1f', cmap='Reds', 
                   ax=axes[1,1], cbar_kws={'label': 'Percentage'})
        axes[1,1].set_title('Risk Distribution Heatmap (%)', fontweight='bold')
        axes[1,1].set_xlabel('Risk Score')
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig
    
    def create_strategic_insights_chart(self, save_path=None):
        """
        Create strategic insights visualization
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # 1. Partnership vs Innovation Matrix
        partnership_innovation = self.data.groupby(['Partnership_Score', 'Innovation_Score']).size().unstack(fill_value=0)
        sns.heatmap(partnership_innovation, annot=True, fmt='d', cmap='Blues', ax=axes[0,0])
        axes[0,0].set_title('Partnership vs Innovation Matrix', fontweight='bold')
        axes[0,0].set_xlabel('Innovation Score')
        axes[0,0].set_ylabel('Partnership Score')
        
        # 2. Ramp Time Analysis by Segment
        ramp_time_data = []
        segments = []
        for segment in ['Strategic', 'Critical', 'Operational', 'Transactional']:
            segment_data = self.data[self.data['Classification'] == segment]
            if not segment_data.empty:
                ramp_time_data.extend(segment_data['Ramp_Time_Months'].tolist())
                segments.extend([segment] * len(segment_data))
        
        ramp_df = pd.DataFrame({'Segment': segments, 'Ramp_Time': ramp_time_data})
        sns.boxplot(data=ramp_df, x='Segment', y='Ramp_Time', ax=axes[0,1])
        axes[0,1].set_title('Ramp Time Distribution by Segment', fontweight='bold')
        axes[0,1].tick_params(axis='x', rotation=45)
        
        # 3. Spend Pareto Analysis
        sorted_data = self.data.sort_values('Annual_Spend', ascending=False)
        sorted_data['cumulative_spend'] = sorted_data['Annual_Spend'].cumsum()
        total_spend = sorted_data['Annual_Spend'].sum()
        sorted_data['cumulative_pct'] = sorted_data['cumulative_spend'] / total_spend * 100
        
        x_range = range(1, min(101, len(sorted_data) + 1))
        y_cumulative = sorted_data['cumulative_pct'].iloc[:100] if len(sorted_data) >= 100 else sorted_data['cumulative_pct']
        
        axes[1,0].plot(x_range[:len(y_cumulative)], y_cumulative, 'b-', linewidth=2)
        axes[1,0].axhline(y=80, color='r', linestyle='--', label='80% Line')
        axes[1,0].set_xlabel('Number of Suppliers (Ranked by Spend)')
        axes[1,0].set_ylabel('Cumulative Spend %')
        axes[1,0].set_title('Spend Concentration (Pareto Analysis)', fontweight='bold')
        axes[1,0].legend()
        axes[1,0].grid(True, alpha=0.3)
        
        # 4. Segment Score Comparison
        segment_stats = self.data.groupby('Classification')['Score'].agg(['mean', 'std']).fillna(0)
        segment_stats = segment_stats.reindex(['Strategic', 'Critical', 'Operational', 'Transactional'])
        
        x_pos = range(len(segment_stats))
        axes[1,1].bar(x_pos, segment_stats['mean'], 
                     yerr=segment_stats['std'], capsize=5,
                     color=[self.segment_colors[seg] for seg in segment_stats.index])
        axes[1,1].set_xlabel('Segment')
        axes[1,1].set_ylabel('Average Score')
        axes[1,1].set_title('Average Score by Segment (±1 Std Dev)', fontweight='bold')
        axes[1,1].set_xticks(x_pos)
        axes[1,1].set_xticklabels(segment_stats.index, rotation=45)
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig
    
    def create_interactive_plotly_dashboard(self):
        """
        Create interactive Plotly dashboard
        """
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Segment Distribution', 'Score vs Spend by Segment', 
                          'Risk Analysis', 'Innovation vs Partnership'),
            specs=[[{"type": "pie"}, {"type": "scatter"}],
                   [{"type": "bar"}, {"type": "scatter"}]]
        )
        
        # 1. Segment Distribution Pie Chart
        segment_counts = self.data['Classification'].value_counts()
        fig.add_trace(
            go.Pie(labels=segment_counts.index, values=segment_counts.values,
                  marker_colors=[self.segment_colors[seg] for seg in segment_counts.index],
                  name="Segments"),
            row=1, col=1
        )
        
        # 2. Score vs Spend Scatter
        for segment in self.segment_colors:
            segment_data = self.data[self.data['Classification'] == segment]
            if not segment_data.empty:
                fig.add_trace(
                    go.Scatter(x=segment_data['Score'], y=segment_data['Annual_Spend'],
                              mode='markers', name=segment,
                              marker=dict(color=self.segment_colors[segment], size=8),
                              showlegend=False),
                    row=1, col=2
                )
        
        # 3. Risk Analysis Bar Chart
        risk_counts = self.data.groupby(['Classification', 'Supply_Risk_Score']).size().reset_index(name='count')
        for risk_score in [1, 2, 3]:
            risk_data = risk_counts[risk_counts['Supply_Risk_Score'] == risk_score]
            fig.add_trace(
                go.Bar(x=risk_data['Classification'], y=risk_data['count'],
                      name=f'Risk {risk_score}', showlegend=False),
                row=2, col=1
            )
        
        # 4. Innovation vs Partnership Scatter
        fig.add_trace(
            go.Scatter(x=self.data['Innovation_Score'], y=self.data['Partnership_Score'],
                      mode='markers', 
                      marker=dict(color=[self.segment_colors[seg] for seg in self.data['Classification']],
                                size=10, opacity=0.6),
                      name='Suppliers', showlegend=False),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            title_text="Interactive Supplier Segmentation Dashboard",
            title_x=0.5,
            height=800,
            showlegend=True
        )
        
        # Update axes labels
        fig.update_xaxes(title_text="Score", row=1, col=2)
        fig.update_yaxes(title_text="Annual Spend (K)", row=1, col=2)
        fig.update_xaxes(title_text="Segment", row=2, col=1)
        fig.update_yaxes(title_text="Count", row=2, col=1)
        fig.update_xaxes(title_text="Innovation Score", row=2, col=2)
        fig.update_yaxes(title_text="Partnership Score", row=2, col=2)
        
        return fig
    
    def generate_executive_summary_chart(self, save_path=None):
        """
        Create executive summary visualization
        """
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        
        # Key metrics summary
        total_suppliers = len(self.data)
        total_spend = self.data['Annual_Spend'].sum()
        
        segment_summary = self.data.groupby('Classification').agg({
            'Annual_Spend': ['sum', 'count'],
            'Score': 'mean'
        }).round(2)
        
        segment_summary.columns = ['Total_Spend', 'Supplier_Count', 'Avg_Score']
        segment_summary['Spend_Share'] = segment_summary['Total_Spend'] / total_spend * 100
        segment_summary['Supplier_Share'] = segment_summary['Supplier_Count'] / total_suppliers * 100
        
        # Create bubble chart
        x = segment_summary['Supplier_Share']
        y = segment_summary['Spend_Share']
        sizes = segment_summary['Avg_Score'] * 50
        colors = [self.segment_colors[seg] for seg in segment_summary.index]
        
        scatter = ax.scatter(x, y, s=sizes, c=colors, alpha=0.7, edgecolors='black', linewidth=2)
        
        # Add labels
        for i, segment in enumerate(segment_summary.index):
            ax.annotate(segment, (x.iloc[i], y.iloc[i]), 
                       xytext=(5, 5), textcoords='offset points',
                       fontweight='bold', fontsize=11)
        
        ax.set_xlabel('Percentage of Suppliers (%)', fontsize=12)
        ax.set_ylabel('Percentage of Total Spend (%)', fontsize=12)
        ax.set_title('Strategic Supplier Portfolio Overview\n(Bubble size = Average Score)', 
                    fontweight='bold', fontsize=14)
        ax.grid(True, alpha=0.3)
        
        # Add quadrant lines
        ax.axhline(y=50, color='gray', linestyle='--', alpha=0.5)
        ax.axvline(x=50, color='gray', linestyle='--', alpha=0.5)
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig

def demonstrate_visualizations():
    """
    Demonstrate all visualization capabilities
    """
    print("Supplier Segmentation Visualization Demo")
    print("=" * 45)
    
    # Import data
    from supplier_scoring_model import SupplierScoringModel
    
    model = SupplierScoringModel()
    data = model.generate_sample_supplier_data(1000)
    classified_data = model.classify_suppliers()
    
    # Initialize dashboard
    dashboard = SupplierVisualizationDashboard(classified_data)
