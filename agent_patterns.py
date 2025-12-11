#!/usr/bin/env python3
"""
Example: Agent Orchestration Patterns
Demonstrates practical uses of recursive research and schema-driven pipelines
"""
import json
import sys
import io
from pathlib import Path
from recursive_researcher import RecursiveResearcher
from lumen_sdk import LumenClient

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def get_client():
    """Get authenticated client"""
    config_file = Path.home() / ".lumen" / "config.json"
    if not config_file.exists():
        print("❌ Not logged in. Run: python lumen_cli.py login")
        sys.exit(1)
    
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    return LumenClient(config['token'])


def example_knowledge_graph_builder():
    """
    Build a knowledge graph by recursively exploring a topic.
    Extract entities and relationships at each level.
    """
    print("=" * 70)
    print("KNOWLEDGE GRAPH BUILDER")
    print("=" * 70)
    
    client = get_client()
    researcher = RecursiveResearcher(client, max_depth=2, delay=0.5)
    
    # Schema for extracting entities and relationships
    entity_schema = {
        "type": "object",
        "properties": {
            "entities": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "type": {"type": "string", "enum": ["person", "organization", "concept", "technology"]},
                        "description": {"type": "string"}
                    },
                    "required": ["name", "type"]
                }
            },
            "relationships": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "from": {"type": "string"},
                        "to": {"type": "string"},
                        "type": {"type": "string"}
                    }
                }
            }
        },
        "additionalProperties": False
    }
    
    query = "Explain neural networks and their key components"
    print(f"\n🎯 Building knowledge graph for: {query}\n")
    
    # Research with entity extraction
    result = researcher.research(query, schema=entity_schema)
    
    print("\n" + "=" * 70)
    print("KNOWLEDGE GRAPH")
    print("=" * 70)
    
    # Collect all extracted entities
    all_entities = []
    all_relationships = []
    
    def collect_from_node(node):
        if 'extracted_data' in node:
            data = node['extracted_data']
            if 'entities' in data:
                all_entities.extend(data['entities'])
            if 'relationships' in data:
                all_relationships.extend(data['relationships'])
        
        for branch in node.get('branches', []):
            collect_from_node(branch)
    
    collect_from_node(result)
    
    print(f"\n📊 Extracted {len(all_entities)} entities")
    print(f"🔗 Found {len(all_relationships)} relationships")
    
    if all_entities:
        print("\n🏷️  Sample Entities:")
        for entity in all_entities[:5]:
            print(f"  • {entity.get('name', 'Unknown')} ({entity.get('type', 'unknown')})")
    
    # Save graph
    graph = {
        "query": query,
        "entities": all_entities,
        "relationships": all_relationships,
        "research_tree": result
    }
    
    with open("knowledge_graph.json", 'w') as f:
        json.dump(graph, f, indent=2)
    
    print("\n💾 Knowledge graph saved to: knowledge_graph.json")
    return graph


def example_comparative_analysis():
    """
    Compare two topics by researching them in parallel and extracting structured comparisons.
    """
    print("=" * 70)
    print("COMPARATIVE ANALYSIS")
    print("=" * 70)
    
    client = get_client()
    researcher = RecursiveResearcher(client, max_depth=1, delay=0.5)
    
    topic1 = "Python programming language"
    topic2 = "JavaScript programming language"
    
    print(f"\n🔬 Comparing: {topic1} vs {topic2}\n")
    
    # Research both topics
    print("📚 Researching topic 1...")
    result1 = researcher.research(f"What are the key features and use cases of {topic1}?")
    
    print("\n📚 Researching topic 2...")
    researcher.explored_contexts.clear()  # Reset for fresh research
    result2 = researcher.research(f"What are the key features and use cases of {topic2}?")
    
    # Now ask for a comparison
    print("\n⚖️  Generating comparison...")
    comparison_query = f"""Compare these two programming languages:

Topic 1 ({topic1}):
{result1.get('response', '')[:500]}

Topic 2 ({topic2}):
{result2.get('response', '')[:500]}

Provide a structured comparison."""
    
    comparison = client.query(comparison_query, model="gpt-5-nano", temperature=1.0)
    
    print("\n" + "=" * 70)
    print("COMPARISON RESULT")
    print("=" * 70)
    print(comparison['data']['response'])
    
    result = {
        "topic1": {"name": topic1, "research": result1},
        "topic2": {"name": topic2, "research": result2},
        "comparison": comparison['data']['response']
    }
    
    with open("comparison_analysis.json", 'w') as f:
        json.dump(result, f, indent=2)
    
    print("\n💾 Analysis saved to: comparison_analysis.json")
    return result


