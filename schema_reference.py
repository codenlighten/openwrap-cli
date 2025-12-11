#!/usr/bin/env python3
"""
Advanced Schema Examples - Complete Reference
Demonstrates all schema validation features available in LumenAI
"""
from lumen_sdk import LumenClient
import json
from pathlib import Path


def load_token():
    config_file = Path.home() / ".lumen" / "config.json"
    with open(config_file) as f:
        return json.load(f)['token']


# Example 1: Enum constraints
SCHEMA_ENUM_EXAMPLE = {
    "type": "object",
    "properties": {
        "status": {
            "type": "string",
            "enum": ["pending", "approved", "rejected"]
        },
        "priority": {
            "type": "string",
            "enum": ["low", "medium", "high", "critical"]
        }
    },
    "required": ["status", "priority"],
    "additionalProperties": False
}

# Example 2: Nested objects with validation
SCHEMA_NESTED_EXAMPLE = {
    "type": "object",
    "properties": {
        "user": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "minLength": 1},
                "age": {"type": "number", "minimum": 0, "maximum": 150},
                "email": {"type": "string"}
            },
            "required": ["name", "email"],
            "additionalProperties": False
        },
        "settings": {
            "type": "object",
            "properties": {
                "notifications": {"type": "boolean"},
                "theme": {"type": "string", "enum": ["light", "dark"]}
            },
            "additionalProperties": False
        }
    },
    "required": ["user"],
    "additionalProperties": False
}

# Example 3: Arrays with constraints
SCHEMA_ARRAY_EXAMPLE = {
    "type": "object",
    "properties": {
        "tags": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1,
            "maxItems": 10,
            "uniqueItems": True
        },
        "scores": {
            "type": "array",
            "items": {
                "type": "number",
                "minimum": 0,
                "maximum": 100
            }
        }
    },
    "required": ["tags"],
    "additionalProperties": False
}

# Example 4: Complex validation with patterns
SCHEMA_PATTERN_EXAMPLE = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
            "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
        },
        "phone": {
            "type": "string",
            "pattern": "^\\+?[1-9]\\d{1,14}$"
        },
        "website": {
            "type": "string",
            "format": "uri"
        }
    },
    "required": ["email"],
    "additionalProperties": False
}

# Example 5: Complete product schema
SCHEMA_PRODUCT_COMPLETE = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string", "minLength": 1, "maxLength": 200},
        "description": {"type": "string"},
        "price": {
            "type": "object",
            "properties": {
                "amount": {"type": "number", "minimum": 0},
                "currency": {"type": "string", "enum": ["USD", "EUR", "GBP", "JPY"]}
            },
            "required": ["amount", "currency"],
            "additionalProperties": False
        },
        "category": {
            "type": "string",
            "enum": ["electronics", "clothing", "food", "books", "toys", "other"]
        },
        "tags": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1,
            "maxItems": 5,
            "uniqueItems": True
        },
        "stock": {
            "type": "object",
            "properties": {
                "quantity": {"type": "integer", "minimum": 0},
                "available": {"type": "boolean"}
            },
            "required": ["quantity", "available"],
            "additionalProperties": False
        },
        "rating": {
            "type": "object",
            "properties": {
                "average": {"type": "number", "minimum": 0, "maximum": 5},
                "count": {"type": "integer", "minimum": 0}
            },
            "additionalProperties": False
        }
    },
    "required": ["id", "name", "price", "category", "stock"],
    "additionalProperties": False
}


def print_schema(name: str, schema: dict):
    """Pretty print schema"""
    print(f"\n{'='*70}")
    print(f"Schema: {name}")
    print('='*70)
    print(json.dumps(schema, indent=2))


if __name__ == "__main__":
    print("="*70)
    print("JSON Schema Reference - All Validation Features")
    print("="*70)
    
    print("""
This file demonstrates all available JSON schema validation features:

1. TYPE VALIDATION
   - "type": "string", "number", "integer", "boolean", "array", "object"

2. STRING CONSTRAINTS
   - "minLength": minimum string length
   - "maxLength": maximum string length
   - "pattern": regex pattern (e.g., email validation)
   - "format": predefined formats (uri, email, date, etc.)
   - "enum": restrict to specific values

3. NUMBER CONSTRAINTS
   - "minimum": minimum value (inclusive)
   - "maximum": maximum value (inclusive)
   - "exclusiveMinimum": minimum value (exclusive)
   - "exclusiveMaximum": maximum value (exclusive)

4. ARRAY CONSTRAINTS
   - "items": schema for array items
   - "minItems": minimum array length
   - "maxItems": maximum array length
   - "uniqueItems": true - all items must be unique

5. OBJECT CONSTRAINTS
   - "properties": define allowed fields and their schemas
   - "required": array of mandatory field names
   - "additionalProperties": false - reject extra fields
   - Nested objects: use object schemas within properties

6. ENUM VALUES
   - Restrict to specific allowed values
   - Works with strings, numbers, etc.
    """)
    
    # Display all example schemas
    print_schema("Enum Example", SCHEMA_ENUM_EXAMPLE)
    print("Use case: Status fields, priorities, fixed options")
    
    print_schema("Nested Objects", SCHEMA_NESTED_EXAMPLE)
    print("Use case: Complex data structures, user profiles")
    
    print_schema("Array Validation", SCHEMA_ARRAY_EXAMPLE)
    print("Use case: Tags, lists with constraints")
    
    print_schema("Pattern Matching", SCHEMA_PATTERN_EXAMPLE)
    print("Use case: Email, phone, URL validation")
    
    print_schema("Complete Product Schema", SCHEMA_PRODUCT_COMPLETE)
    print("Use case: E-commerce, detailed product data")
    
    print("\n" + "="*70)
    print("CLI Usage Examples")
    print("="*70)
    
    print("""
# Simple enum constraint
python lumen_cli.py query "What's the status?" \\
  --schema '{"type":"object","properties":{"status":{"type":"string","enum":["pending","approved","rejected"]}},"required":["status"],"additionalProperties":false}'

# Nested object with validation
python lumen_cli.py query "Get user info" \\
  --schema '{"type":"object","properties":{"user":{"type":"object","properties":{"name":{"type":"string"},"age":{"type":"number","minimum":0}},"required":["name"],"additionalProperties":false}},"required":["user"],"additionalProperties":false}'

# Array with constraints
python lumen_cli.py query "List tags" \\
  --schema '{"type":"object","properties":{"tags":{"type":"array","items":{"type":"string"},"minItems":1,"maxItems":5}},"required":["tags"],"additionalProperties":false}'
    """)
    
    print("\n" + "="*70)
    print("SDK Usage Examples")
    print("="*70)
    
    print("""
from lumen_sdk import LumenClient

client = LumenClient(token)

# Use any schema from above
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "score": {"type": "number", "minimum": 0, "maximum": 100}
    },
    "required": ["name", "score"],
    "additionalProperties": False
}

result = client.query(
    "Extract name and score",
    model="gpt-5-nano",
    output_schema=schema
)
    """)
    
    print("\n" + "="*70)
    print("💡 Best Practices")
    print("="*70)
    print("""
1. Always use "additionalProperties": false for strict validation
2. Include "required" array to enforce mandatory fields
3. Use enums for fields with fixed options
4. Add min/max constraints for numbers and arrays
5. Validate strings with patterns or formats
6. Nest schemas for complex object structures
7. Be specific with types (integer vs number)
8. Document expected values in your prompts

This ensures type-safe, predictable API responses!
    """)
