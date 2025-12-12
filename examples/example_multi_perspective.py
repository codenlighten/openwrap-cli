#!/usr/bin/env python3
"""
Example: Multi-Perspective Analysis Engine

Demonstrates how to combine multiple specialized AI agents with different
perspectives to analyze complex problems and make better decisions.
"""

import sys
import os
from pathlib import Path
import json

# Add parent directory to path for imports
parent = str(Path(__file__).parent.parent)
sys.path.insert(0, parent)

from lumen_sdk import LumenClient, LumenAuth
from recursive_researcher import RecursiveResearcher


def get_client():
    """Load token from config and create client"""
    from pathlib import Path
    import json
    
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


class MultiPerspectiveEngine:
    """Orchestrates multiple specialized agents for comprehensive analysis"""
    
    def __init__(self, client: LumenClient):
        self.client = client
        self.researcher = RecursiveResearcher(client, max_depth=2)
    
    def analyze_from_perspectives(self, question: str, perspectives: dict):
        """
        Analyze a question from multiple perspectives
        
        Args:
            question: The question or decision to analyze
            perspectives: Dict mapping perspective names to analysis prompts
        
        Returns:
            dict: Results from each perspective plus synthesis
        """
        results = {}
        
        print(f"\n🔍 Analyzing: {question}")
        print(f"📊 Using {len(perspectives)} specialized perspectives\n")
        
        # Get analysis from each perspective
        for perspective_name, analysis_prompt in perspectives.items():
            print(f"   🤖 {perspective_name} perspective...")
            
            full_prompt = f"{analysis_prompt}\n\nQuestion: {question}"
            result = self.researcher.research(full_prompt)
            
            results[perspective_name] = {
                "analysis": result.answer,
                "confidence": "high" if not hasattr(result, 'missing_context') or not result.missing_context else "medium",
                "missing_context": getattr(result, 'missing_context', [])
            }
        
        print("\n   ✅ All perspectives analyzed")
        
        # Synthesize perspectives
        print("   🧠 Synthesizing insights...\n")
        synthesis = self._synthesize_perspectives(question, results)
        
        return {
            "perspectives": results,
            "synthesis": synthesis
        }
    
    def _synthesize_perspectives(self, question: str, perspectives: dict):
        """Synthesize multiple perspectives into unified analysis"""
        
        # Build synthesis prompt
        synthesis_prompt = f"""You are a synthesis agent. Analyze these different perspectives on the question:

QUESTION: {question}

PERSPECTIVES:
"""
        
        for name, result in perspectives.items():
            synthesis_prompt += f"\n{name.upper()} PERSPECTIVE:\n{result['analysis']}\n"
        
        synthesis_prompt += """
Provide a synthesis that:
1. Identifies areas of agreement across perspectives
2. Highlights conflicts or disagreements
3. Finds insights that emerge from combining perspectives
4. Provides a balanced recommendation

Format as JSON with keys: agreement, conflicts, emergent_insights, recommendation"""
        
        schema = {
            "type": "object",
            "properties": {
                "agreement": {"type": "array", "items": {"type": "string"}},
                "conflicts": {"type": "array", "items": {"type": "string"}},
                "emergent_insights": {"type": "array", "items": {"type": "string"}},
                "recommendation": {"type": "string"}
            },
            "required": ["agreement", "conflicts", "emergent_insights", "recommendation"],
            "additionalProperties": False
        }
        
        result = self.researcher.research(synthesis_prompt, schema=schema)
        
        return result.extracted_data if result.extracted_data else {
            "agreement": [],
            "conflicts": [],
            "emergent_insights": [],
            "recommendation": result.answer
        }


def demo_investment_decision():
    """Demo: Investment decision with multiple expert perspectives"""
    print("\n" + "="*70)
    print("DEMO 1: Investment Decision Analysis")
    print("="*70)
    
    client = get_client()
    engine = MultiPerspectiveEngine(client)
    
    question = "Should we invest in a renewable energy startup?"
    
    perspectives = {
        "Financial": """Analyze from a CFO perspective:
- Financial viability and ROI projections
- Revenue model sustainability
- Capital requirements and burn rate
- Exit strategy and timeline""",
        
        "Technical": """Analyze from a CTO perspective:
- Technology maturity and scalability
- Technical risks and challenges
- Competitive advantages
- IP and patents""",
        
        "Market": """Analyze from a market analyst perspective:
- Market size and growth potential
- Competitive landscape
- Customer acquisition strategy
- Market timing and trends""",
        
        "Risk": """Analyze from a risk management perspective:
- Regulatory and compliance risks
- Market risks and volatility
- Operational risks
- Mitigation strategies"""
    }
    
    result = engine.analyze_from_perspectives(question, perspectives)
    
    # Display results
    print("\n" + "="*70)
    print("📊 ANALYSIS RESULTS")
    print("="*70)
    
    for perspective_name, analysis in result['perspectives'].items():
        print(f"\n🔵 {perspective_name.upper()} PERSPECTIVE:")
        print(f"   Confidence: {analysis['confidence']}")
        print(f"   Analysis: {analysis['analysis'][:200]}...")
        if analysis['missing_context']:
            print(f"   ⚠️  Missing context: {len(analysis['missing_context'])} items")
    
    print("\n" + "="*70)
    print("🧠 SYNTHESIS")
    print("="*70)
    
    synthesis = result['synthesis']
    
    if isinstance(synthesis, dict):
        print("\n✅ Areas of Agreement:")
        for item in synthesis.get('agreement', []):
            print(f"   • {item}")
        
        print("\n⚠️  Conflicts & Disagreements:")
        for item in synthesis.get('conflicts', []):
            print(f"   • {item}")
        
        print("\n💡 Emergent Insights:")
        for item in synthesis.get('emergent_insights', []):
            print(f"   • {item}")
        
        print(f"\n🎯 Recommendation:\n   {synthesis.get('recommendation', 'No recommendation')}")
    else:
        print(synthesis)


