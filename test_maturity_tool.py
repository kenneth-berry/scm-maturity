#!/usr/bin/env python3
"""
Test script for SCM Maturity Assessment Tool

This script tests various functionality of the SCM maturity tool including:
- Assessment initialization
- Score calculation
- Maturity level determination
- Recommendation generation
"""

import unittest
import json
import os
from scm_maturity_tool import SCMMaturityTool, MaturityLevel, Assessment

class TestSCMMaturityTool(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.tool = SCMMaturityTool()
    
    def test_initialization(self):
        """Test that the tool initializes correctly with assessments"""
        self.assertIsInstance(self.tool.assessments, list)
        self.assertGreater(len(self.tool.assessments), 0)
        
        # Check that assessments have required attributes
        for assessment in self.tool.assessments:
            self.assertIsInstance(assessment, Assessment)
            self.assertIsInstance(assessment.category, str)
            self.assertIsInstance(assessment.question, str)
            self.assertIsInstance(assessment.weight, float)
            self.assertEqual(assessment.current_score, 0)  # Initial score should be 0
    
    def test_assessment_categories(self):
        """Test that all expected categories are present"""
        expected_categories = {
            "Version Control",
            "Build Management", 
            "Release Management",
            "Configuration Management",
            "Quality Assurance",
            "Documentation"
        }
        
        actual_categories = set(assessment.category for assessment in self.tool.assessments)
        self.assertEqual(actual_categories, expected_categories)
    
    def test_maturity_level_determination(self):
        """Test maturity level determination based on scores"""
        test_cases = [
            (4.8, MaturityLevel.OPTIMIZING),
            (4.0, MaturityLevel.QUANTITATIVELY_MANAGED),
            (3.0, MaturityLevel.DEFINED),
            (2.0, MaturityLevel.MANAGED),
            (1.0, MaturityLevel.INITIAL)
        ]
        
        for score, expected_level in test_cases:
            actual_level = self.tool._determine_maturity_level(score)
            self.assertEqual(actual_level, expected_level, 
                           f"Score {score} should map to {expected_level.name}")
    
    def test_calculate_results_all_high_scores(self):
        """Test calculation with all high scores (should be OPTIMIZING)"""
        # Set all assessments to score 5
        for assessment in self.tool.assessments:
            assessment.current_score = 5
        
        results = self.tool.calculate_results()
        
        self.assertEqual(results['overall_score'], 5.0)
        self.assertEqual(results['maturity_level'], 'OPTIMIZING')
        
        # All category scores should be 5.0
        for category_score in results['category_scores'].values():
            self.assertEqual(category_score, 5.0)
    
    def test_calculate_results_all_low_scores(self):
        """Test calculation with all low scores (should be INITIAL)"""
        # Set all assessments to score 1
        for assessment in self.tool.assessments:
            assessment.current_score = 1
        
        results = self.tool.calculate_results()
        
        self.assertEqual(results['overall_score'], 1.0)
        self.assertEqual(results['maturity_level'], 'INITIAL')
        
        # All category scores should be 1.0
        for category_score in results['category_scores'].values():
            self.assertEqual(category_score, 1.0)
    
    def test_calculate_results_mixed_scores(self):
        """Test calculation with mixed scores"""
        # Set different scores for different assessments
        scores = [1, 2, 3, 4, 5] * (len(self.tool.assessments) // 5 + 1)
        
        for i, assessment in enumerate(self.tool.assessments):
            assessment.current_score = scores[i]
        
        results = self.tool.calculate_results()
        
        # Overall score should be around 3.0 (average)
        self.assertGreater(results['overall_score'], 2.5)
        self.assertLess(results['overall_score'], 3.5)
        
        # Should have recommendations for improvement
        self.assertIsInstance(results['recommendations'], list)
        self.assertGreater(len(results['recommendations']), 0)
    
    def test_recommendations_generation(self):
        """Test that recommendations are generated for low-scoring categories"""
        # Set Version Control category to low scores
        for assessment in self.tool.assessments:
            if assessment.category == "Version Control":
                assessment.current_score = 1
            else:
                assessment.current_score = 4
        
        results = self.tool.calculate_results()
        recommendations = results['recommendations']
        
        # Should have recommendation for Version Control
        version_control_recommendation = any(
            'version control' in rec.lower() for rec in recommendations
        )
        self.assertTrue(version_control_recommendation)
    
    def test_weight_influence(self):
        """Test that assessment weights influence the final score"""
        # Create two identical tools but modify weights
        tool1 = SCMMaturityTool()
        tool2 = SCMMaturityTool()
        
        # Set same base scores but one different score
        for i, (assessment1, assessment2) in enumerate(zip(tool1.assessments, tool2.assessments)):
            if i == 0:
                assessment1.current_score = 1  # Low score with normal weight
                assessment2.current_score = 1  # Low score with high weight
            else:
                assessment1.current_score = 5
                assessment2.current_score = 5
        
        # Significantly increase weight of first assessment in tool2
        tool2.assessments[0].weight = 5.0  # Much higher weight
        
        results1 = tool1.calculate_results()
        results2 = tool2.calculate_results()
        
        # Results should be different due to weight difference
        # tool2 should have a lower score because the low-scoring item has more weight
        self.assertNotEqual(results1['overall_score'], results2['overall_score'])
        self.assertLess(results2['overall_score'], results1['overall_score'])
    
    def test_results_structure(self):
        """Test that results have the expected structure"""
        # Set some scores
        for assessment in self.tool.assessments:
            assessment.current_score = 3
        
        results = self.tool.calculate_results()
        
        # Check required keys
        required_keys = ['overall_score', 'maturity_level', 'category_scores', 'recommendations']
        for key in required_keys:
            self.assertIn(key, results)
        
        # Check data types
        self.assertIsInstance(results['overall_score'], (int, float))
        self.assertIsInstance(results['maturity_level'], str)
        self.assertIsInstance(results['category_scores'], dict)
        self.assertIsInstance(results['recommendations'], list)
        
        # Check score ranges
        self.assertGreaterEqual(results['overall_score'], 1.0)
        self.assertLessEqual(results['overall_score'], 5.0)
        
        for category_score in results['category_scores'].values():
            self.assertGreaterEqual(category_score, 1.0)
            self.assertLessEqual(category_score, 5.0)

class TestIntegration(unittest.TestCase):
    """Integration tests for the SCM Maturity Tool"""
    
    def setUp(self):
        self.tool = SCMMaturityTool()
        self.test_file = "test_results.json"
    
    def tearDown(self):
        # Clean up test files
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_save_and_load_results(self):
        """Test saving results to file and loading them back"""
        # Set some scores
        for assessment in self.tool.assessments:
            assessment.current_score = 4
        
        results = self.tool.calculate_results()
        self.tool.save_results(results, self.test_file)
        
        # Verify file was created
        self.assertTrue(os.path.exists(self.test_file))
        
        # Load results back
        with open(self.test_file, 'r') as f:
            loaded_results = json.load(f)
        
        # Compare original and loaded results
        self.assertEqual(results['overall_score'], loaded_results['overall_score'])
        self.assertEqual(results['maturity_level'], loaded_results['maturity_level'])
        self.assertEqual(results['category_scores'], loaded_results['category_scores'])
        self.assertEqual(results['recommendations'], loaded_results['recommendations'])

def run_demo_test():
    """Run a demonstration of the tool with sample data"""
    print("=" * 60)
    print("DEMONSTRATION: SCM Maturity Assessment Tool")
    print("=" * 60)
    
    tool = SCMMaturityTool()
    
    # Simulate a mid-level organization
    demo_scores = {
        "Version Control": [4, 3, 3, 4],  # Good version control
        "Build Management": [3, 2, 3, 2],  # Needs improvement
        "Release Management": [2, 3, 2, 3],  # Basic practices
        "Configuration Management": [3, 3, 4],  # Decent
        "Quality Assurance": [2, 2, 3],  # Weak area
        "Documentation": [2, 2, 1]  # Very weak
    }
    
    # Apply demo scores
    score_index = 0
    for assessment in tool.assessments:
        category_scores = demo_scores.get(assessment.category, [3])
        assessment.current_score = category_scores[score_index % len(category_scores)]
        score_index += 1
    
    results = tool.calculate_results()
    tool.display_results(results)
    
    print(f"\nTest completed successfully!")
    print(f"Assessed {len(tool.assessments)} criteria across {len(demo_scores)} categories")
    
    return results

if __name__ == "__main__":
    print("Testing SCM Maturity Assessment Tool...")
    
    # Run unit tests
    print("\n" + "=" * 50)
    print("RUNNING UNIT TESTS")
    print("=" * 50)
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSCMMaturityTool)
    integration_suite = unittest.TestLoader().loadTestsFromTestCase(TestIntegration)
    
    runner = unittest.TextTestRunner(verbosity=2)
    test_result = runner.run(suite)
    integration_result = runner.run(integration_suite)
    
    # Run demonstration
    demo_results = run_demo_test()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    total_tests = test_result.testsRun + integration_result.testsRun
    total_failures = len(test_result.failures) + len(integration_result.failures)
    total_errors = len(test_result.errors) + len(integration_result.errors)
    
    print(f"Total tests run: {total_tests}")
    print(f"Failures: {total_failures}")
    print(f"Errors: {total_errors}")
    
    if total_failures == 0 and total_errors == 0:
        print("✅ ALL TESTS PASSED!")
    else:
        print("❌ SOME TESTS FAILED")
    
    print(f"\nDemo assessment result: {demo_results['maturity_level']} level")
    print(f"Demo overall score: {demo_results['overall_score']}/5.0")