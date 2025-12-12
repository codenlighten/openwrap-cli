#!/usr/bin/env python3
"""
Knowledge Evolution - Step 2: Gap Filling

Systematically fills knowledge gaps identified in Step 1,
demonstrating how the system discovers cross-domain connections
and emergent insights.

This simulates what would happen in a scientific research context:
- Start with high-level question
- System identifies what it doesn't know
- Fills those gaps recursively
- Discovers connections between disparate domains
- Surfaces insights invisible to single-domain analysis
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from lumen_sdk import LumenClient
from recursive_researcher import RecursiveResearcher


class GapFiller:
    """Fills knowledge gaps and tracks emergent insights"""
    
    def __init__(self, experiment_dir: str, client: LumenClient):
        self.experiment_dir = Path(experiment_dir) if isinstance(experiment_dir, str) else experiment_dir
        self.client = client
        self.researcher = RecursiveResearcher(client, max_depth=2)
        
        # Load existing experiment
        self.experiment_file = self.experiment_dir / "experiment.json"
        with open(self.experiment_file) as f:
            self.experiment = json.load(f)
        
        print(f"🔬 Knowledge Gap Filling - Step 2")
        print(f"Domain: {self.experiment['domain']}")
        print(f"Gaps to fill: {len(self.experiment['gaps'])}")
        print(f"{'='*70}\n")
    
    def fill_gaps(self, max_gaps: int = 5):
        """
        Fill top N knowledge gaps
        
        This is where cross-domain synthesis happens:
        - Each gap research may identify new gaps
        - Connections between gaps become visible
        - Domain boundaries dissolve
        - Emergent patterns surface
        """
        print("🧬 STEP 2: Filling Knowledge Gaps")
        print(f"Target: {max_gaps} gaps (rate-limited for API quota)\n")
        
        unfilled_gaps = [g for g in self.experiment['gaps'] if not g.get('filled')]
        gaps_to_fill = unfilled_gaps[:max_gaps]
        
        filled_count = 0
        emergent_insights = []
        cross_domain_links = []
        
        for i, gap_entry in enumerate(gaps_to_fill, 1):
            gap = gap_entry['gap']
            print(f"\n[{i}/{len(gaps_to_fill)}] Researching gap...")
            print(f"    {gap[:80]}...")
            print(f"    (Originally from: \"{gap_entry['discovered_by'][:50]}...\")")
            
            try:
                # Research the gap
                result = self.researcher.research(gap)
                
                # Track the filling
                gap_entry['filled'] = True
                gap_entry['filled_at'] = datetime.now().isoformat()
                gap_entry['response_length'] = len(result.get('response', ''))
                gap_entry['new_gaps_discovered'] = result.get('missing_context', [])
                
                print(f"    ✅ Filled: {gap_entry['response_length']} chars")
                
                # Detect emergent insights
                new_gaps = result.get('missing_context', [])
                if new_gaps:
                    print(f"    🌟 Discovered {len(new_gaps)} new gaps from filling this one")
                    
                    # Check for cross-domain connections
                    for new_gap in new_gaps:
                        # Simple heuristic: if new gap mentions concepts from different original queries
                        original_queries = set(g['discovered_by'] for g in self.experiment['gaps'])
                        if any(self._concepts_overlap(new_gap, orig_q) for orig_q in original_queries):
                            cross_domain_links.append({
                                "from_gap": gap,
                                "to_gap": new_gap,
                                "connection_type": "cross_domain_synthesis",
                                "timestamp": datetime.now().isoformat()
                            })
                            print(f"    🔗 Cross-domain link detected!")
                    
                    # Add new gaps to queue
                    for new_gap in new_gaps[:2]:  # Limit to avoid explosion
                        if new_gap not in [g['gap'] for g in self.experiment['gaps']]:
                            self.experiment['gaps'].append({
                                "gap": new_gap,
                                "discovered_by": f"filling: {gap[:50]}",
                                "timestamp": datetime.now().isoformat(),
                                "filled": False,
                                "generation": 2  # Second-order gap
                            })
                            emergent_insights.append(new_gap)
                
                filled_count += 1
                
                # Rate limiting
                time.sleep(1.5)
                
            except Exception as e:
                print(f"    ❌ Error: {e}")
                gap_entry['error'] = str(e)
        
        # Take snapshot
        self._take_snapshot("after_gap_filling", {
            "gaps_filled": filled_count,
            "emergent_insights": len(emergent_insights),
            "cross_domain_links": len(cross_domain_links)
        })
        
        print(f"\n{'='*70}")
        print(f"✅ Gap Filling Complete")
        print(f"   Gaps filled: {filled_count}")
        print(f"   Emergent insights: {len(emergent_insights)}")
        print(f"   Cross-domain links: {len(cross_domain_links)}")
        print(f"{'='*70}\n")
        
        return {
            "filled_count": filled_count,
            "emergent_insights": emergent_insights,
            "cross_domain_links": cross_domain_links
        }
    
    def _concepts_overlap(self, text1: str, text2: str) -> bool:
        """Simple concept overlap detection"""
        # Extract key terms (simplified - in production use NER/embeddings)
        terms1 = set(text1.lower().split())
        terms2 = set(text2.lower().split())
        overlap = terms1 & terms2
        return len(overlap) > 3  # More than 3 common words suggests connection
    
    def _take_snapshot(self, label: str, metrics: Dict[str, Any]):
        """Take a snapshot of current state"""
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "label": label,
            "queries_count": len(self.experiment['queries']),
            "gaps_total": len(self.experiment['gaps']),
            "gaps_filled": len([g for g in self.experiment['gaps'] if g.get('filled')]),
            "metrics": metrics
        }
        
        if 'snapshots' not in self.experiment:
            self.experiment['snapshots'] = []
        
        self.experiment['snapshots'].append(snapshot)
        
        # Save to file
        snapshot_file = self.experiment_dir / f"snapshot_{label}.json"
        with open(snapshot_file, 'w') as f:
            json.dump(snapshot, f, indent=2)
        
        print(f"📸 Snapshot saved: {label}")
    
    def analyze_knowledge_growth(self):
        """Analyze how knowledge has grown"""
        print("\n" + "="*70)
        print("📊 KNOWLEDGE GROWTH ANALYSIS")
        print("="*70)
        
        snapshots = self.experiment['snapshots']
        initial = snapshots[0]
        current = snapshots[-1]
        
        print(f"\nInitial State (after seeding):")
        print(f"  Queries: {initial['queries_count']}")
        print(f"  Gaps identified: {initial['gaps_identified']}")
        print(f"  Gaps filled: {initial['gaps_filled']}")
        
        print(f"\nCurrent State (after gap filling):")
        print(f"  Queries: {current['queries_count']}")
        print(f"  Gaps total: {current['gaps_total']}")
        print(f"  Gaps filled: {current['gaps_filled']}")
        
        if 'metrics' in current:
            print(f"  Emergent insights: {current['metrics'].get('emergent_insights', 0)}")
            print(f"  Cross-domain links: {current['metrics'].get('cross_domain_links', 0)}")
        
        # Calculate growth metrics
        gap_growth = current['gaps_total'] - initial['gaps_identified']
        fill_rate = (current['gaps_filled'] / current['gaps_total'] * 100) if current['gaps_total'] > 0 else 0
        
        print(f"\n📈 Growth Metrics:")
        print(f"  New gaps discovered: +{gap_growth} ({gap_growth / initial['gaps_identified'] * 100:.0f}% increase)")
        print(f"  Fill rate: {fill_rate:.1f}%")
        
        # Identify emergent patterns
        second_gen_gaps = [g for g in self.experiment['gaps'] if g.get('generation') == 2]
        if second_gen_gaps:
            print(f"\n🌟 Emergent Discoveries (2nd-order gaps):")
            for i, gap in enumerate(second_gen_gaps[:5], 1):
                print(f"  {i}. {gap['gap'][:70]}...")
                print(f"     (emerged from: \"{gap['discovered_by'][:60]}...\")")
    
    def save_experiment(self):
        """Save updated experiment"""
        with open(self.experiment_file, 'w') as f:
            json.dump(self.experiment, f, indent=2)
        
        print(f"\n💾 Experiment updated: {self.experiment_file}")


def main():
    """Run Step 2: Gap filling"""
    
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
    
    # Find most recent experiment
    experiments_dir = Path("knowledge_experiments")
    if not experiments_dir.exists():
        print("❌ No experiments found. Run knowledge_evolution.py first (Step 1)")
        return
    
    # Get latest experiment directory
    experiment_dirs = [d for d in experiments_dir.iterdir() if d.is_dir()]
    if not experiment_dirs:
        print("❌ No experiment directories found")
        return
    
    latest_experiment = max(experiment_dirs, key=lambda d: d.stat().st_mtime)
    
    print(f"🔬 Continuing experiment: {latest_experiment.name}")
    print(f"{'='*70}\n")
    
    # Create gap filler
    filler = GapFiller(latest_experiment, client)
    
    # Fill gaps
    results = filler.fill_gaps(max_gaps=5)
    
    # Analyze growth
    filler.analyze_knowledge_growth()
    
    # Save
    filler.save_experiment()
    
    print("\n" + "="*70)
    print("🎯 KEY INSIGHT")
    print("="*70)
    print("\nThis demonstrates the compound learning effect:")
    print("  1. Initial queries identified gaps")
    print("  2. Filling gaps discovered NEW gaps")
    print("  3. These 2nd-order gaps connect different domains")
    print("  4. Cross-domain synthesis creates emergent insights")
    print("\nIn scientific research, this is how breakthroughs happen:")
    print("  • Biology + Physics = Biophysics insights")
    print("  • Neuroscience + ML = Novel architectures")
    print("  • Quantum mechanics + Information theory = Quantum computing")
    print("\n💡 The system is doing autonomous cross-domain research!")
    
    if results['cross_domain_links']:
        print("\n🔗 Cross-Domain Connections Found:")
        for i, link in enumerate(results['cross_domain_links'][:3], 1):
            print(f"  {i}. {link['from_gap'][:50]}...")
            print(f"     → {link['to_gap'][:50]}...")


if __name__ == "__main__":
    main()
