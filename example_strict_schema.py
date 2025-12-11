#!/usr/bin/env python3
"""
Example: Advanced JSON Schema with strict validation
Demonstrates using custom schema objects with properties, required fields, and additionalProperties
"""
from lumen_sdk import LumenClient
import json
from pathlib import Path


def load_token():
    """Load token from config"""
    config_file = Path.home() / ".lumen" / "config.json"
    with open(config_file) as f:
        return json.load(f)['token']


def analyze_with_strict_schema(text: str) -> dict:
    """
    Analyze text with strict JSON schema validation
    
    This example shows how to use:
    - properties: Define expected fields
    - required: Enforce specific fields must be present
    - additionalProperties: false - Reject any unexpected fields
    """
    client = LumenClient(load_token())
    
    # Strict schema - only allows defined properties, no extras
    schema = {
        "type": "object",
        "properties": {
            "sentiment": {
                "type": "string",
                "enum": ["positive", "negative", "neutral"]
            },
            "confidence": {
                "type": "number",
                "minimum": 0,
                "maximum": 1
            },
            "key_topics": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 1,
                "maxItems": 5
            },
            "summary": {
                "type": "string",
                "maxLength": 200
            }
        },
        "required": ["sentiment", "confidence", "key_topics"],  # summary is optional
        "additionalProperties": False  # Reject any fields not in properties
    }
    
    prompt = f"""Analyze this text and return ONLY valid JSON matching the schema.

Text: "{text}"

Return JSON with:
- sentiment: "positive", "negative", or "neutral"
- confidence: decimal between 0 and 1
- key_topics: array of 1-5 topic strings
- summary: optional brief summary (max 200 chars)

IMPORTANT: Return ONLY these fields, no additional properties."""
    
    try:
        result = client.query(
            prompt,
            model="gpt-5-nano",
            temperature=1.0
        )
        return result
    except Exception as e:
        print(f"Error: {e}")
        return None


def extract_product_info(description: str) -> dict:
    """Extract structured product information with strict validation"""
    client = LumenClient(load_token())
    
    schema = {
        "type": "object",
        "properties": {
            "product_name": {"type": "string"},
            "category": {
                "type": "string",
                "enum": ["electronics", "clothing", "food", "books", "other"]
            },
            "price": {
                "type": "object",
                "properties": {
                    "amount": {"type": "number", "minimum": 0},
                    "currency": {"type": "string", "enum": ["USD", "EUR", "GBP"]}
                },
                "required": ["amount", "currency"],
                "additionalProperties": False
            },
            "features": {
                "type": "array",
                "items": {"type": "string"}
            },
            "in_stock": {"type": "boolean"}
        },
        "required": ["product_name", "category", "price"],
        "additionalProperties": False
    }
    
    prompt = f"""Extract product information from this description as JSON:

"{description}"

Return exactly these fields:
- product_name: string
- category: one of [electronics, clothing, food, books, other]
- price: object with amount (number) and currency (USD/EUR/GBP)
- features: array of feature strings
- in_stock: boolean

No additional fields allowed."""
    
    try:
        result = client.query(
            prompt,
            model="gpt-5-nano",
            temperature=1.0
        )
        return result
    except Exception as e:
        print(f"Error: {e}")
        return None


def validate_response_schema(response_data, schema):
    """
    Validate that response matches schema
    This is a simple validator - in production use jsonschema library
    """
    if not isinstance(response_data, dict):
        return False, "Response is not an object"
    
    # Check required fields
    if "required" in schema:
        for field in schema["required"]:
            if field not in response_data:
                return False, f"Missing required field: {field}"
    
    # Check for additional properties
    if schema.get("additionalProperties") == False:
        allowed_props = set(schema.get("properties", {}).keys())
        actual_props = set(response_data.keys())
        extra_props = actual_props - allowed_props
        if extra_props:
            return False, f"Unexpected fields: {extra_props}"
    
    return True, "Valid"


if __name__ == "__main__":
    print("=" * 70)
    print("Advanced JSON Schema Example - Strict Validation")
    print("=" * 70)
    
    # Example 1: Sentiment Analysis with strict schema
    print("\n📊 Example 1: Sentiment Analysis (Strict Schema)")
    print("-" * 70)
    
    text = """
    I absolutely loved this product! The quality exceeded my expectations 
    and the customer service was fantastic. Highly recommended!
    """
    
    print(f"Text: {text.strip()}")
    print("\nSchema Requirements:")
    print("  - Required: sentiment, confidence, key_topics")
    print("  - Optional: summary")
    print("  - additionalProperties: false (no extra fields allowed)")
    print("\nAnalyzing...\n")
    
    result = analyze_with_strict_schema(text)
    if result:
        print("Response:")
        print(json.dumps(result['data'], indent=2))
        
        # Try to parse and validate
        try:
            response_text = result['data']['response']
            # Extract JSON from response (might be wrapped in markdown)
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0]
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0]
            
            parsed = json.loads(response_text.strip())
            print("\n✅ Successfully parsed JSON:")
            print(json.dumps(parsed, indent=2))
            
            # Manual validation
            has_required = all(k in parsed for k in ["sentiment", "confidence", "key_topics"])
            print(f"\n✅ Has required fields: {has_required}")
            
            # Check for extra fields
            allowed = {"sentiment", "confidence", "key_topics", "summary"}
            extra = set(parsed.keys()) - allowed
            if extra:
                print(f"⚠️  Warning: Extra fields found: {extra}")
            else:
                print("✅ No additional properties (schema enforced)")
                
        except json.JSONDecodeError as e:
            print(f"⚠️  Could not parse response as JSON: {e}")
    
    # Example 2: Product Extraction with nested schema
    print("\n\n" + "=" * 70)
    print("📦 Example 2: Product Information (Nested Schema)")
    print("-" * 70)
    
    product_desc = """
    Apple MacBook Pro 16-inch with M3 chip. Price: $2,499 USD.
    Features include: 16GB RAM, 512GB SSD, Retina Display, Touch Bar.
    Currently in stock and available for immediate shipping.
    """
    
    print(f"Description: {product_desc.strip()}")
    print("\nSchema Requirements:")
    print("  - Required: product_name, category, price (nested object)")
    print("  - price.required: amount, currency")
    print("  - additionalProperties: false at all levels")
    print("\nExtracting...\n")
    
    result = extract_product_info(product_desc)
    if result:
        print("Response:")
        response_text = result['data']['response']
        
        # Try to extract and validate JSON
        try:
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0]
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0]
            
            parsed = json.loads(response_text.strip())
            print("✅ Parsed Product Data:")
            print(json.dumps(parsed, indent=2))
            
            # Validate structure
            has_required = all(k in parsed for k in ["product_name", "category", "price"])
            print(f"\n✅ Has required top-level fields: {has_required}")
            
            if "price" in parsed and isinstance(parsed["price"], dict):
                has_price_fields = all(k in parsed["price"] for k in ["amount", "currency"])
                print(f"✅ Has required price fields: {has_price_fields}")
                
        except json.JSONDecodeError as e:
            print(f"⚠️  Could not parse response as JSON: {e}")
            print(f"Raw response: {response_text}")
    
    print("\n" + "=" * 70)
    print("💡 Key Takeaways:")
    print("=" * 70)
    print("""
1. Use 'properties' to define allowed fields and their types
2. Use 'required' array to enforce mandatory fields
3. Set 'additionalProperties: false' to reject unexpected fields
4. Nest schemas for complex objects (like price with amount/currency)
5. Use enums to restrict values to specific options
6. Add validation constraints (min/max, minItems/maxItems, etc.)

This ensures type-safe, predictable API responses!
    """)
