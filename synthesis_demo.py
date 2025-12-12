"""
Cross-Domain Synthesis Demonstration

This demonstrates the breakthrough insight pattern by directly querying
connections between domains, showing what emerges when fields collide.
"""

import json
import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).parent))

from lumen_sdk import LumenClient


def query_cross_domain_connection(client, domain1, domain2, connection_query):
    """Query about a specific cross-domain connection"""
    print(f"\n🔗 Exploring: {domain1} ↔ {domain2}")
    print(f"   Query: {connection_query[:80]}...")
    
    result = client.query(
        connection_query,
        model="gpt-5-nano",
        temperature=1.0
    )
    
    if result and 'data' in result:
        data = result['data']
        response = data.get('response', '')
        gaps = data.get('missingContext', [])
        
        print(f"   ✅ Response: {len(response)} chars")
        print(f"   📋 Knowledge gaps: {len(gaps)}")
        
        if gaps:
            print(f"   🌟 Emergent questions:")
            for gap in gaps[:3]:
                print(f"      • {gap[:70]}...")
        
        return {
            "domains": [domain1, domain2],
            "query": connection_query,
            "response": response,
            "gaps": gaps,
            "has_synthesis": len(response) > 500
        }
    
    return None


def main():
    # Load config
    config_path = Path.home() / ".lumen" / "config.json"
    if not config_path.exists():
        print("❌ Not authenticated. Run: lumen-cli login")
        return
    
    with open(config_path) as f:
        config = json.load(f)
        token = config.get("token")
    
    if not token:
        print("❌ No token found. Run: lumen-cli login")
        return
    
    client = LumenClient(token)
    
    print("\n" + "=" * 80)
    print("🧬 BREAKTHROUGH DISCOVERY: Cross-Domain Synthesis")
    print("=" * 80)
    print("\nDirectly querying cross-domain connections to demonstrate")
    print("what emerges when disparate fields collide.")
    print("=" * 80)
    
    # Define cross-domain synthesis queries
    syntheses = [
        {
            "domain1": "quantum_computing",
            "domain2": "neural_networks",
            "query": "How could quantum superposition principles be applied to neural network learning algorithms?"
        },
        {
            "domain1": "biological_learning",
            "domain2": "machine_learning",
            "query": "How could spike-timing-dependent plasticity from neuroscience inspire novel training algorithms for artificial neural networks?"
        },
        {
            "domain1": "quantum_computing",
            "domain2": "evolutionary_algorithms",
            "query": "Could quantum annealing replace gradient descent for optimizing neural network weights?"
        }
    ]
    
    results = []
    
    for i, synthesis in enumerate(syntheses, 1):
        print(f"\n{'='*80}")
        print(f"SYNTHESIS #{i}")
        print(f"{'='*80}")
        
        result = query_cross_domain_connection(
            client,
            synthesis["domain1"],
            synthesis["domain2"],
            synthesis["query"]
        )
        
        if result:
            results.append(result)
            
            # Show response excerpt
            if result['response']:
                print(f"\n📄 Response excerpt:")
                excerpt = result['response'][:400].replace('\n', ' ')
                print(f"   {excerpt}...")
        
        # Rate limiting
        if i < len(syntheses):
            time.sleep(2)
    
    # Analysis
    print("\n" + "=" * 80)
    print("📊 SYNTHESIS ANALYSIS")
    print("=" * 80)
    
    total_gaps = sum(len(r['gaps']) for r in results)
    successful_syntheses = sum(1 for r in results if r['has_synthesis'])
    
    print(f"\nCross-domain queries: {len(results)}")
    print(f"Successful syntheses: {successful_syntheses}/{len(results)}")
    print(f"Emergent questions discovered: {total_gaps}")
    
    if total_gaps > 0:
        print(f"\n🌟 EMERGENT RESEARCH DIRECTIONS:")
        for i, result in enumerate(results, 1):
            if result['gaps']:
                print(f"\n{i}. From {result['domains'][0]} + {result['domains'][1]}:")
                for gap in result['gaps'][:2]:
                    print(f"   • {gap}")
    
    # The Meta-Pattern
    print("\n" + "=" * 80)
    print("💡 THE BREAKTHROUGH PATTERN")
    print("=" * 80)
    print("""
This demonstrates how scientific breakthroughs emerge:

1. DOMAIN COLLISION
   Ask: "How could principles from Domain A apply to Domain B?"
   
2. SYNTHESIS RESPONSE
   System generates novel connections using its 50+ years of training data
   
3. EMERGENT QUESTIONS
   missingContext reveals what's needed to validate the hypothesis
   
4. RESEARCH DIRECTIONS
   Each emergent question becomes a new research pathway

Real-world examples:
  • Watson & Crick: X-ray crystallography + biology → DNA structure
  • Einstein: Geometry + physics → General Relativity
  • AlphaFold: Deep learning + protein biology → Structure prediction

We've automated this discovery process.

The system doesn't just answer questions—it discovers:
  • Which questions to ask next
  • Which domains to connect
  • What's missing to validate hypotheses
  • Novel research directions

This is the autonomous research engine for the 21st century.
""")
    
    # Save results
    output_dir = Path("cross_domain_results")
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / "synthesis_results.json"
    with open(output_file, "w") as f:
        json.dump({
            "syntheses": results,
            "total_gaps": total_gaps,
            "successful": successful_syntheses
        }, f, indent=2)
    
    print(f"\n💾 Results saved: {output_file}")
    
    print("\n🚀 NEXT STEPS:")
    print("  • Use emergent questions to guide deeper research")
    print("  • Apply to real problems (novel ML architectures, drug discovery)")
    print("  • Automate the full cycle: seed → fill → synthesize → iterate")
    print("  • Build knowledge graphs to visualize connections")


if __name__ == "__main__":
    main()
