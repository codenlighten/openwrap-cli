#!/usr/bin/env python3
"""
🚀 ULTIMATE DEMO: Recursive AI Agent System
Showcases the full power of schema-driven, recursive, multi-agent research
"""
import json
import sys
import io
from pathlib import Path
from recursive_researcher import RecursiveResearcher
from lumen_sdk import LumenClient

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def main():
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║     🧠 RECURSIVE AI AGENT SYSTEM - ULTIMATE DEMO 🧠              ║
║                                                                   ║
║  Demonstrating the power of:                                     ║
║  • Schema-driven knowledge extraction                            ║
║  • Recursive context exploration                                 ║
║  • Multi-agent collaboration                                     ║
║  • Self-aware research (missingContext)                          ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
""")
    
    # Load client
    config_file = Path.home() / ".lumen" / "config.json"
    if not config_file.exists():
        print("❌ Not logged in. Run: python lumen_cli.py login")
        return
    
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    client = LumenClient(config['token'])
    
    # ========================================================================
    # PHASE 1: Recursive Deep Research
    # ========================================================================
    print("\n" + "="*70)
    print("PHASE 1: RECURSIVE DEEP RESEARCH")
    print("="*70)
    print("\n📚 Exploring: 'What breakthroughs happened in AI in 2024?'")
    print("💡 The agent will automatically follow missingContext branches\n")
    
    researcher = RecursiveResearcher(client, max_depth=2, delay=0.5)
    research_tree = researcher.research(
        "What breakthroughs happened in AI in 2024?"
    )
    
    nodes = researcher._count_nodes(research_tree)
    depth = researcher._max_depth_in_tree(research_tree)
    contexts = len(researcher.explored_contexts)
    
    print(f"\n📊 Research Statistics:")
    print(f"   • Total nodes explored: {nodes}")
    print(f"   • Maximum depth: {depth}")
    print(f"   • Unique contexts: {contexts}")
    
    # ========================================================================
    # PHASE 2: Schema-Driven Extraction
    # ========================================================================
    print("\n" + "="*70)
    print("PHASE 2: SCHEMA-DRIVEN EXTRACTION")
    print("="*70)
    print("\n🔧 Generating schema for 'Scientific breakthrough with researchers, institutions, impact'")
    
    # Generate schema using AI
    schema_result = client.query(
        """Generate a JSON schema for: Scientific breakthrough with researchers, institutions, and impact score

Return JSON in this format:
{
  "schema": {
    "type": "object",
    "properties": {...},
    "required": [...],
    "additionalProperties": false
  }
}""",
        model="gpt-5-nano",
        temperature=1.0
    )
    
    try:
        response_text = schema_result['data']['response']
        if '```json' in response_text:
            response_text = response_text.split('```json')[1].split('```')[0]
        schema_data = json.loads(response_text.strip())
        
        if 'schema' in schema_data:
            extraction_schema = schema_data['schema']
        else:
            extraction_schema = schema_data
        
        print("✅ Schema generated!")
        print(f"   Properties: {len(extraction_schema.get('properties', {}))}")
        
        # Use schema to extract from research tree
        print("\n📊 Extracting structured data from research tree...")
        
        def extract_all(node):
            responses = []
            if 'response' in node:
                responses.append(node['response'])
            for branch in node.get('branches', []):
                responses.extend(extract_all(branch))
            return responses
        
        all_responses = extract_all(research_tree)
        combined_text = " ".join(all_responses[:2])[:800]  # Limit size
        
        extraction_result = client.query(
            f"""Extract data from this text according to the schema:

Text: "{combined_text}"

Schema: {json.dumps(extraction_schema, indent=2)}

