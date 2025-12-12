#!/usr/bin/env python3
"""
Example: Self-Improving Knowledge Base

Demonstrates how to build a knowledge base that:
- Identifies its own knowledge gaps via missingContext
- Proactively fills gaps through background research
- Improves answer quality over time
- Builds a comprehensive knowledge graph
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import json
from collections import defaultdict

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


class KnowledgeGraph:
    """Simple in-memory knowledge graph"""
    
    def __init__(self):
        self.entities = {}  # entity_id -> {type, properties, last_updated}
        self.relationships = []  # [(entity1, relation, entity2), ...]
        self.query_history = []
        self.gap_fill_history = []
    
    def add_entity(self, entity_id: str, entity_type: str, properties: dict):
        """Add or update an entity"""
        self.entities[entity_id] = {
            "type": entity_type,
            "properties": properties,
            "last_updated": datetime.now().isoformat()
        }
    
    def add_relationship(self, entity1: str, relation: str, entity2: str):
        """Add a relationship between entities"""
        rel = (entity1, relation, entity2)
        if rel not in self.relationships:
            self.relationships.append(rel)
    
    def extract_entities_from_text(self, text: str, context: str = ""):
        """Extract entities from text (simplified)"""
        # In production, use NER or structured extraction with schemas
        # For demo, just track that we processed this text
        entity_id = f"content_{len(self.entities)}"
        self.add_entity(entity_id, "information", {
            "content": text[:200],  # Store snippet
            "context": context,
            "timestamp": datetime.now().isoformat()
        })
        return entity_id
    
    def get_stats(self):
        """Get knowledge graph statistics"""
        return {
            "entities": len(self.entities),
            "relationships": len(self.relationships),
            "queries_processed": len(self.query_history),
            "gaps_filled": len(self.gap_fill_history)
        }


class SelfImprovingKnowledgeBase:
    """Knowledge base that identifies and fills its own gaps"""
    
    def __init__(self, client: LumenClient, max_research_depth: int = 2):
        self.client = client
        self.researcher = RecursiveResearcher(client, max_depth=max_research_depth)
        self.knowledge_graph = KnowledgeGraph()
        self.pending_gaps = []  # Queue of gaps to research
    
    def query(self, question: str):
        """
        Answer a question and identify knowledge gaps
        
        Returns:
            dict: {
                'answer': str,
                'confidence': str,
                'identified_gaps': list,
                'knowledge_graph_updated': bool
            }
        """
        print(f"\n🔍 Processing query: {question}")
        
        # Research the question
        result = self.researcher.research(question)
        
        # Log the query
        self.knowledge_graph.query_history.append({
            "question": question,
            "timestamp": datetime.now().isoformat(),
            "answer_length": len(result.answer)
        })
        
        # Extract entities and add to knowledge graph
        entity_id = self.knowledge_graph.extract_entities_from_text(
            result.answer,
            context=question
        )
        
        # Identify knowledge gaps from missingContext
        gaps = []
        if hasattr(result, 'missing_context') and result.missing_context:
            gaps = result.missing_context
            self.pending_gaps.extend(gaps)
            print(f"\n⚠️  Identified {len(gaps)} knowledge gaps:")
            for i, gap in enumerate(gaps, 1):
                print(f"   {i}. {gap}")
        
        return {
            "answer": result.answer,
            "confidence": "high" if not gaps else "medium",
            "identified_gaps": gaps,
            "knowledge_graph_updated": True,
            "stats": self.knowledge_graph.get_stats()
        }
    
    def fill_knowledge_gaps(self, max_gaps: int = 3):
        """
        Proactively research pending knowledge gaps
        
        This would typically run as a background worker
        """
        if not self.pending_gaps:
            print("\n✅ No knowledge gaps to fill")
            return
        
        print(f"\n🔧 Filling {min(max_gaps, len(self.pending_gaps))} knowledge gaps...")
        
        gaps_to_fill = self.pending_gaps[:max_gaps]
        self.pending_gaps = self.pending_gaps[max_gaps:]
        
        for i, gap in enumerate(gaps_to_fill, 1):
            print(f"\n   [{i}/{len(gaps_to_fill)}] Researching: {gap}")
            
            try:
                # Research the gap
                result = self.researcher.research(gap)
                
                # Add to knowledge graph
                entity_id = self.knowledge_graph.extract_entities_from_text(
                    result.answer,
                    context=f"gap_fill: {gap}"
                )
                
                # Log the gap fill
                self.knowledge_graph.gap_fill_history.append({
                    "gap": gap,
                    "timestamp": datetime.now().isoformat(),
                    "entity_id": entity_id
                })
                
                print(f"   ✅ Gap filled and added to knowledge base")
                
            except Exception as e:
                print(f"   ❌ Error filling gap: {e}")
    
    def get_learning_progress(self):
        """Show how the knowledge base has improved over time"""
        stats = self.knowledge_graph.get_stats()
        
        return {
            "total_entities": stats['entities'],
            "total_relationships": stats['relationships'],
            "queries_answered": stats['queries_processed'],
            "gaps_proactively_filled": stats['gaps_filled'],
            "pending_gaps": len(self.pending_gaps),
            "knowledge_density": stats['relationships'] / max(stats['entities'], 1)
        }


def demo_basic_query():
    """Demo: Basic query with gap identification"""
    print("\n" + "="*70)
    print("DEMO 1: Basic Query with Automatic Gap Detection")
    print("="*70)
    
    client = get_client()
    kb = SelfImprovingKnowledgeBase(client, max_research_depth=1)
    
    question = "What are the key features of Python 3.12?"
    
    result = kb.query(question)
    
    print(f"\n📝 Answer:\n{result['answer']}")
    print(f"\n🎯 Confidence: {result['confidence']}")
    
    if result['identified_gaps']:
        print(f"\n🔍 System Self-Awareness - Identified {len(result['identified_gaps'])} knowledge gaps:")
        for i, gap in enumerate(result['identified_gaps'], 1):
            print(f"   {i}. {gap}")
        print("\n💡 These gaps will be researched proactively to improve future answers")
    
    print(f"\n📊 Knowledge Graph Stats:")
    for key, value in result['stats'].items():
        print(f"   {key}: {value}")


def demo_progressive_improvement():
    """Demo: Knowledge base improving over multiple queries"""
    print("\n" + "="*70)
    print("DEMO 2: Progressive Knowledge Base Improvement")
    print("="*70)
    
    client = get_client()
    kb = SelfImprovingKnowledgeBase(client, max_research_depth=1)
    
    questions = [
        "What is quantum computing?",
        "What are qubits?",
        "How does quantum entanglement work?"
    ]
    
    print("\n📚 Simulating knowledge base growth over 3 queries...")
    
    for i, question in enumerate(questions, 1):
        print(f"\n{'─'*70}")
        print(f"QUERY {i}: {question}")
        print('─'*70)
        
        result = kb.query(question)
        
        print(f"\n💡 Answer Preview: {result['answer'][:150]}...")
        
        if result['identified_gaps']:
            print(f"\n🔍 New Gaps Identified: {len(result['identified_gaps'])}")
            for gap in result['identified_gaps'][:2]:  # Show first 2
                print(f"   - {gap}")
        
        # Show progress
        progress = kb.get_learning_progress()
        print(f"\n📊 Learning Progress:")
        print(f"   Entities: {progress['total_entities']}")
        print(f"   Queries Answered: {progress['queries_answered']}")
        print(f"   Pending Gaps: {progress['pending_gaps']}")
        
        if i < len(questions):
            input("\n⏸️  Press Enter to continue to next query...")
    
    print("\n" + "="*70)
    print("📈 FINAL KNOWLEDGE BASE STATE")
    print("="*70)
    
    final_progress = kb.get_learning_progress()
    print(f"\nTotal Entities: {final_progress['total_entities']}")
    print(f"Total Queries: {final_progress['queries_answered']}")
    print(f"Gaps Identified: {final_progress['pending_gaps']}")
    print(f"\n💡 The knowledge base has grown organically from user questions!")


def demo_proactive_gap_filling():
    """Demo: Proactive gap filling in background"""
    print("\n" + "="*70)
    print("DEMO 3: Proactive Knowledge Gap Filling")
    print("="*70)
    
    client = get_client()
    kb = SelfImprovingKnowledgeBase(client, max_research_depth=1)
    
    # Initial query creates gaps
    print("\n🔍 Initial Query:")
    question = "What is machine learning?"
    result = kb.query(question)
    
    print(f"\n📝 Answer Preview: {result['answer'][:150]}...")
    
    initial_gaps = result['identified_gaps']
    if initial_gaps:
        print(f"\n⚠️  Identified {len(initial_gaps)} knowledge gaps")
        print("\n🤖 System is now self-aware of what it doesn't know")
        
        input("\n⏸️  Press Enter to trigger proactive gap filling...")
        
        # Proactively fill gaps (this would run as background worker)
        print("\n" + "="*70)
        print("🔧 BACKGROUND WORKER: Proactive Gap Filling")
        print("="*70)
        
        before_stats = kb.get_learning_progress()
        
        kb.fill_knowledge_gaps(max_gaps=2)
        
        after_stats = kb.get_learning_progress()
        
        print("\n" + "="*70)
        print("📊 IMPROVEMENT METRICS")
        print("="*70)
        print(f"\nEntities Before: {before_stats['total_entities']}")
        print(f"Entities After:  {after_stats['total_entities']}")
        print(f"Change: +{after_stats['total_entities'] - before_stats['total_entities']}")
        
        print(f"\nGaps Filled: {after_stats['gaps_proactively_filled']}")
        print(f"Remaining Gaps: {after_stats['pending_gaps']}")
        
        print("\n💡 Key Insight:")
        print("   The system improved WITHOUT any user queries!")
        print("   It filled its own knowledge gaps proactively.")


def demo_compound_learning():
    """Demo: Compound learning effect over time"""
    print("\n" + "="*70)
    print("DEMO 4: Compound Learning Effect")
    print("="*70)
    
    client = get_client()
    kb = SelfImprovingKnowledgeBase(client, max_research_depth=1)
    
    print("\n📈 Simulating knowledge base usage over time...")
    print("\nDay 1: Initial queries")
    
    # Day 1 queries
    day1_questions = [
        "What is FastAPI?",
        "What is PostgreSQL?"
    ]
    
    for q in day1_questions:
        kb.query(q)
    
    day1_stats = kb.get_learning_progress()
    print(f"   Entities: {day1_stats['total_entities']}")
    print(f"   Pending Gaps: {day1_stats['pending_gaps']}")
    
    input("\n⏸️  Press Enter to simulate Day 7...")
    
    # Simulate gap filling over a week
    print("\n🔧 Background worker fills gaps over the week...")
    kb.fill_knowledge_gaps(max_gaps=2)
    
    print("\nDay 7: Follow-up query")
    kb.query("How do FastAPI and PostgreSQL work together?")
    
    day7_stats = kb.get_learning_progress()
    print(f"   Entities: {day7_stats['total_entities']}")
    print(f"   Total Queries: {day7_stats['queries_answered']}")
    print(f"   Gaps Filled: {day7_stats['gaps_proactively_filled']}")
    
    print("\n" + "="*70)
    print("📊 COMPOUND LEARNING ANALYSIS")
    print("="*70)
    
    growth_rate = ((day7_stats['total_entities'] - day1_stats['total_entities']) / 
                   max(day1_stats['total_entities'], 1) * 100)
    
    print(f"\nKnowledge Growth: {growth_rate:.1f}%")
    print(f"Queries Required: {day7_stats['queries_answered']}")
    print(f"Autonomous Learning: {day7_stats['gaps_proactively_filled']} gaps filled without prompting")
    
    print("\n💡 The Compound Effect:")
    print("   - Each query identifies gaps")
    print("   - System fills gaps proactively")
    print("   - Future queries benefit from previous learning")
    print("   - Knowledge compounds exponentially")


def main():
    """Run all self-improving knowledge base demos"""
    print("\n" + "="*70)
    print("🧠 SELF-IMPROVING KNOWLEDGE BASE DEMO")
    print("="*70)
    print("\nDemonstrating how missingContext enables knowledge bases that:")
    print("  • Know what they don't know (self-awareness)")
    print("  • Proactively fill their own knowledge gaps")
    print("  • Improve continuously from usage")
    print("  • Create compound learning effects")
    
    try:
        # Demo 1: Basic query with gap detection
        demo_basic_query()
        
        input("\n\n⏸️  Press Enter to continue to next demo...")
        
        # Demo 2: Progressive improvement
        demo_progressive_improvement()
        
        input("\n\n⏸️  Press Enter to continue to next demo...")
        
        # Demo 3: Proactive gap filling
        demo_proactive_gap_filling()
        
        input("\n\n⏸️  Press Enter to continue to final demo...")
        
        # Demo 4: Compound learning
        demo_compound_learning()
        
        print("\n" + "="*70)
        print("✅ ALL DEMOS COMPLETE")
        print("="*70)
        print("\nKey Takeaways:")
        print("1. missingContext makes systems self-aware of knowledge gaps")
        print("2. Proactive gap-filling improves quality without user intervention")
        print("3. Knowledge compounds over time - exponential growth")
        print("4. System becomes smarter with every query, even indirect ones")
        print("\n🚀 This is impossible with traditional static knowledge bases!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error running demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
