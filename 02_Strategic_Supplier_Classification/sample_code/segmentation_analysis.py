import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class SegmentationAnalyzer:
    """
    Advanced analytics for supplier segmentation results
    """
    
    def __init__(self, suppliers_data):
        self.data = suppliers_data
        self.analysis_results = {}
    
    def segment_profile_analysis(self):
        """
        Analyze characteristics of each supplier segment
        """
        segments = ['Strategic', 'Critical', 'Operational', 'Transactional']
        profiles = {}
        
        for segment in segments:
            segment_data = self.data[self.data['Classification'] == segment]
            
            if len(segment_data) > 0:
                profile = {
                    'count': len(segment_data),
                    'avg_score': segment_data['Score'].mean(),
                    'avg_spend': segment_data['Annual_Spend'].mean(),
                    'avg_ramp_time': segment_data['Ramp_Time_Months'].mean(),
                    'avg_partnership': segment_data['Partnership_Score'].mean(),
                    'avg_innovation': segment_data['Innovation_Score'].mean(),
                    'avg_risk': segment_data['Supply_Risk_Score'].mean(),
                    'sole_source_ratio': segment_data['Sole_Source_Ratio'].mean(),
                    'spend_concentration': segment_data['Annual_Spend'].sum() / self.data['Annual_Spend'].sum()
                }
                profiles[segment] = profile
        
        self.analysis_results['segment_profiles'] = profiles
        return profiles
    
    def business_unit_analysis(self):
        """
        Analyze segmentation patterns by business unit
        """
        bu_analysis = {}
        business_units = self.data['Business_Unit'].unique()
        
        for bu in business_units:
            bu_data = self.data[self.data['Business_Unit'] == bu]
            
            # Segment distribution
            segment_dist = bu_data['Classification'].value_counts(normalize=True) * 100
            
            # Key metrics
            metrics = {
                'total_suppliers': len(bu_data),
                'total_spend': bu_data['Annual_Spend'].sum(),
                'avg_score': bu_data['Score'].mean(),
                'segment_distribution': segment_dist.to_dict(),
                'strategic_spend_share': bu_data[bu_data['Classification'] == 'Strategic']['Annual_Spend'].sum() / bu_data['Annual_Spend'].sum() * 100
            }
            
            bu_analysis[bu] = metrics
        
        self.analysis_results['business_unit_analysis'] = bu_analysis
        return bu_analysis
    
    def risk_concentration_analysis(self):
        """
        Analyze supply risk concentration across segments
        """
        # High risk suppliers (risk score = 3)
        high_risk = self.data[self.data['Supply_Risk_Score'] == 3]
        
        # Sole source dependency analysis
        sole_source = self.data[self.data['Sole_Source_Parts'] > 0]
        
        risk_analysis = {
            'high_risk_by_segment': high_risk.groupby('Classification').size().to_dict(),
            'sole_source_by_segment': sole_source.groupby('Classification').size().to_dict(),
            'critical_risk_suppliers': len(high_risk[high_risk['Classification'].isin(['Strategic', 'Critical'])]),
            'high_spend_high_risk': len(self.data[(self.data['Supply_Risk_Score'] == 3) & 
                                                 (self.data['Annual_Spend'] > self.data['Annual_Spend'].quantile(0.8))])
        }
        
        self.analysis_results['risk_analysis'] = risk_analysis
        return risk_analysis
    
    def spend_concentration_analysis(self):
        """
        Analyze spend concentration patterns
        """
        # Pareto analysis
        sorted_suppliers = self.data.sort_values('Annual_Spend', ascending=False)
        sorted_suppliers['cumulative_spend'] = sorted_suppliers['Annual_Spend'].cumsum()
        total_spend = sorted_suppliers['Annual_Spend'].sum()
        sorted_suppliers['cumulative_spend_pct'] = sorted_suppliers['cumulative_spend'] / total_spend * 100
        
        # Find 80/20 breakpoint
        pareto_80_index = (sorted_suppliers['cumulative_spend_pct'] <= 80).sum()
        pareto_80_pct = pareto_80_index / len(sorted_suppliers) * 100
        
        # Segment spend analysis
        segment_spend = self.data.groupby('Classification')['Annual_Spend'].agg(['sum', 'count'])
        segment_spend['avg_spend'] = segment_spend['sum'] / segment_spend['count']
        segment_spend['spend_share'] = segment_spend['sum'] / total_spend * 100
        
        spend_analysis = {
            'pareto_80_suppliers_pct': pareto_80_pct,
            'pareto_80_supplier_count': pareto_80_index,
            'segment_spend_analysis': segment_spend.to_dict(),
            'top_10_suppliers_spend_share': sorted_suppliers.head(10)['Annual_Spend'].sum() / total_spend * 100
        }
        
        self.analysis_results['spend_analysis'] = spend_analysis
        return spend_analysis
    
    def innovation_potential_analysis(self):
        """
        Analyze innovation potential across segments
        """
        # High innovation suppliers
        high_innovation = self.data[self.data['Innovation_Score'] == 3]
        
        innovation_analysis = {
            'high_innovation_by_segment': high_innovation.groupby('Classification').size().to_dict(),
            'innovation_spend_correlation': self.data['Innovation_Score'].corr(np.log(self.data['Annual_Spend'])),
            'strategic_innovation_suppliers': len(high_innovation[high_innovation['Classification'] == 'Strategic']),
            'untapped_innovation_potential': len(high_innovation[high_innovation['Classification'] == 'Transactional'])
        }
        
        self.analysis_results['innovation_analysis'] = innovation_analysis
        return innovation_analysis
    
    def segmentation_effectiveness_metrics(self):
        """
        Calculate metrics to assess segmentation effectiveness
        """
        # Score separation between segments
        segment_scores = self.data.groupby('Classification')['Score'].mean()
        score_separation = segment_scores.max() - segment_scores.min()
        
        # Within-segment variance
        segment_variance = self.data.groupby('Classification')['Score'].var().mean()
        
        # Silhouette-like analysis for segmentation quality
        total_variance = self.data['Score'].var()
        between_segment_variance = self.data.groupby('Classification')['Score'].apply(
            lambda x: len(x) * (x.mean() - self.data['Score'].mean()) ** 2
        ).sum() / len(self.data)
        
        effectiveness_metrics = {
            'score_separation': score_separation,
            'avg_within_segment_variance': segment_variance,
            'between_segment_variance': between_segment_variance,
            'variance_ratio': between_segment_variance / total_variance,
            'segment_distinctiveness': score_separation / np.sqrt(segment_variance)
        }
        
        self.analysis_results['effectiveness_metrics'] = effectiveness_metrics
        return effectiveness_metrics
    
    def generate_actionable_insights(self):
        """
        Generate business-focused insights and recommendations
        """
        if not self.analysis_results:
            # Run all analyses if not done yet
            self.segment_profile_analysis()
            self.business_unit_analysis()
            self.risk_concentration_analysis()
            self.spend_concentration_analysis()
            self.innovation_potential_analysis()
            self.segmentation_effectiveness_metrics()
        
        insights = []
        
        # Strategic supplier insights
        strategic_count = self.analysis_results['segment_profiles'].get('Strategic', {}).get('count', 0)
        if strategic_count > 0:
            strategic_spend_share = self.analysis_results['segment_profiles']['Strategic']['spend_concentration'] * 100
            insights.append(f"Strategic suppliers ({strategic_count} suppliers) represent {strategic_spend_share:.1f}% of total spend")
        
        # Risk insights
        risk_data = self.analysis_results['risk_analysis']
        critical_risk = risk_data.get('critical_risk_suppliers', 0)
        if critical_risk > 0:
            insights.append(f"{critical_risk} Strategic/Critical suppliers have high supply risk - require immediate attention")
        
        # Spend concentration insights
        spend_data = self.analysis_results['spend_analysis']
        pareto_pct = spend_data['pareto_80_suppliers_pct']
        insights.append(f"{pareto_pct:.1f}% of suppliers drive 80% of spend (Pareto principle)")
        
        # Innovation insights
        innovation_data = self.analysis_results['innovation_analysis']
        untapped_innovation = innovation_data.get('untapped_innovation_potential', 0)
        if untapped_innovation > 0:
            insights.append(f"{untapped_innovation} Transactional suppliers have high innovation potential - consider upgrading")
        
        # Effectiveness insights
        effectiveness = self.analysis_results['effectiveness_metrics']
        if effectiveness['variance_ratio'] > 0.5:
            insights.append("Strong segmentation effectiveness - clear differentiation between segments")
        else:
            insights.append("Moderate segmentation effectiveness - consider refining classification criteria")
        
        return insights
    
    def export_analysis_summary(self):
        """
        Export comprehensive analysis summary
        """
        summary = {
            'analysis_timestamp': pd.Timestamp.now(),
            'total_suppliers': len(self.data),
            'segment_profiles': self.analysis_results.get('segment_profiles', {}),
            'business_unit_analysis': self.analysis_results.get('business_unit_analysis', {}),
            'risk_analysis': self.analysis_results.get('risk_analysis', {}),
            'spend_analysis': self.analysis_results.get('spend_analysis', {}),
            'innovation_analysis': self.analysis_results.get('innovation_analysis', {}),
            'effectiveness_metrics': self.analysis_results.get('effectiveness_metrics', {}),
            'actionable_insights': self.generate_actionable_insights()
        }
        
        return summary

