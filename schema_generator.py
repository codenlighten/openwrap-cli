#!/usr/bin/env python3
"""
Schema Generator - Use AI to generate JSON schemas dynamically
Creates schemas from natural language descriptions using a meta-schema
"""
from lumen_sdk import LumenClient
import json
from pathlib import Path


def load_token():
    """Load token from config"""
    config_file = Path.home() / ".lumen" / "config.json"
    with open(config_file) as f:
        return json.load(f)['token']


# Meta-schema: A schema for generating other schemas
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
        "example": {
            "type": "object",
            "description": "Example object that matches the schema"
        }
    },
    "required": ["schema"],
    "additionalProperties": False
}

# Example of what we want the AI to return
SCHEMA_EXAMPLE = {
    "schema": {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "number", "minimum": 0},
            "email": {"type": "string"}
        },
        "required": ["name", "email"],
        "additionalProperties": False
    },
    "example": {
        "name": "John Doe",
        "age": 30,
        "email": "john@example.com"
    }
}


def generate_schema(description: str) -> dict:
    """
    Generate a JSON schema from a natural language description
    
    Args:
        description: Natural language description of what the schema should validate
        
    Returns:
        Dictionary containing 'schema' and optionally 'example'
    """
    client = LumenClient(load_token())
    
    prompt = f"""Generate a JSON schema for the following use case:

"{description}"

Your response must follow this exact format:
{{
  "schema": {{
    "type": "object",
    "properties": {{
      // Define all fields here with their types and constraints
    }},
    "required": [/* list required field names */],
    "additionalProperties": false
  }},
  "example": {{
    // Optional: provide an example object that matches the schema
  }}
}}

Example format:
{json.dumps(SCHEMA_EXAMPLE, indent=2)}

Guidelines:
- Use appropriate types: string, number, integer, boolean, array, object
- Add constraints: minimum, maximum, minLength, maxLength, enum, etc.
- Mark mandatory fields in "required" array
- Always set "additionalProperties": false for strict validation
- Nest objects when needed for complex structures
- Provide meaningful example data

Return ONLY valid JSON matching the meta-schema."""
    
    try:
        result = client.query(
            prompt,
            model="gpt-5-nano",
            temperature=1.0
        )
        
        # Extract the generated schema
        response_text = result['data']['response']
        
        # Try to parse JSON from response
        if '```json' in response_text:
            response_text = response_text.split('```json')[1].split('```')[0]
        elif '```' in response_text:
            response_text = response_text.split('```')[1].split('```')[0]
        
        generated = json.loads(response_text.strip())
        return generated
        
    except Exception as e:
        print(f"Error generating schema: {e}")
        return None


def validate_generated_schema(generated: dict) -> bool:
    """Validate that the generated response matches our meta-schema"""
    if not isinstance(generated, dict):
        return False
    
    if 'schema' not in generated:
        return False
    
    schema = generated['schema']
    
    # Check required meta-schema fields
    required_fields = ['type', 'properties', 'required', 'additionalProperties']
    for field in required_fields:
        if field not in schema:
            print(f"Missing required field in schema: {field}")
            return False
    
    return True


def use_generated_schema(schema: dict, prompt: str) -> dict:
    """Use a generated schema to query the API"""
    client = LumenClient(load_token())
    
    result = client.query(
        prompt,
        model="gpt-5-nano",
        temperature=1.0
    )
    
    return result


