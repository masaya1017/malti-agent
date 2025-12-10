#!/usr/bin/env python3
"""Test script to verify Strategy Agent integration"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from frameworks.three_c_analysis import ThreeCAnalysis
        print("✓ ThreeCAnalysis imported")
    except Exception as e:
        print(f"✗ ThreeCAnalysis import failed: {e}")
        return False
    
    try:
        from frameworks.swot_analysis import SWOTAnalysis
        print("✓ SWOTAnalysis imported")
    except Exception as e:
        print(f"✗ SWOTAnalysis import failed: {e}")
        return False
    
    try:
        from frameworks.five_forces import FiveForcesAnalysis
        print("✓ FiveForcesAnalysis imported")
    except Exception as e:
        print(f"✗ FiveForcesAnalysis import failed: {e}")
        return False
    
    try:
        from frameworks.pest_analysis import PESTAnalysis
        print("✓ PESTAnalysis imported")
    except Exception as e:
        print(f"✗ PESTAnalysis import failed: {e}")
        return False
    
    try:
        from frameworks.value_chain import ValueChainAnalysis
        print("✓ ValueChainAnalysis imported")
    except Exception as e:
        print(f"✗ ValueChainAnalysis import failed: {e}")
        return False
    
    return True

def test_strategy_agent_structure():
    """Test Strategy Agent structure without initializing LLM"""
    print("\nTesting Strategy Agent structure...")
    
    try:
        # Read the strategy_agent.py file
        with open('agents/strategy_agent.py', 'r') as f:
            content = f.read()
        
        # Check for required imports
        required_imports = [
            'from frameworks.pest_analysis import PESTAnalysis',
            'from frameworks.value_chain import ValueChainAnalysis'
        ]
        
        for imp in required_imports:
            if imp in content:
                print(f"✓ Found import: {imp}")
            else:
                print(f"✗ Missing import: {imp}")
                return False
        
        # Check for tool creation methods
        required_methods = [
            'def _create_pest_analysis_tool',
            'def _create_value_chain_analysis_tool'
        ]
        
        for method in required_methods:
            if method in content:
                print(f"✓ Found method: {method}")
            else:
                print(f"✗ Missing method: {method}")
                return False
        
        # Check that tools are registered
        if 'self._create_pest_analysis_tool()' in content:
            print("✓ PEST Analysis tool registered")
        else:
            print("✗ PEST Analysis tool not registered")
            return False
        
        if 'self._create_value_chain_analysis_tool()' in content:
            print("✓ Value Chain tool registered")
        else:
            print("✗ Value Chain tool not registered")
            return False
        
        # Check system prompt
        if 'PEST分析' in content and 'バリューチェーン分析' in content:
            print("✓ System prompt includes new frameworks")
        else:
            print("✗ System prompt missing framework descriptions")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Error reading strategy_agent.py: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Strategy Agent Integration Test")
    print("=" * 60)
    
    # Test imports
    imports_ok = test_imports()
    
    # Test structure
    structure_ok = test_strategy_agent_structure()
    
    print("\n" + "=" * 60)
    if imports_ok and structure_ok:
        print("✓ ALL TESTS PASSED")
        print("=" * 60)
        sys.exit(0)
    else:
        print("✗ SOME TESTS FAILED")
        print("=" * 60)
        sys.exit(1)
