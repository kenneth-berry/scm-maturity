#!/usr/bin/env python3
"""
Quick example of how to use the SCM Maturity Tool programmatically
"""

from scm_maturity_tool import SCMMaturityTool

def example_usage():
    """Example of programmatic usage of the SCM maturity tool"""
    
    print("=== SCM Maturity Tool - Programmatic Usage Example ===\n")
    
    # Create tool instance
    tool = SCMMaturityTool()
    
    # Set example scores (simulating a real assessment)
    example_scores = {
        "Version Control": 4,    # Good version control practices
        "Build Management": 2,   # Basic build processes
        "Release Management": 3, # Moderate release practices
        "Configuration Management": 3, # Decent config management
        "Quality Assurance": 2,  # Limited QA integration
        "Documentation": 1       # Poor documentation
    }
    
    # Apply scores to assessments
    category_index = {}
    for assessment in tool.assessments:
        if assessment.category not in category_index:
            category_index[assessment.category] = 0
        else:
            category_index[assessment.category] += 1
        
        # Get base score for category and add some variation
        base_score = example_scores.get(assessment.category, 3)
        variation = [-1, 0, 1, 0][category_index[assessment.category] % 4] 
        assessment.current_score = max(1, min(5, base_score + variation))
    
    # Calculate results
    results = tool.calculate_results()
    
    # Display results
    print("ASSESSMENT RESULTS:")
    print("-" * 40)
    print(f"Overall Score: {results['overall_score']}/5.0")
    print(f"Maturity Level: {results['maturity_level']}")
    print()
    
    print("Category Breakdown:")
    for category, score in results['category_scores'].items():
        print(f"  {category}: {score}/5.0")
    
    print()
    print("Top Recommendations:")
    for i, rec in enumerate(results['recommendations'][:3], 1):
        print(f"  {i}. {rec}")
    
    # Save results
    filename = "example_results.json"
    tool.save_results(results, filename)
    print(f"\nResults saved to {filename}")
    
    return results

if __name__ == "__main__":
    results = example_usage()
    
    print("\n" + "="*50)
    print("EXAMPLE COMPLETED SUCCESSFULLY")
    print("="*50)
    print(f"Final maturity level: {results['maturity_level']}")
    print(f"Areas needing improvement: {len(results['recommendations'])}")