def example_iterative_refinement():
    """
    Iteratively refine an answer by using missingContext to guide follow-up questions.
    """
    print("=" * 70)
    print("ITERATIVE REFINEMENT")
    print("=" * 70)
    
    client = get_client()
    
    query = "How does blockchain technology work?"
    print(f"\n🎯 Initial Query: {query}\n")
    
    # Start with initial query
    result = client.query(query, model="gpt-5-nano", temperature=1.0)
    
    print("📝 Initial Response:")
    print(result['data']['response'][:300] + "...\n")
    
    missing = result['data'].get('missingContext', [])
    
    if missing:
        print(f"🔍 Found {len(missing)} missing context items:")
        for i, item in enumerate(missing[:3], 1):
            print(f"  {i}. {item}")
        
        # Use missing context to refine
        print("\n🔄 Refining with missing context...\n")
        
        refinement_query = f"""You previously answered: "{result['data']['response'][:200]}..."

You indicated these missing context items: {', '.join(missing[:2])}

Please provide a more complete answer addressing these missing pieces."""
        
        refined = client.query(refinement_query, model="gpt-5-nano", temperature=1.0)
        
        print("✅ Refined Response:")
        print(refined['data']['response'][:300] + "...")
        
        result = {
            "initial_query": query,
            "initial_response": result['data']['response'],
            "missing_context": missing,
            "refined_response": refined['data']['response']
        }
    else:
        print("✅ Initial response was complete (no missing context)")
        result = {
            "initial_query": query,
            "initial_response": result['data']['response'],
            "missing_context": []
        }
    
    with open("iterative_refinement.json", 'w') as f:
        json.dump(result, f, indent=2)
    
    print("\n💾 Refinement saved to: iterative_refinement.json")
    return result


def example_multi_agent_synthesis():
    """
    Use multiple agents with different roles to synthesize comprehensive answers.
    """
    print("=" * 70)
    print("MULTI-AGENT SYNTHESIS")
    print("=" * 70)
    
    client = get_client()
    
    topic = "impact of artificial intelligence on healthcare"
    print(f"\n🎯 Topic: {topic}\n")
    
    # Agent 1: Technical perspective
    print("🤖 Agent 1 (Technical Expert)...")
    tech_prompt = f"As a technical expert, explain the {topic} focusing on the technologies and methods involved."
    tech_result = client.query(tech_prompt, model="gpt-5-nano", temperature=1.0)
    tech_response = tech_result['data']['response']
    print(f"✅ Response: {tech_response[:150]}...\n")
    
    # Agent 2: Ethical perspective
    print("🤖 Agent 2 (Ethics Specialist)...")
    ethics_prompt = f"As an ethics specialist, discuss the {topic} focusing on ethical considerations and societal impacts."
    ethics_result = client.query(ethics_prompt, model="gpt-5-nano", temperature=1.0)
    ethics_response = ethics_result['data']['response']
    print(f"✅ Response: {ethics_response[:150]}...\n")
    
    # Agent 3: Synthesizer
    print("🤖 Agent 3 (Synthesizer)...")
    synthesis_prompt = f"""Synthesize these two perspectives on {topic}:

Technical View: {tech_response[:400]}

Ethical View: {ethics_response[:400]}

Provide a balanced synthesis highlighting how these perspectives complement each other."""
    
    synthesis = client.query(synthesis_prompt, model="gpt-5-nano", temperature=1.0)
    
    print("\n" + "=" * 70)
    print("SYNTHESIZED RESULT")
    print("=" * 70)
    print(synthesis['data']['response'])
    
    result = {
        "topic": topic,
        "technical_perspective": tech_response,
        "ethical_perspective": ethics_response,
        "synthesis": synthesis['data']['response']
    }
    
    with open("multi_agent_synthesis.json", 'w') as f:
        json.dump(result, f, indent=2)
    
    print("\n💾 Synthesis saved to: multi_agent_synthesis.json")
    return result


if __name__ == "__main__":
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        
        if mode == "graph":
            example_knowledge_graph_builder()
        elif mode == "compare":
            example_comparative_analysis()
        elif mode == "refine":
            example_iterative_refinement()
        elif mode == "synthesis":
            example_multi_agent_synthesis()
        else:
            print("Usage: python agent_patterns.py [graph|compare|refine|synthesis]")
            print("\nModes:")
            print("  graph     - Build knowledge graph with entities and relationships")
            print("  compare   - Compare two topics with structured analysis")
            print("  refine    - Iteratively refine answers using missingContext")
            print("  synthesis - Multi-agent synthesis with different perspectives")
    else:
        print("Select a mode:")
        print("  python agent_patterns.py graph")
        print("  python agent_patterns.py compare")
        print("  python agent_patterns.py refine")
        print("  python agent_patterns.py synthesis")