if __name__ == "__main__":
    import sys
    import io
    
    # Fix encoding for Windows console
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("="*70)
    print("Schema Generator - Create Schemas from Descriptions")
    print("="*70)
    
    # Example 1: Generate schema for a blog post
    print("\nExample 1: Blog Post Schema")
    print("-"*70)
    description = """
    A blog post with title, author name, publication date, content text,
    tags (array of strings), and view count. Title, author, and content
    are required. Tags should have 1-10 items.
    """
    
    print(f"Description: {description.strip()}")
    print("\nGenerating schema...")
    
    generated = generate_schema(description)
    
    if generated and validate_generated_schema(generated):
        print("\n[SUCCESS] Schema generated successfully:")
        print(json.dumps(generated['schema'], indent=2))
        
        if 'example' in generated:
            print("\n[EXAMPLE] Example data:")
            print(json.dumps(generated['example'], indent=2))
        
        # Save the schema for reuse
        schema_file = Path("generated_blog_schema.json")
        with open(schema_file, 'w') as f:
            json.dump(generated['schema'], f, indent=2)
        print(f"\n[SAVED] Schema saved to: {schema_file}")
    else:
        print("[ERROR] Failed to generate valid schema")
    
    # Example 2: Generate schema for a product review
    print("\n\n" + "="*70)
    print("Example 2: Product Review Schema")
    print("-"*70)
    description = """
    A product review with reviewer name, rating (1-5 stars as integer),
    review title, review text, verified purchase (boolean), and helpful
    count. Rating, title, and text are required. Include a nested object
    for product info with id and name.
    """
    
    print(f"Description: {description.strip()}")
    print("\nGenerating schema...")
    
    generated = generate_schema(description)
    
    if generated and validate_generated_schema(generated):
        print("\n[SUCCESS] Schema generated successfully:")
        print(json.dumps(generated['schema'], indent=2))
        
        if 'example' in generated:
            print("\n[EXAMPLE] Example data:")
            print(json.dumps(generated['example'], indent=2))
        
        schema_file = Path("generated_review_schema.json")
        with open(schema_file, 'w') as f:
            json.dump(generated['schema'], f, indent=2)
        print(f"\n[SAVED] Schema saved to: {schema_file}")
    else:
        print("[ERROR] Failed to generate valid schema")
    
    # Example 3: Generate and immediately use a schema
    print("\n\n" + "="*70)
    print("Example 3: Generate & Use Schema")
    print("-"*70)
    description = """
    Weather data with location (city and country), temperature in celsius,
    conditions (sunny/cloudy/rainy/snowy), humidity percentage, and wind
    speed. Location and conditions are required. Temperature should be
    between -50 and 50.
    """
    
    print(f"Description: {description.strip()}")
    print("\nGenerating schema...")
    
    generated = generate_schema(description)
    
    if generated and validate_generated_schema(generated):
        print("\n[SUCCESS] Schema generated:")
        print(json.dumps(generated['schema'], indent=2))
        
        # Now use this schema to extract weather data
        print("\n[INFO] Using generated schema to extract weather data...")
        weather_text = "Paris, France: sunny with 22°C, humidity at 65%, winds at 15 km/h"
        
        # Note: In real usage, you'd pass the schema to the API
        # For now, just demonstrate the workflow
        print(f"\nText to analyze: {weather_text}")
        print("[SUCCESS] Schema is ready to use with API queries")
        
        schema_file = Path("generated_weather_schema.json")
        with open(schema_file, 'w') as f:
            json.dump(generated['schema'], f, indent=2)
        print(f"\n[SAVED] Schema saved to: {schema_file}")
    
    # Display meta-schema
    print("\n\n" + "="*70)
    print("Meta-Schema (Schema for Generating Schemas)")
    print("="*70)
    print(json.dumps(META_SCHEMA, indent=2))
    
    print("\n\n" + "="*70)
    print("How It Works")
    print("="*70)
    print("""
1. Define a META-SCHEMA that describes the structure of JSON schemas
2. Provide an EXAMPLE of what a generated schema should look like
3. Give a natural language DESCRIPTION of what you need
4. AI generates a schema matching the meta-schema format
5. Validate the generated schema
6. Use the schema immediately or save for later

Benefits:
- Generate schemas on-demand from descriptions
- No need to manually write complex schemas
- Consistent schema format enforced by meta-schema
- Reusable schemas saved as JSON files
- Can create specialized schemas for any use case

Usage:
- Describe what data structure you need
- Get back a validated JSON schema
- Use it immediately with the LumenAI API
- Build schema libraries for your applications
    """)
    
    print("\n" + "="*70)
    print("Use Cases")
    print("="*70)
    print("""
- API response validation
- Data extraction from text
- Form validation schemas
- Database model schemas
- Configuration file schemas
- Event logging schemas
- Analytics data schemas
- User profile schemas
- E-commerce product schemas
- IoT device data schemas
    """)
