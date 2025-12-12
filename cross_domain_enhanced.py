"""
Enhanced Cross-Domain Research with Targeted Queries

This version uses more specific technical questions that are more likely
to trigger missingContext responses, enabling true cross-domain synthesis.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from lumen_sdk import LumenClient
from cross_domain_research import CrossDomainResearcher


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
    
    # Initialize
    client = LumenClient(token)
    researcher = CrossDomainResearcher(client)
    
    # Use MORE SPECIFIC technical questions that will trigger missingContext
    domains = {
        "quantum_ml": [
            "How would I implement a quantum circuit for supervised learning?",
            "What quantum gates are needed for gradient-free optimization?"
        ],
        "bio_neural_learning": [
            "How do I implement spike-timing-dependent plasticity in artificial neural networks?",
            "What data structures represent synaptic weight changes in Hebbian learning?"
        ],
        "gradient_free_optimization": [
            "How do I implement evolution strategies for training deep neural networks?",
            "What hyperparameters control mutation rates in neuroevolution?"
        ]
    }
    
    print("\n" + "=" * 80)
    print("🔬 TARGETED CROSS-DOMAIN RESEARCH")
    print("=" * 80)
    print("\nUsing specific technical queries to trigger missingContext...")
    print("\nDomains:")
    for domain, queries in domains.items():
        print(f"  • {domain}")
        for q in queries:
            print(f"    - {q[:70]}...")
    print("\n" + "=" * 80)
    
    # Phase 1: Seed all domains
    print("\n📍 PHASE 1: Domain Seeding")
    researcher.seed_domains(domains)
    
    # Check if we got any gaps
    total_gaps = sum(len(d['initial_gaps']) for d in researcher.domains.values())
    print(f"\n📊 Total gaps identified across all domains: {total_gaps}")
    
    if total_gaps == 0:
        print("\n⚠️  No gaps identified with these queries.")
        print("This happens when queries are still too broad or the API doesn't")
        print("return missingContext for certain question types.")
        print("\n💡 However, we can still demonstrate the concept:")
        print("   If gaps were identified, the system would:")
        print("   1. Fill gaps recursively")
        print("   2. Extract technical concepts")
        print("   3. Detect concept overlap across domains")
        print("   4. Generate synthesis hypotheses")
        return
    
    # Phase 2: Fill gaps
    print("\n📍 PHASE 2: Knowledge Gap Filling")
    print(f"⚠️  Filling up to 3 gaps per domain (rate-limited for demo)")
    all_concepts = researcher.fill_domain_gaps(max_gaps_per_domain=3)
    
    # Phase 3: Synthesize
    print("\n📍 PHASE 3: Cross-Domain Synthesis")
    insights = researcher.synthesize_insights()
    
    # Save results
    results = researcher.save_results()
    
    # Summary
    print("\n" + "=" * 80)
    print("✅ EXPERIMENT COMPLETE")
    print("=" * 80)
    print(f"\nDomains explored: {len(domains)}")
    print(f"Gaps identified: {total_gaps}")
    print(f"Cross-domain links: {len(researcher.cross_domain_links)}")
    print(f"Potential breakthroughs: {len(insights)}")
    
    if insights:
        print("\n🌟 BREAKTHROUGH INSIGHTS:")
        for i, insight in enumerate(insights, 1):
            print(f"\n{i}. {insight['domains'][0]} + {insight['domains'][1]}")
            print(f"   {insight['hypothesis']}")


if __name__ == "__main__":
    main()
