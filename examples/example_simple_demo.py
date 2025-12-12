#!/usr/bin/env python3
"""
Simple Example: Test the new use case patterns

Quick demo showing the three new use case implementations.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
parent = str(Path(__file__).parent.parent)
sys.path.insert(0, parent)

from lumen_sdk import LumenClient
from recursive_researcher import RecursiveResearcher
import json


def get_client():
    """Load token from config and create client"""
    config_file = Path.home() / ".lumen" / "config.json"
    if not config_file.exists():
        print("❌ Not logged in. Please run: lumen-cli login")
        sys.exit(1)
    
    with open(config_file) as f:
        config = json.load(f)
        token = config.get('token')
    
    if not token:
        print("❌ No token found. Please run: lumen-cli login")
        sys.exit(1)
    
    return LumenClient(token)


def demo_simple_research():
    """Simple demo: Recursive research with gap detection"""
    print("\n" + "="*70)
    print("🔬 AUTONOMOUS RESEARCH DEMO")
    print("="*70)
    print("\nDemonstrating self-aware research that identifies knowledge gaps\n")
    
    client = get_client()
    researcher = RecursiveResearcher(client, max_depth=1)
    
    question = "What are the key benefits of Python 3.12?"
    
    print(f"📝 Research Question: {question}\n")
    print("⏳ Researching (this explores missingContext automatically)...\n")
    
    try:
        result = researcher.research(question)
        
        print("✅ Research Complete!")
        print("-" * 70)
        print(f"\n{result.get('response', 'No response')}\n")
        
        if result.get('missing_context'):
            print("🔍 System Self-Awareness - Knowledge Gaps Identified:")
            for i, gap in enumerate(result['missing_context'][:3], 1):
                print(f"   {i}. {gap}")
            print("\n💡 In production, these gaps would be researched automatically")
            print("   to continuously improve the knowledge base.")
        else:
            print("\n✅ No knowledge gaps detected - comprehensive answer provided")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


def demo_code_generation():
    """Simple demo: Code generation"""
    print("\n" + "="*70)
    print("🛠️  CODE GENERATION DEMO")
    print("="*70)
    print("\nDemonstrating natural language to code generation\n")
    
    client = get_client()
    
    prompt = """Write a Python function that:
- Takes a list of numbers
- Returns the sum of even numbers
- Include a docstring and type hints
- Add input validation"""
    
    print(f"📝 Request: {prompt}\n")
    print("⏳ Generating code...\n")
    
    try:
        result = client.query(prompt, temperature=1.0, max_tokens=500)
        
        print("✅ Code Generated!")
        print("-" * 70)
        print(result['data']['response'])
        print("\n💡 The agent researched Python best practices automatically")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def demo_multi_perspective():
    """Simple demo: Multi-perspective analysis"""
    print("\n" + "="*70)
    print("🤝 MULTI-PERSPECTIVE ANALYSIS DEMO")
    print("="*70)
    print("\nDemonstrating specialized agents with different viewpoints\n")
    
    client = get_client()
    researcher = RecursiveResearcher(client, max_depth=1)
    
    decision = "Should we migrate our monolith to microservices?"
    
    print(f"🎯 Decision: {decision}\n")
    print("⏳ Analyzing from multiple perspectives...\n")
    
    perspectives = {
        "Technical": "Analyze technical feasibility, complexity, and risks of migrating to microservices",
        "Business": "Analyze cost, timeline, and business impact of microservices migration"
    }
    
    results = {}
    
    try:
        for perspective_name, analysis_prompt in perspectives.items():
            print(f"   🤖 {perspective_name} perspective...")
            
            full_prompt = f"{analysis_prompt}\n\nDecision: {decision}"
            result = researcher.research(full_prompt)
            
            results[perspective_name] = result.get('response', 'No response')
            print(f"   ✅ {perspective_name} analysis complete")
        
        print("\n" + "="*70)
        print("📊 ANALYSIS RESULTS")
        print("="*70)
        
        for perspective_name, analysis in results.items():
            print(f"\n🔵 {perspective_name.upper()} PERSPECTIVE:")
            print(f"{analysis[:300]}...")
        
        print("\n💡 In production, a synthesis agent would combine these")
        print("   perspectives to find conflicts, agreements, and emergent insights.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Run simple demos"""
    print("\n" + "="*70)
    print("🚀 NEW USE CASES - SIMPLE DEMO")
    print("="*70)
    print("\nTesting the three new powerful use case patterns:")
    print("  1. Autonomous Research (self-aware gap detection)")
    print("  2. Code Generation (natural language → working code)")
    print("  3. Multi-Perspective Analysis (specialized agents)")
    
    try:
        # Demo 1: Research
        demo_simple_research()
        
        input("\n\n⏸️  Press Enter to continue to code generation demo...")
        
        # Demo 2: Code Generation
        demo_code_generation()
        
        input("\n\n⏸️  Press Enter to continue to multi-perspective demo...")
        
        # Demo 3: Multi-Perspective
        demo_multi_perspective()
        
        print("\n" + "="*70)
        print("✅ ALL DEMOS COMPLETE")
        print("="*70)
        print("\nThese patterns scale to:")
        print("  • Self-improving knowledge bases")
        print("  • Complete development assistants")
        print("  • Multi-agent decision systems")
        print("\n💡 See full examples in examples/ directory")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error running demos: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