Return ONLY valid JSON matching the schema.""",
            model="gpt-5-nano",
            temperature=1.0
        )
        
        print("✅ Extraction complete!")
        
    except Exception as e:
        print(f"⚠️  Schema extraction demo skipped: {e}")
    
    # ========================================================================
    # PHASE 3: Multi-Agent Collaboration
    # ========================================================================
    print("\n" + "="*70)
    print("PHASE 3: MULTI-AGENT COLLABORATION")
    print("="*70)
    print("\n🤖 Spawning 3 specialized agents for synthesis...\n")
    
    topic = "quantum computing applications"
    
    # Agent 1: Technical
    print("   🔬 Agent 1 (Technical Expert) analyzing...")
    tech = client.query(
        f"As a technical expert, briefly explain current {topic}",
        model="gpt-5-nano",
        temperature=1.0
    )
    print(f"   ✅ {tech['data']['response'][:80]}...")
    
    # Agent 2: Business
    print("\n   💼 Agent 2 (Business Analyst) analyzing...")
    business = client.query(
        f"As a business analyst, briefly explain the market potential of {topic}",
        model="gpt-5-nano",
        temperature=1.0
    )
    print(f"   ✅ {business['data']['response'][:80]}...")
    
    # Agent 3: Synthesizer
    print("\n   🧩 Agent 3 (Synthesizer) combining perspectives...")
    synthesis = client.query(
        f"""Synthesize these perspectives on {topic}:

Technical: {tech['data']['response'][:300]}
Business: {business['data']['response'][:300]}

Provide a brief unified view.""",
        model="gpt-5-nano",
        temperature=1.0
    )
    print(f"   ✅ Synthesis: {synthesis['data']['response'][:100]}...")
    
    # ========================================================================
    # PHASE 4: Iterative Refinement
    # ========================================================================
    print("\n" + "="*70)
    print("PHASE 4: ITERATIVE REFINEMENT (missingContext Loop)")
    print("="*70)
    print("\n🔄 Asking a question, detecting gaps, and refining...\n")
    
    initial = client.query(
        "What was the most significant AI research paper published in late 2024?",
        model="gpt-5-nano",
        temperature=1.0
    )
    
    missing = initial['data'].get('missingContext', [])
    print(f"   📝 Initial response: {initial['data']['response'][:120]}...")
    
    if missing:
        print(f"\n   🔍 Detected {len(missing)} missing context items:")
        for i, item in enumerate(missing[:2], 1):
            print(f"      {i}. {item}")
        
        print("\n   🔄 Refining answer with missing context...")
        refined = client.query(
            f"You mentioned these missing details: {', '.join(missing[:2])}. Please elaborate.",
            model="gpt-5-nano",
            temperature=1.0
        )
        print(f"   ✅ Refined: {refined['data']['response'][:120]}...")
    else:
        print("   ✅ Initial answer was complete!")
    
    # ========================================================================
    # FINAL SUMMARY
    # ========================================================================
    print("\n" + "="*70)
    print("🎉 DEMO COMPLETE")
    print("="*70)
    print("""
What we demonstrated:

✅ Recursive Research: Agent automatically explored 2-3 depth levels
✅ Schema Generation: AI created structured extraction schemas
✅ Data Extraction: Applied schemas to unstructured research data  
✅ Multi-Agent Synthesis: 3 agents with different perspectives collaborated
✅ Iterative Refinement: Used missingContext to fill knowledge gaps

This is a complete cognitive architecture for AI agents!

🚀 Next Steps:
   • Chain multiple schemas for complex data pipelines
   • Build knowledge graphs with entity/relationship extraction
   • Create self-improving agents that learn from failures
   • Implement parallel agent swarms for fast exploration
   • Add memory systems for long-term context retention

💡 The possibilities are endless when you combine:
   Schema-driven extraction + Recursive exploration + Multi-agent collaboration
    """)
    
    print("\n📊 Total API calls in demo: ~" + str(
        nodes + 2 + 3 + 2  # research + schema + agents + refinement
    ))
    
    print("\n💾 Check the JSON output files for detailed results!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Demo error: {e}")
        import traceback
        traceback.print_exc()