def demo_product_launch():
    """Demo: Product launch readiness with cross-functional perspectives"""
    print("\n" + "="*70)
    print("DEMO 2: Product Launch Readiness Assessment")
    print("="*70)
    
    client = get_client()
    engine = MultiPerspectiveEngine(client)
    
    question = "Is our new SaaS product ready to launch?"
    
    perspectives = {
        "Engineering": """Assess from engineering perspective:
- Technical stability and bug count
- Performance and scalability readiness
- Security audit status
- Infrastructure preparedness""",
        
        "Product": """Assess from product management perspective:
- Feature completeness vs roadmap
- User testing feedback
- Product-market fit indicators
- Competitive positioning""",
        
        "Marketing": """Assess from marketing perspective:
- Go-to-market strategy readiness
- Content and collateral preparation
- Launch campaign plan
- Market timing""",
        
        "Support": """Assess from customer support perspective:
- Documentation completeness
- Support team training
- Help desk setup
- FAQ and troubleshooting guides"""
    }
    
    result = engine.analyze_from_perspectives(question, perspectives)
    
    # Display synthesis
    print("\n" + "="*70)
    print("🚀 LAUNCH READINESS SYNTHESIS")
    print("="*70)
    
    synthesis = result['synthesis']
    
    if isinstance(synthesis, dict):
        print("\n✅ Ready to Launch (Agreement):")
        for item in synthesis.get('agreement', []):
            print(f"   • {item}")
        
        print("\n⚠️  Concerns (Conflicts):")
        for item in synthesis.get('conflicts', []):
            print(f"   • {item}")
        
        print("\n💡 Cross-Functional Insights:")
        for item in synthesis.get('emergent_insights', []):
            print(f"   • {item}")
        
        print(f"\n🎯 Launch Decision:\n   {synthesis.get('recommendation', 'No decision')}")


def demo_strategic_planning():
    """Demo: Strategic planning with diverse stakeholder perspectives"""
    print("\n" + "="*70)
    print("DEMO 3: Strategic Planning - Enter New Market")
    print("="*70)
    
    client = get_client()
    engine = MultiPerspectiveEngine(client)
    
    question = "Should our company expand into the healthcare sector?"
    
    perspectives = {
        "Strategy": """Analyze from strategic perspective:
- Alignment with company vision and mission
- Strategic fit with existing capabilities
- Long-term competitive positioning
- Resource allocation implications""",
        
        "Legal": """Analyze from legal and compliance perspective:
- Regulatory requirements in healthcare
- Licensing and certifications needed
- Liability and risk exposure
- Compliance infrastructure costs""",
        
        "Operations": """Analyze from operations perspective:
- Operational complexity and changes needed
- Supply chain and vendor requirements
- Process modifications required
- Timeline and implementation phases""",
        
        "HR": """Analyze from human resources perspective:
- Talent and hiring needs
- Training and certification requirements
- Cultural fit and change management
- Retention risks"""
    }
    
    result = engine.analyze_from_perspectives(question, perspectives)
    
    synthesis = result['synthesis']
    
    print("\n" + "="*70)
    print("🎯 STRATEGIC DECISION SYNTHESIS")
    print("="*70)
    
    if isinstance(synthesis, dict):
        print("\n📊 Stakeholder Alignment:")
        for item in synthesis.get('agreement', []):
            print(f"   ✅ {item}")
        
        print("\n⚠️  Stakeholder Concerns:")
        for item in synthesis.get('conflicts', []):
            print(f"   ⚠️  {item}")
        
        print("\n💎 Strategic Insights (Emergent from multi-perspective analysis):")
        for item in synthesis.get('emergent_insights', []):
            print(f"   💡 {item}")
        
        print(f"\n🎯 Strategic Recommendation:\n\n{synthesis.get('recommendation', 'No recommendation')}")
        
        print("\n" + "="*70)
        print("Key Benefit: Single-perspective analysis would miss conflicts")
        print("             Multi-perspective reveals hidden risks and opportunities")
        print("="*70)


def main():
    """Run all multi-perspective analysis demos"""
    print("\n" + "="*70)
    print("🤝 MULTI-PERSPECTIVE ANALYSIS ENGINE DEMO")
    print("="*70)
    print("\nDemonstrating how specialized agents with different perspectives")
    print("collaborate to produce better decisions than any single expert.")
    print("\nKey Innovation: Each agent explores missingContext from THEIR")
    print("                perspective, leading to unexpected discoveries.")
    
    try:
        # Demo 1: Investment decision
        demo_investment_decision()
        
        input("\n\n⏸️  Press Enter to continue to next demo...")
        
        # Demo 2: Product launch
        demo_product_launch()
        
        input("\n\n⏸️  Press Enter to continue to final demo...")
        
        # Demo 3: Strategic planning
        demo_strategic_planning()
        
        print("\n" + "="*70)
        print("✅ ALL DEMOS COMPLETE")
        print("="*70)
        print("\nKey Takeaways:")
        print("1. Multiple perspectives reveal blind spots invisible to single experts")
        print("2. Conflicts between perspectives often highlight critical risks")
        print("3. Synthesis creates emergent insights no single agent would find")
        print("4. Cross-domain pattern matching discovers non-obvious connections")
        print("\n🚀 This replicates human expert panels but scales infinitely!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error running demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