def run_comprehensive_analysis(suppliers_data):
    """
    Run complete segmentation analysis and return results
    """
    print("Running Comprehensive Supplier Segmentation Analysis")
    print("=" * 55)
    
    analyzer = SegmentationAnalyzer(suppliers_data)
    
    print("\n1. Segment Profile Analysis...")
    profiles = analyzer.segment_profile_analysis()
    
    print("\n2. Business Unit Analysis...")
    bu_analysis = analyzer.business_unit_analysis()
    
    print("\n3. Risk Concentration Analysis...")
    risk_analysis = analyzer.risk_concentration_analysis()
    
    print("\n4. Spend Concentration Analysis...")
    spend_analysis = analyzer.spend_concentration_analysis()
    
    print("\n5. Innovation Potential Analysis...")
    innovation_analysis = analyzer.innovation_potential_analysis()
    
    print("\n6. Segmentation Effectiveness Metrics...")
    effectiveness = analyzer.segmentation_effectiveness_metrics()
    
    print("\n7. Generating Actionable Insights...")
    insights = analyzer.generate_actionable_insights()
    
    # Display key results
    print(f"\nKey Insights:")
    print("-" * 20)
    for i, insight in enumerate(insights, 1):
        print(f"{i}. {insight}")
    
    print(f"\nSegmentation Effectiveness Score: {effectiveness['variance_ratio']:.3f}")
    print(f"Score Separation: {effectiveness['score_separation']:.2f}")
    
    return analyzer.export_analysis_summary()

if __name__ == "__main__":
    # Demo with sample data
    from supplier_scoring_model import SupplierScoringModel
    
    model = SupplierScoringModel()
    sample_data = model.generate_sample_supplier_data(1000)
    classified_data = model.classify_suppliers()
    
    results = run_comprehensive_analysis(classified_data)
