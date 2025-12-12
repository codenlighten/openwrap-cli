#!/usr/bin/env python3
"""
Knowledge Evolution Experiment

Tracks how a knowledge base improves over time through:
1. Initial seeding with queries
2. Automatic gap identification
3. Background gap filling
4. Measurement of knowledge growth

Goal: Demonstrate compound learning effect empirically
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from lumen_sdk import LumenClient
from recursive_researcher import RecursiveResearcher


class KnowledgeEvolution:
    """Tracks and measures knowledge base evolution over time"""
    
    def __init__(self, client: LumenClient, domain: str):
        self.client = client
        self.domain = domain
        self.researcher = RecursiveResearcher(client, max_depth=2)
        
        # Storage
        self.experiment_dir = Path("knowledge_experiments") / domain.replace(" ", "_")
        self.experiment_dir.mkdir(parents=True, exist_ok=True)
        
        # Metrics
        self.queries_asked = []
        self.gaps_identified = []
        self.gaps_filled = []
        self.knowledge_snapshots = []
        
        print(f"📊 Knowledge Evolution Experiment")
        print(f"Domain: {domain}")
        print(f"Storage: {self.experiment_dir}")
        print(f"{'='*70}\n")
    
    def seed_knowledge(self, seed_queries: List[str]):
        """
        Step 1: Initial seeding with queries
        
        Ask initial questions to populate knowledge base and identify gaps
        """
        print("🌱 STEP 1: Seeding Knowledge Base")
        print(f"Processing {len(seed_queries)} initial queries...\n")
        
        for i, query in enumerate(seed_queries, 1):
            print(f"[{i}/{len(seed_queries)}] {query}")
            
            try:
                result = self.researcher.research(query)
                
                # Track query
                query_data = {
                    "timestamp": datetime.now().isoformat(),
                    "query": query,
                    "response_length": len(result.get('response', '')),
                    "missing_context": result.get('missing_context', []),
                    "gap_count": len(result.get('missing_context', []))
                }
                
                self.queries_asked.append(query_data)
                
                # Extract and track gaps
                for gap in result.get('missing_context', []):
                    if gap not in [g['gap'] for g in self.gaps_identified]:
                        self.gaps_identified.append({
                            "gap": gap,
                            "discovered_by": query,
                            "timestamp": datetime.now().isoformat(),
                            "filled": False
                        })
                
                print(f"   ✅ Response: {len(result.get('response', ''))} chars")
                print(f"   🔍 Gaps identified: {len(result.get('missing_context', []))}")
                
                # Rate limiting
                time.sleep(1)
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        # Take snapshot
        self._take_snapshot("after_seeding")
        
        print(f"\n{'='*70}")
        print(f"✅ Seeding Complete")
        print(f"   Queries processed: {len(self.queries_asked)}")
        print(f"   Unique gaps identified: {len(self.gaps_identified)}")
        print(f"{'='*70}\n")
        
        return self.gaps_identified
    
    def _take_snapshot(self, label: str):
        """Take a snapshot of current knowledge state"""
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "label": label,
            "queries_count": len(self.queries_asked),
            "gaps_identified": len(self.gaps_identified),
            "gaps_filled": len([g for g in self.gaps_identified if g.get('filled')]),
            "total_response_chars": sum(q['response_length'] for q in self.queries_asked)
        }
        
        self.knowledge_snapshots.append(snapshot)
        
        # Save to file
        snapshot_file = self.experiment_dir / f"snapshot_{label}.json"
        with open(snapshot_file, 'w') as f:
            json.dump(snapshot, f, indent=2)
        
        print(f"📸 Snapshot saved: {label}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current statistics"""
        return {
            "domain": self.domain,
            "queries_asked": len(self.queries_asked),
            "gaps_identified": len(self.gaps_identified),
            "gaps_filled": len([g for g in self.gaps_identified if g.get('filled')]),
            "snapshots": len(self.knowledge_snapshots)
        }
    
    def save_experiment(self):
        """Save complete experiment data"""
        experiment_data = {
            "domain": self.domain,
            "started": self.knowledge_snapshots[0]['timestamp'] if self.knowledge_snapshots else None,
            "queries": self.queries_asked,
            "gaps": self.gaps_identified,
            "snapshots": self.knowledge_snapshots,
            "stats": self.get_stats()
        }
        
        output_file = self.experiment_dir / "experiment.json"
        with open(output_file, 'w') as f:
            json.dump(experiment_data, f, indent=2)
        
        print(f"\n💾 Experiment saved to: {output_file}")
        return output_file


def main():
    """Run Step 1: Initial seeding experiment"""
    
    # Load client
    config_file = Path.home() / ".lumen" / "config.json"
    if not config_file.exists():
        print("❌ Not logged in. Please run: lumen-cli login")
        return
    
    with open(config_file) as f:
        config = json.load(f)
        token = config.get('token')
    
    if not token:
        print("❌ No token found. Please run: lumen-cli login")
        return
    
    client = LumenClient(token)
    
    # Choose domain
    domain = "Python FastAPI microservices"
    
    # Initial seed queries - more specific to trigger gap detection
    seed_queries = [
        "How do I implement authentication in FastAPI microservices?",
        "What's the best way to handle database connections in FastAPI?",
        "How should microservices communicate in a FastAPI architecture?"
    ]
    
    print(f"🧪 Starting Knowledge Evolution Experiment")
    print(f"Domain: {domain}")
    print(f"Seed queries: {len(seed_queries)}")
    print(f"{'='*70}\n")
    
    # Create experiment
    experiment = KnowledgeEvolution(client, domain)
    
    # Step 1: Seed knowledge
    gaps = experiment.seed_knowledge(seed_queries)
    
    # Show results
    print("\n" + "="*70)
    print("📊 EXPERIMENT RESULTS - STEP 1")
    print("="*70)
    
    stats = experiment.get_stats()
    print(f"\nDomain: {stats['domain']}")
    print(f"Queries Asked: {stats['queries_asked']}")
    print(f"Gaps Identified: {stats['gaps_identified']}")
    print(f"Gaps Filled: {stats['gaps_filled']}")
    
    print("\n🔍 Top 10 Knowledge Gaps Discovered:")
    for i, gap in enumerate(gaps[:10], 1):
        print(f"   {i}. {gap['gap'][:80]}...")
        print(f"      (discovered by: \"{gap['discovered_by']}\")")
    
    if len(gaps) > 10:
        print(f"   ... and {len(gaps) - 10} more gaps")
    
    # Save experiment
    output_file = experiment.save_experiment()
    
    print("\n" + "="*70)
    print("✅ STEP 1 COMPLETE")
    print("="*70)
    print("\nNext steps:")
    print("  1. Review identified knowledge gaps above")
    print("  2. Run Step 2 to fill top gaps (uses API calls)")
    print("  3. Measure knowledge improvement")
    print(f"\nExperiment data saved to: {output_file}")


if __name__ == "__main__":
    main()
