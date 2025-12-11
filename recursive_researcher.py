#!/usr/bin/env python3
"""
Recursive Research Agent - Exploits missingContext for deep knowledge discovery
"""
import json
import time
from typing import List, Dict, Any, Set
from lumen_sdk import LumenClient


class RecursiveResearcher:
    """
    Agent that recursively explores missingContext to build comprehensive knowledge.
    Uses schema-driven extraction to structure findings at each depth level.
    """
    
    def __init__(self, client: LumenClient, max_depth: int = 3, delay: float = 0.5):
        self.client = client
        self.max_depth = max_depth
        self.delay = delay  # Rate limiting between requests
        self.explored_contexts: Set[str] = set()  # Avoid re-exploring
        
    def research(self, query: str, schema: Dict[str, Any] = None, depth: int = 0) -> Dict[str, Any]:
        """
        Recursively research a query, exploring all missing context branches.
        
        Args:
            query: The research question
            schema: Optional schema for structured extraction
            depth: Current recursion depth (internal)
            
        Returns:
            Dictionary with response, context tree, and all explored branches
        """
        print(f"{'  ' * depth}🔍 Depth {depth}: {query[:60]}...")
        
        # Prevent infinite recursion
        if depth >= self.max_depth:
            print(f"{'  ' * depth}⚠️  Max depth reached")
            return {"query": query, "depth": depth, "max_depth_reached": True}
        
        # Avoid re-exploring the same context
        query_key = query.lower().strip()
        if query_key in self.explored_contexts:
            print(f"{'  ' * depth}↩️  Already explored")
            return {"query": query, "depth": depth, "cached": True}
        
        self.explored_contexts.add(query_key)
        
        # Rate limiting
        if depth > 0:
            time.sleep(self.delay)
        
        # Query the API
        try:
            result = self.client.query(
                query=query,
                model="gpt-5-nano",
                temperature=1.0
            )
            
            if not result or 'data' not in result:
                print(f"{'  ' * depth}❌ Query failed")
                return {"query": query, "depth": depth, "error": "Query failed"}
            
            response = result['data']['response']
            missing_context = result['data'].get('missingContext', [])
            
            print(f"{'  ' * depth}✅ Got response ({len(response)} chars)")
            if missing_context:
                print(f"{'  ' * depth}📋 Found {len(missing_context)} missing context items")
            
            # Build result node
            node = {
                "query": query,
                "depth": depth,
                "response": response,
                "missing_context": missing_context,
                "usage": result.get('usage', {}),
                "branches": []
            }
            
            # If schema provided, extract structured data
            if schema:
                extracted = self._extract_with_schema(response, schema, depth)
                if extracted:
                    node["extracted_data"] = extracted
            
            # Recursively explore missing context branches
            if missing_context and depth < self.max_depth:
                for i, context_item in enumerate(missing_context[:3]):  # Limit branches
                    print(f"{'  ' * depth}🌿 Branch {i+1}/{len(missing_context[:3])}: {context_item[:50]}...")
                    branch = self.research(context_item, schema, depth + 1)
                    node["branches"].append(branch)
            
            return node
            
        except Exception as e:
            print(f"{'  ' * depth}❌ Error: {e}")
            return {"query": query, "depth": depth, "error": str(e)}
    
    def _extract_with_schema(self, text: str, schema: Dict[str, Any], depth: int) -> Dict[str, Any]:
        """Extract structured data using a schema"""
        try:
            prompt = f"""Extract data from this text according to the schema:

Text: "{text[:500]}..."

Schema: {json.dumps(schema, indent=2)}

Return ONLY valid JSON matching the schema."""
            
            time.sleep(self.delay)
            result = self.client.query(prompt, model="gpt-5-nano", temperature=1.0)
            
            if result and 'data' in result:
                response_text = result['data']['response']
                
                # Extract JSON from response
                if '```json' in response_text:
                    response_text = response_text.split('```json')[1].split('```')[0]
                elif '```' in response_text:
                    response_text = response_text.split('```')[1].split('```')[0]
                
                extracted = json.loads(response_text.strip())
                print(f"{'  ' * depth}📊 Extracted structured data")
                return extracted
                
        except Exception as e:
            print(f"{'  ' * depth}⚠️  Extraction failed: {e}")
        
        return None
    
    def research_with_parallel_schemas(self, query: str, schemas: Dict[str, Dict]) -> Dict[str, Any]:
        """
        Research with multiple extraction schemas applied in parallel.
        Each schema captures different aspects of the knowledge.
        """
        print(f"🔬 Multi-schema research: {query}")
        print(f"📐 Schemas: {', '.join(schemas.keys())}")
        
        # Get base research tree
        base_tree = self.research(query)
        
        # Apply each schema to extract different structured views
        extracted_views = {}
        for schema_name, schema in schemas.items():
            print(f"\n📊 Applying {schema_name} schema...")
            extracted = self._extract_from_tree(base_tree, schema)
            extracted_views[schema_name] = extracted
        
        return {
            "query": query,
            "research_tree": base_tree,
            "structured_views": extracted_views,
            "total_nodes": self._count_nodes(base_tree),
            "max_depth_reached": self._max_depth_in_tree(base_tree)
        }
    
    def _extract_from_tree(self, node: Dict[str, Any], schema: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Recursively extract structured data from all nodes in research tree"""
        extractions = []
        
        if 'response' in node:
            extracted = self._extract_with_schema(node['response'], schema, node.get('depth', 0))
            if extracted:
                extractions.append({
                    "depth": node.get('depth', 0),
                    "query": node.get('query', ''),
                    "data": extracted
                })
        
        # Recurse into branches
        for branch in node.get('branches', []):
            extractions.extend(self._extract_from_tree(branch, schema))
        
        return extractions
    
    def _count_nodes(self, node: Dict[str, Any]) -> int:
        """Count total nodes in research tree"""
        count = 1
        for branch in node.get('branches', []):
            count += self._count_nodes(branch)
        return count
    
    def _max_depth_in_tree(self, node: Dict[str, Any]) -> int:
        """Find maximum depth reached in tree"""
        max_depth = node.get('depth', 0)
        for branch in node.get('branches', []):
            max_depth = max(max_depth, self._max_depth_in_tree(branch))
        return max_depth
    
    def save_research(self, research_result: Dict[str, Any], filename: str):
        """Save research tree to JSON file"""
        with open(filename, 'w') as f:
            json.dump(research_result, f, indent=2)
        print(f"\n💾 Research saved to: {filename}")
    
    def print_tree(self, node: Dict[str, Any], show_responses: bool = False):
        """Print research tree in readable format"""
        depth = node.get('depth', 0)
        indent = '  ' * depth
        
        print(f"{indent}{'└─' if depth > 0 else ''}🔍 {node.get('query', 'Unknown')[:60]}")
        
        if show_responses and 'response' in node:
            response_preview = node['response'][:100].replace('\n', ' ')
            print(f"{indent}   💬 {response_preview}...")
        
        if 'extracted_data' in node:
            print(f"{indent}   📊 Structured data extracted")
        
        if 'missing_context' in node and node['missing_context']:
            print(f"{indent}   📋 Missing: {len(node['missing_context'])} items")
        
        # Recurse into branches
        for branch in node.get('branches', []):
            self.print_tree(branch, show_responses)


def example_deep_research():
    """Example: Deep research on a topic"""
    # Load token from config
    from pathlib import Path
    config_file = Path.home() / ".lumen" / "config.json"
    if not config_file.exists():
        print("❌ Not logged in. Run: python lumen_cli.py login")
        return None
    
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    client = LumenClient(config['token'])
    researcher = RecursiveResearcher(client, max_depth=3, delay=0.5)
    
    print("=" * 70)
    print("RECURSIVE RESEARCH AGENT - Deep Knowledge Discovery")
    print("=" * 70)
    
    query = "What are the key challenges in quantum computing?"
    
    print(f"\n🎯 Research Question: {query}\n")
    
    result = researcher.research(query)
    
    print("\n" + "=" * 70)
    print("RESEARCH TREE")
    print("=" * 70)
    researcher.print_tree(result, show_responses=True)
    
    print("\n" + "=" * 70)
    print("STATISTICS")
    print("=" * 70)
    print(f"Total nodes explored: {researcher._count_nodes(result)}")
    print(f"Maximum depth reached: {researcher._max_depth_in_tree(result)}")
    print(f"Unique contexts explored: {len(researcher.explored_contexts)}")
    
    # Save results
    researcher.save_research(result, "research_quantum_computing.json")
    
    return result


def example_multi_schema_research():
    """Example: Research with multiple extraction schemas"""
    # Load token from config
    from pathlib import Path
    config_file = Path.home() / ".lumen" / "config.json"
    if not config_file.exists():
        print("❌ Not logged in. Run: python lumen_cli.py login")
        return None
    
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    client = LumenClient(config['token'])
    researcher = RecursiveResearcher(client, max_depth=2, delay=0.5)
    
    print("=" * 70)
    print("MULTI-SCHEMA RESEARCH - Parallel Knowledge Extraction")
    print("=" * 70)
    
    query = "Explain the impact of artificial intelligence on healthcare"
    
    # Define multiple schemas for different extraction perspectives
    schemas = {
        "key_points": {
            "type": "object",
            "properties": {
                "main_points": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "technologies": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "required": ["main_points"],
            "additionalProperties": False
        },
        "entities": {
            "type": "object",
            "properties": {
                "organizations": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "people": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "locations": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "additionalProperties": False
        },
        "timeline": {
            "type": "object",
            "properties": {
                "events": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "year": {"type": "string"},
                            "event": {"type": "string"}
                        }
                    }
                }
            },
            "additionalProperties": False
        }
    }
    
    result = researcher.research_with_parallel_schemas(query, schemas)
    
    print("\n" + "=" * 70)
    print("STRUCTURED VIEWS")
    print("=" * 70)
    
    for view_name, extractions in result['structured_views'].items():
        print(f"\n📊 {view_name.upper()} VIEW:")
        print(f"   Extracted from {len(extractions)} nodes")
        if extractions:
            print(f"   Sample: {json.dumps(extractions[0]['data'], indent=2)[:200]}...")
    
    researcher.save_research(result, "research_ai_healthcare_multi.json")
    
    return result


def example_pipeline_research():
    """Example: Pipeline multiple research stages"""
    # Load token from config
    from pathlib import Path
    config_file = Path.home() / ".lumen" / "config.json"
    if not config_file.exists():
        print("❌ Not logged in. Run: python lumen_cli.py login")
        return None
    
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    client = LumenClient(config['token'])
    researcher = RecursiveResearcher(client, max_depth=2, delay=0.5)
    
    print("=" * 70)
    print("RESEARCH PIPELINE - Chained Agent Workflow")
    print("=" * 70)
    
    # Stage 1: Broad overview
    print("\n🔬 STAGE 1: Overview Research")
    overview = researcher.research("What is machine learning?")
    
    # Stage 2: Extract key topics from overview
    print("\n🔬 STAGE 2: Topic Extraction")
    topics_schema = {
        "type": "object",
        "properties": {
            "topics": {
                "type": "array",
                "items": {"type": "string"},
                "maxItems": 3
            }
        },
        "required": ["topics"],
        "additionalProperties": False
    }
    
    topics = researcher._extract_with_schema(
        overview.get('response', ''),
        topics_schema,
        0
    )
    
    # Stage 3: Deep dive into each topic
    print("\n🔬 STAGE 3: Deep Dive into Each Topic")
    deep_dives = []
    if topics and 'topics' in topics:
        for topic in topics['topics'][:2]:  # Limit to 2 topics
            print(f"\n  🎯 Deep diving: {topic}")
            researcher.explored_contexts.clear()  # Reset for new branch
            dive = researcher.research(f"Explain {topic} in detail", depth=0)
            deep_dives.append(dive)
    
    pipeline_result = {
        "overview": overview,
        "extracted_topics": topics,
        "deep_dives": deep_dives
    }
    
    researcher.save_research(pipeline_result, "research_pipeline_ml.json")
    
    print("\n✅ Pipeline complete!")
    return pipeline_result


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        
        if mode == "deep":
            example_deep_research()
        elif mode == "multi":
            example_multi_schema_research()
        elif mode == "pipeline":
            example_pipeline_research()
        else:
            print("Usage: python recursive_researcher.py [deep|multi|pipeline]")
    else:
        # Default: run deep research
        example_deep_research()
