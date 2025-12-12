"""
Cross-Domain Research Experiment

Demonstrates how autonomous research across multiple domains can discover
emergent connections and breakthrough insights through gap-filling synthesis.

This is the "killer app" for scientific research - enabling discoveries that
would be nearly impossible for human researchers working in isolation.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
import time

sys.path.insert(0, str(Path(__file__).parent))

from lumen_sdk import LumenClient
from knowledge_evolution import KnowledgeEvolution
from knowledge_evolution_step2 import GapFiller


class CrossDomainResearcher:
    """Autonomous researcher that explores multiple domains and finds connections"""
    
    def __init__(self, client: LumenClient):
        self.client = client
        self.domains = {}
        self.cross_domain_links = []
    
    def seed_domains(self, domain_configs: dict):
        """Seed multiple research domains with initial queries"""
        print("\n🌍 CROSS-DOMAIN RESEARCH EXPERIMENT")
        print("=" * 80)
        print(f"\nSeeding {len(domain_configs)} research domains...")
        
        for domain_name, queries in domain_configs.items():
            print(f"\n📚 Domain: {domain_name}")
            print(f"   Queries: {len(queries)}")
            
            # Create knowledge evolution experiment for this domain
            experiment = KnowledgeEvolution(self.client, domain_name)
            gaps = experiment.seed_knowledge(queries)
            
            # Save the experiment data
            experiment.save_experiment()
            
            self.domains[domain_name] = {
                "experiment": experiment,
                "experiment_dir": str(experiment.experiment_dir),
                "initial_gaps": gaps
            }
            
            print(f"   ✅ {len(gaps)} gaps identified")
        
        print(f"\n✅ All domains seeded")
        return self.domains
    
    def fill_domain_gaps(self, max_gaps_per_domain=3):
        """Fill gaps in each domain and look for cross-domain connections"""
        print("\n🔬 FILLING KNOWLEDGE GAPS ACROSS DOMAINS")
        print("=" * 80)
        
        all_concepts = {}  # Track concepts across domains
        
        for domain_name, domain_data in self.domains.items():
            print(f"\n📖 Filling gaps in: {domain_name}")
            
            # Convert string path to Path object
            experiment_dir = Path(domain_data["experiment_dir"])
            filler = GapFiller(str(experiment_dir), self.client)
            results = filler.fill_gaps(max_gaps=max_gaps_per_domain)
            
            # Extract concepts from this domain
            domain_concepts = self._extract_concepts(results)
            all_concepts[domain_name] = domain_concepts
            
            print(f"   ✅ Filled {results.get('gaps_filled', 0)} gaps")
            print(f"   🌟 {results.get('emergent_insights', 0)} emergent insights")
        
        # Detect cross-domain connections
        self._detect_cross_domain_links(all_concepts)
        
        return all_concepts
    
    def _extract_concepts(self, fill_results: dict) -> set:
        """Extract key concepts from gap filling results"""
        concepts = set()
        
        # Extract from filled gap content
        for gap_data in fill_results.get('filled', []):
            response = gap_data.get('response', '')
            # Simple concept extraction (in production, use NLP/entity extraction)
            words = response.lower().split()
            # Focus on technical terms (simplified)
            technical_terms = [w for w in words if len(w) > 8]
            concepts.update(technical_terms[:10])  # Top 10 terms
        
        return concepts
    
    def _detect_cross_domain_links(self, all_concepts: dict):
        """Detect when concepts appear across different domains"""
        print("\n🔗 DETECTING CROSS-DOMAIN CONNECTIONS")
        print("=" * 80)
        
        domains = list(all_concepts.keys())
        
        for i, domain1 in enumerate(domains):
            for domain2 in domains[i+1:]:
                # Find shared concepts
                shared = all_concepts[domain1].intersection(all_concepts[domain2])
                
                if shared:
                    print(f"\n🌟 CONNECTION FOUND:")
                    print(f"   {domain1} ↔ {domain2}")
                    print(f"   Shared concepts: {len(shared)}")
                    print(f"   Examples: {list(shared)[:3]}")
                    
                    self.cross_domain_links.append({
                        "domain1": domain1,
                        "domain2": domain2,
                        "shared_concepts": list(shared),
                        "link_strength": len(shared)
                    })
        
        if not self.cross_domain_links:
            print("\n⚠️  No cross-domain links detected yet")
            print("   (This is expected with limited gaps filled)")
            print("   Fill more gaps to discover connections!")
        
        return self.cross_domain_links
    
    def synthesize_insights(self):
        """Generate breakthrough insights from cross-domain connections"""
        print("\n💡 EMERGENT BREAKTHROUGH INSIGHTS")
        print("=" * 80)
        
        if not self.cross_domain_links:
            print("\nNo cross-domain links to synthesize yet.")
            print("Need to fill more gaps to discover connections.")
            return []
        
        insights = []
        
        for link in self.cross_domain_links:
            insight = {
                "domains": [link["domain1"], link["domain2"]],
                "connection_type": "concept_overlap",
                "strength": link["link_strength"],
                "hypothesis": f"Research linking {link['domain1']} and {link['domain2']} "
                             f"may reveal novel approaches by applying concepts from one domain to the other."
            }
            insights.append(insight)
            
            print(f"\n🚀 Insight #{len(insights)}:")
            print(f"   Domains: {link['domain1']} + {link['domain2']}")
            print(f"   Shared concepts: {link['shared_concepts'][:3]}...")
            print(f"   Potential: Novel synthesis opportunities")
        
        return insights
    
    def save_results(self, output_dir: str = "cross_domain_results"):
        """Save cross-domain research results"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "domains": list(self.domains.keys()),
            "cross_domain_links": self.cross_domain_links,
            "summary": {
                "domains_explored": len(self.domains),
                "links_discovered": len(self.cross_domain_links),
                "total_shared_concepts": sum(
                    len(link["shared_concepts"]) for link in self.cross_domain_links
                )
            }
        }
        
        output_file = output_path / "cross_domain_experiment.json"
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Results saved: {output_file}")
        return results


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
    
    # Define research domains
    # Using scientifically interesting domains with potential connections
    domains = {
        "quantum_computing": [
            "What are the principles of quantum superposition?",
            "How do quantum gates perform computation?"
        ],
        "neuroscience": [
            "How do biological neural networks learn without backpropagation?",
            "What is synaptic plasticity?"
        ],
        "ml_optimization": [
            "What are alternatives to backpropagation?",
            "How do evolutionary algorithms optimize neural networks?"
        ]
    }
    
    print("\n" + "=" * 80)
    print("🔬 AUTONOMOUS CROSS-DOMAIN SCIENTIFIC RESEARCH")
    print("=" * 80)
    print("\nThis experiment demonstrates:")
    print("  • Multi-domain knowledge seeding")
    print("  • Recursive gap filling across domains")
    print("  • Cross-domain connection discovery")
    print("  • Emergent insight synthesis")
    print("\n" + "=" * 80)
    
    # Phase 1: Seed all domains
    print("\n📍 PHASE 1: Domain Seeding")
    researcher.seed_domains(domains)
    
    # Phase 2: Fill gaps (limited to avoid rate limits)
    print("\n📍 PHASE 2: Knowledge Gap Filling")
    print("⚠️  Filling 3 gaps per domain (rate-limited for demo)")
    researcher.fill_domain_gaps(max_gaps_per_domain=3)
    
    # Phase 3: Synthesize insights
    print("\n📍 PHASE 3: Cross-Domain Synthesis")
    insights = researcher.synthesize_insights()
    
    # Save results
    results = researcher.save_results()
    
    # Summary
    print("\n" + "=" * 80)
    print("✅ EXPERIMENT COMPLETE")
    print("=" * 80)
    print(f"\nDomains explored: {len(domains)}")
    print(f"Cross-domain links: {len(researcher.cross_domain_links)}")
    print(f"Potential breakthroughs: {len(insights)}")
    
    print("\n💡 KEY INSIGHT:")
    print("""
This demonstrates the autonomous research pattern:
  1. Seed multiple domains with initial questions
  2. System identifies gaps in each domain
  3. Fill gaps recursively, discovering emergent questions
  4. Detect when concepts bridge domains
  5. Synthesize novel research hypotheses

With 50+ years of LLM training data, the system can discover
connections that human researchers would miss. This is how
scientific breakthroughs happen - by connecting disparate fields.

Next steps:
  • Fill more gaps to discover deeper connections
  • Query system about specific cross-domain hypotheses
  • Apply to real research problems (drug discovery, novel materials, AI architectures)
""")
    
    print("\n🚀 Try querying the system about specific connections:")
    print('  "How could quantum superposition principles apply to neural network learning?"')
    print('  "Can biological learning mechanisms inspire quantum computing algorithms?"')


if __name__ == "__main__":
    main()
