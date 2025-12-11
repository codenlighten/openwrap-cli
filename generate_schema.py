#!/usr/bin/env python3
"""
Interactive Schema Generator CLI
Generate JSON schemas from natural language descriptions
"""
import sys
import json
from pathlib import Path
from lumen_sdk import LumenClient


def load_token():
    config_file = Path.home() / ".lumen" / "config.json"
    if not config_file.exists():
        print("❌ Not logged in. Run: python lumen_cli.py login")
        sys.exit(1)
    with open(config_file) as f:
        return json.load(f)['token']


META_SCHEMA = {
    "type": "object",
    "properties": {
        "schema": {
            "type": "object",
            "properties": {
                "type": {"type": "string"},
                "properties": {"type": "object"},
                "required": {"type": "array", "items": {"type": "string"}},
                "additionalProperties": {"type": "boolean"}
            },
            "required": ["type", "properties", "required", "additionalProperties"]
        },
        "example": {"type": "object"}
    },
    "required": ["schema"],
    "additionalProperties": False
}


def generate_schema(description: str) -> dict:
    """Generate a JSON schema from description"""
    client = LumenClient(load_token())
    
    example = {
        "schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "number", "minimum": 0}
            },
            "required": ["name"],
            "additionalProperties": False
        }
    }
    
    prompt = f"""Generate a JSON schema for: {description}

Return JSON in this exact format:
{json.dumps(example, indent=2)}

Guidelines:
- Use types: string, number, integer, boolean, array, object
- Add constraints: minimum, maximum, minLength, maxLength, enum, minItems, maxItems
- List required fields in "required" array
- Always set "additionalProperties": false
- Nest objects for complex structures

Return ONLY valid JSON."""
    
    try:
        result = client.query(prompt, model="gpt-5-nano", temperature=1.0)
        response_text = result['data']['response']
        
        if '```json' in response_text:
            response_text = response_text.split('```json')[1].split('```')[0]
        elif '```' in response_text:
            response_text = response_text.split('```')[1].split('```')[0]
        
        return json.loads(response_text.strip())
    except Exception as e:
        print(f"Error: {e}")
        return None


def main():
    print("🔧 Schema Generator - Interactive Mode")
    print("=" * 60)
    print("Describe what you need a schema for, and I'll generate it.")
    print("Type 'quit' to exit.\n")
    
    while True:
        print("-" * 60)
        description = input("📝 Describe your schema: ").strip()
        
        if description.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
        
        if not description:
            continue
        
        print("\n⏳ Generating schema...")
        generated = generate_schema(description)
        
        if generated and 'schema' in generated:
            print("\n✅ Generated Schema:")
            print(json.dumps(generated['schema'], indent=2))
            
            if 'example' in generated:
                print("\n📋 Example:")
                print(json.dumps(generated['example'], indent=2))
            
            # Ask if user wants to save
            save = input("\n💾 Save to file? (y/n): ").strip().lower()
            if save == 'y':
                filename = input("Filename (e.g., my_schema.json): ").strip()
                if not filename.endswith('.json'):
                    filename += '.json'
                
                with open(filename, 'w') as f:
                    json.dump(generated['schema'], f, indent=2)
                print(f"✅ Saved to {filename}")
            
            # Ask if user wants to test it
            test = input("\n🧪 Test with sample data? (y/n): ").strip().lower()
            if test == 'y':
                print("Describe sample data to validate against this schema:")
                sample_desc = input("Sample: ").strip()
                if sample_desc:
                    print(f"\n✅ Schema is ready to use!")
                    print(f"Use: python lumen_cli.py query '{sample_desc}' --schema '{filename}'")
        else:
            print("❌ Failed to generate schema")
        
        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted")
        sys.exit(0)
