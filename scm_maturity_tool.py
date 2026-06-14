#!/usr/bin/env python3
"""
Berry Consulting Supply Chain Maturity Assessment (SCMA) Tool

This tool evaluates the maturity level of Supply Chain Management practices
in organizations using the Berry Consulting 5-level framework. It assesses 6 key pillars
and provides consulting package recommendations.
"""

import json
import sys
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum

class MaturityLevel(Enum):
    AD_HOC = 1
    FUNCTIONAL = 2
    INTEGRATED = 3
    OPTIMIZED = 4
    TRANSFORMATIONAL = 5

@dataclass
class Assessment:
    category: str
    question: str
    weight: float
    current_score: int  # 1-5 scale
    
class SCMAssessmentTool:
    def __init__(self):
        self.assessments = self._initialize_assessments()
        
    def _initialize_assessments(self) -> List[Assessment]:
        """Initialize the SCMA assessment questions across 6 pillars"""
        return [
            # Planning (5 questions)
            Assessment("Planning", "Do you have a structured demand forecasting process?", 1.0, 0),
            Assessment("Planning", "How often are sales and operations aligned in planning cycles?", 0.9, 0),
            Assessment("Planning", "How accurate are your forecasts (compared to actual demand)?", 0.8, 0),
            Assessment("Planning", "Do you run scenario/sensitivity analysis for demand shifts?", 0.7, 0),
            Assessment("Planning", "Is risk management integrated into your planning process?", 0.8, 0),
            
            # Procurement & Supplier Management (4 questions)
            Assessment("Procurement", "Are supplier performance metrics monitored regularly?", 0.9, 0),
            Assessment("Procurement", "Do you negotiate contracts based on long-term partnerships?", 0.8, 0),
            Assessment("Procurement", "How digitized is your procurement process (e-tendering, eRFQ)?", 0.7, 0),
            Assessment("Procurement", "Is supplier risk/ESG compliance part of vendor evaluation?", 0.8, 0),
            
            # Logistics & Distribution (5 questions)
            Assessment("Logistics", "Do you have end-to-end visibility of shipments in real time?", 1.0, 0),
            Assessment("Logistics", "How optimized are your delivery routes & fleet utilization?", 0.9, 0),
            Assessment("Logistics", "Do you track logistics KPIs (cost-to-serve, OTIF, etc.)?", 0.8, 0),
            Assessment("Logistics", "Are third-party logistics providers (3PLs) effectively integrated?", 0.7, 0),
            Assessment("Logistics", "Do you run simulations to improve regional distribution planning?", 0.6, 0),
            
            # Order-to-Cash (4 questions)
            Assessment("Order-to-Cash", "How well do you track stock levels across locations?", 0.9, 0),
            Assessment("Order-to-Cash", "Do you use safety stock/reorder point optimization methods?", 0.8, 0),
            Assessment("Order-to-Cash", "How often do you experience stockouts or overstocks?", 0.8, 0),
            Assessment("Order-to-Cash", "Is inventory data visible in real time across functions?", 0.7, 0),
            
            # Technology & Data (4 questions)
            Assessment("Technology", "What is the maturity of your ERP or core SCM systems?", 1.0, 0),
            Assessment("Technology", "Do you use advanced analytics (dashboards, predictive models)?", 0.9, 0),
            Assessment("Technology", "Is AI/ML integrated into decision-making (forecasting, optimization)?", 0.8, 0),
            Assessment("Technology", "Do you use technology (ERP/WMS) for automated replenishment?", 0.7, 0),
            
            # ESG & Compliance (3 questions)
            Assessment("ESG & Compliance", "Do you measure and report supply chain sustainability (CO₂, waste)?", 0.9, 0),
            Assessment("ESG & Compliance", "Is traceability (farm-to-fork / source-to-shelf) embedded?", 0.8, 0),
            Assessment("ESG & Compliance", "Do you align supply chain processes with global ESG standards (GRI, SASB, etc.)?", 0.7, 0),
        ]
    
    def conduct_assessment(self) -> Dict:
        """Conduct interactive assessment"""
        print("=== Berry Consulting Supply Chain Maturity Assessment (SCMA) ===")
        print("Please rate each aspect on a scale of 1-5:")
        print("1 = Ad-Hoc/Reactive (No structured process)")
        print("2 = Functional/Emerging (Basic processes exist)")
        print("3 = Integrated/Process-Driven (Coordinated across functions)")
        print("4 = Optimized/Data-Driven (Advanced analytics, KPIs)")
        print("5 = Transformational/Digital (AI-driven, best-in-class)")
        print()
        print("💡 For detailed scoring guidance, see SCORING_GUIDE.md")
        print("-" * 70)
        
        for assessment in self.assessments:
            while True:
                try:
                    print(f"\nCategory: {assessment.category}")
                    print(f"Question: {assessment.question}")
                    score = int(input("Score (1-5): "))
                    if 1 <= score <= 5:
                        assessment.current_score = score
                        break
                    else:
                        print("Please enter a score between 1 and 5")
                except ValueError:
                    print("Please enter a valid number")
        
        return self.calculate_results()
    
    def calculate_results(self) -> Dict:
        """Calculate maturity results"""
        category_data = {}
        
        # Collect scores and weights by category
        for assessment in self.assessments:
            if assessment.category not in category_data:
                category_data[assessment.category] = {'scores': [], 'weights': []}
            category_data[assessment.category]['scores'].append(assessment.current_score)
            category_data[assessment.category]['weights'].append(assessment.weight)
        
        # Calculate weighted average per category
        category_averages = {}
        for category, data in category_data.items():
            scores = data['scores']
            weights = data['weights']
            # Calculate weighted average
            weighted_sum = sum(score * weight for score, weight in zip(scores, weights))
            total_weight = sum(weights)
            category_averages[category] = weighted_sum / total_weight
        
        # Calculate overall maturity score
        overall_score = sum(category_averages.values()) / len(category_averages)
        
        # Determine maturity level
        maturity_level = self._determine_maturity_level(overall_score)
        
        results = {
            "overall_score": round(overall_score, 2),
            "maturity_level": maturity_level.name,
            "category_scores": {k: round(v, 2) for k, v in category_averages.items()},
            "recommendations": self._generate_recommendations(category_averages, overall_score),
            "consulting_package": self._suggest_consulting_package(maturity_level, overall_score)
        }
        
        return results
    
    def _determine_maturity_level(self, score: float) -> MaturityLevel:
        """Determine maturity level based on score"""
        if score >= 4.5:
            return MaturityLevel.TRANSFORMATIONAL
        elif score >= 3.5:
            return MaturityLevel.OPTIMIZED
        elif score >= 2.5:
            return MaturityLevel.INTEGRATED
        elif score >= 1.5:
            return MaturityLevel.FUNCTIONAL
        else:
            return MaturityLevel.AD_HOC
    
    def _generate_recommendations(self, category_scores: Dict[str, float], overall_score: float) -> List[str]:
        """Generate recommendations based on assessment results"""
        recommendations = []
        
        # Find weakest categories
        sorted_categories = sorted(category_scores.items(), key=lambda x: x[1])
        
        for category, score in sorted_categories[:3]:  # Top 3 areas for improvement
            if score < 3.0:
                if category == "Planning":
                    recommendations.append("Implement structured demand planning with S&OP (Sales & Operations Planning) process")
                elif category == "Procurement":
                    recommendations.append("Digitize procurement processes and establish supplier performance scorecards")
                elif category == "Logistics":
                    recommendations.append("Implement real-time shipment visibility and route optimization systems")
                elif category == "Order-to-Cash":
                    recommendations.append("Establish inventory optimization with safety stock management and automated replenishment")
                elif category == "Technology":
                    recommendations.append("Upgrade to integrated ERP/SCM systems with advanced analytics and dashboards")
                elif category == "ESG & Compliance":
                    recommendations.append("Implement ESG metrics tracking and establish supply chain sustainability reporting")
        
        # Level-specific recommendations
        if overall_score < 1.5:  # Ad-Hoc
            recommendations.append("Urgent stabilization needed - document basic processes and implement visibility tools")
        elif overall_score < 2.5:  # Functional
            recommendations.append("Focus on cross-functional integration and standardizing supply chain processes")
        elif overall_score < 3.5:  # Integrated
            recommendations.append("Implement predictive analytics and supplier collaboration programs")
        elif overall_score < 4.5:  # Optimized
            recommendations.append("Focus on digital transformation, AI/ML optimization, and ESG leadership")
        
        return recommendations
    
    def _suggest_consulting_package(self, maturity_level: MaturityLevel, overall_score: float) -> Dict:
        """Suggest appropriate Berry Consulting package based on maturity level"""
        if maturity_level in [MaturityLevel.AD_HOC, MaturityLevel.FUNCTIONAL] or overall_score < 2.5:
            return {
                "package": "Diagnostic",
                "description": "Baseline assessment, process documentation, KPI setup, and quick wins identification",
                "scope": "Process standardization, basic SCM framework, 1-day leadership workshop",
                "outcome": "Move from firefighting to stable functional control",
                "duration": "4-6 weeks",
                "price_range": "$3,000 - $8,000"
            }
        elif maturity_level == MaturityLevel.INTEGRATED or (2.5 <= overall_score < 3.5):
            return {
                "package": "Advisory", 
                "description": "Cross-functional integration, S&OP implementation, ERP/WMS guidance, ESG baseline",
                "scope": "Integrated planning, supplier scorecards, digital tools advisory, ESG framework",
                "outcome": "Move from functional silos to integrated, data-driven supply chain",
                "duration": "6-12 weeks",
                "price_range": "$15,000 - $35,000"
            }
        else:  # OPTIMIZED or TRANSFORMATIONAL
            return {
                "package": "Transformation",
                "description": "Digital twins, AI/ML optimization, end-to-end ESG strategy, regional redesign",
                "scope": "Predictive analytics, digital transformation, ESG leadership, change management",
                "outcome": "Move to world-class, resilient supply chain ecosystem",
                "duration": "6-12 months",
                "price_range": "$50,000+"
            }
    
    def display_results(self, results: Dict):
        """Display assessment results"""
        print("\n" + "=" * 50)
        print("SCM MATURITY ASSESSMENT RESULTS")
        print("=" * 50)
        
        print(f"\nOverall Maturity Score: {results['overall_score']}/5.0")
        print(f"Maturity Level: {results['maturity_level']}")
        
        print("\nCategory Breakdown:")
        for category, score in results['category_scores'].items():
            print(f"  {category}: {score}/5.0")
        
        print("\nRecommendations:")
        for i, recommendation in enumerate(results['recommendations'], 1):
            print(f"  {i}. {recommendation}")
        
        # Maturity level descriptions
        print(f"\n--- {results['maturity_level']} Level Description ---")
        level_descriptions = {
            "AD_HOC": "Supply chain processes are reactive and uncoordinated. High costs, inefficiency, no resilience.",
            "FUNCTIONAL": "Basic processes exist but are siloed. Policies in place but still tactical, not strategic.",
            "INTEGRATED": "Cross-functional coordination with integrated systems. Costs reducing, better visibility.",
            "OPTIMIZED": "Data-driven with advanced analytics. High efficiency, resilience, competitive advantage.",
            "TRANSFORMATIONAL": "AI-driven, digital twins, sustainability leadership. World-class efficiency and innovation."
        }
        print(level_descriptions.get(results['maturity_level'], "Unknown level"))
        
        # Suggested consulting package
        package = results['consulting_package']
        print(f"\n🎯 RECOMMENDED BERRY CONSULTING PACKAGE")
        print("=" * 50)
        print(f"Package: {package['package']}")
        print(f"Description: {package['description']}")
        print(f"Scope: {package['scope']}")
        print(f"Expected Outcome: {package['outcome']}")
        print(f"Duration: {package['duration']}")
        print(f"Investment Range: {package['price_range']}")
        print("\n💡 Contact Berry Consulting: kenneth@berrycom.co.ke | +254 727 866057")
    
    def save_results(self, results: Dict, filename: str = "scm_maturity_results.json"):
        """Save results to JSON file"""
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to {filename}")

def main():
    """Main function to run the SCM maturity assessment"""
    tool = SCMAssessmentTool()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        # Demo mode with predefined scores
        print("Running in demo mode...")
        demo_scores = [3, 4, 2, 3, 4, 3, 3, 2, 3, 4, 2, 3, 4, 3, 3, 2, 3, 2, 2, 3, 2]
        for i, assessment in enumerate(tool.assessments):
            if i < len(demo_scores):
                assessment.current_score = demo_scores[i]
            else:
                assessment.current_score = 3
        
        results = tool.calculate_results()
        tool.display_results(results)
        tool.save_results(results)
    else:
        # Interactive mode
        results = tool.conduct_assessment()
        tool.display_results(results)
        
        save = input("\nSave results to file? (y/n): ").lower().strip()
        if save in ['y', 'yes']:
            tool.save_results(results)

if __name__ == "__main__":
    main()