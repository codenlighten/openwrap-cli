# Schema Generator - Meta-Schema Approach

## Concept

Use AI to generate JSON schemas from natural language descriptions by employing a **meta-schema** - a schema that defines how other schemas should be structured.

## The Meta-Schema

```json
{
  "type": "object",
  "properties": {
    "schema": {
      "type": "object",
      "properties": {
        "type": {"type": "string"},
        "properties": {"type": "object"},
        "required": {
          "type": "array",
          "items": {"type": "string"}
        },
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
  "additionalProperties": false
}
```

## How It Works

1. **Define the meta-schema** that describes what a valid schema looks like
2. **Provide an example** of a properly formatted schema
3. **Describe what you need** in natural language
4. **AI generates** a schema matching your description
5. **Validate** the generated schema against the meta-schema
6. **Use immediately** or save for later

## Usage

### Interactive Mode

```bash
python generate_schema.py
```

Then describe what you need:
```
Describe your schema: A user profile with name, email (required), age (optional, 0-120), and tags array
```

### Programmatic Usage

```python
from schema_generator import generate_schema

description = """
A product with id, name, price (object with amount and currency),
category enum, and stock count. Id, name, and price are required.
"""

result = generate_schema(description)
schema = result['schema']

# Use the generated schema
from lumen_sdk import LumenClient
client = LumenClient(token)
result = client.query("Extract product info", output_schema=schema)
```

## Example Generated Schemas

### User Profile Schema

**Description:**
```
A user profile with username (3-20 chars), email, age (13-120),
and settings object with notifications boolean and theme enum (light/dark).
Username and email are required.
```

**Generated Schema:**
```json
{
  "type": "object",
  "properties": {
    "username": {
      "type": "string",
      "minLength": 3,
      "maxLength": 20
    },
    "email": {"type": "string"},
    "age": {
      "type": "integer",
      "minimum": 13,
      "maximum": 120
    },
    "settings": {
      "type": "object",
      "properties": {
        "notifications": {"type": "boolean"},
        "theme": {
          "type": "string",
          "enum": ["light", "dark"]
        }
      },
      "additionalProperties": false
    }
  },
  "required": ["username", "email"],
  "additionalProperties": false
}
```

### E-commerce Order Schema

**Description:**
```
An order with order_id, customer object (name, email), items array
(each with product_id, quantity, price), total_amount, status enum
(pending/processing/shipped/delivered), and created_at timestamp.
Order_id, customer, items, and status are required.
```

**Generated Schema:**
```json
{
  "type": "object",
  "properties": {
    "order_id": {"type": "string"},
    "customer": {
      "type": "object",
      "properties": {
        "name": {"type": "string"},
        "email": {"type": "string"}
      },
      "required": ["name", "email"],
      "additionalProperties": false
    },
    "items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "product_id": {"type": "string"},
          "quantity": {"type": "integer", "minimum": 1},
          "price": {"type": "number", "minimum": 0}
        },
        "required": ["product_id", "quantity", "price"],
        "additionalProperties": false
      },
      "minItems": 1
    },
    "total_amount": {"type": "number", "minimum": 0},
    "status": {
      "type": "string",
      "enum": ["pending", "processing", "shipped", "delivered"]
    },
    "created_at": {"type": "string"}
  },
  "required": ["order_id", "customer", "items", "status"],
  "additionalProperties": false
}
```

## Benefits

### 1. **Rapid Schema Development**
- Describe what you need in plain English
- Get a production-ready schema instantly
- No need to memorize JSON Schema syntax

### 2. **Consistency**
- Meta-schema enforces uniform structure
- All generated schemas follow best practices
- `additionalProperties: false` by default

### 3. **Reusability**
- Save generated schemas as JSON files
- Build a library of validated schemas
- Share schemas across projects

### 4. **Type Safety**
- Schemas ensure predictable API responses
- Validation catches errors early
- Enforces data contracts

## Workflow

```
┌──────────────────────┐
│ Describe Data Need   │
│ (Natural Language)   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  AI + Meta-Schema    │
│  Generate Schema     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Validate Schema     │
│  Against Meta-Schema │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Save or Use         │
│  Immediately         │
└──────────────────────┘
```

## Use Cases

- **API Development**: Generate response schemas
- **Data Extraction**: Create schemas for parsing unstructured text
- **Form Validation**: Define input validation rules
- **Database Models**: Schema for document stores
- **Configuration Files**: Validate config structure
- **Event Logging**: Structured event schemas
- **Analytics**: Data pipeline schemas
- **IoT**: Device data schemas

## Advanced Features

### Nested Objects

Description can include complex nesting:
```
"A company with name, address object (street, city, country),
employees array (each with id, name, role object with title and department)"
```

### Validation Constraints

Include constraints in description:
```
"Price between 0 and 10000, email matching pattern, tags with 1-5 items"
```

### Enums

Specify fixed options:
```
"Status must be one of: draft, published, archived"
```

## Implementation Tips

### 1. Be Specific
```
❌ "A user object"
✅ "A user with username (string), age (number 0-150), and active status (boolean)"
```

### 2. Mention Required Fields
```
❌ "Fields: name, email, phone"
✅ "Required: name and email. Optional: phone"
```

### 3. Include Constraints
```
❌ "An array of tags"
✅ "Tags array with 1-10 unique strings"
```

### 4. Specify Types Clearly
```
❌ "A date field"
✅ "A timestamp string in ISO 8601 format"
```

## Integration with LumenAI

Once you have a generated schema:

```python
# Generate schema
schema_result = generate_schema("Your description here")
schema = schema_result['schema']

# Use with LumenAI
client = LumenClient(token)
result = client.query(
    "Extract data from this text: ...",
    output_schema=schema
)

# Response will match the schema structure
data = result['data']['response']
```

## Files

- `schema_generator.py` - Demo script with examples
- `generate_schema.py` - Interactive CLI tool
- `SCHEMA_GENERATOR.md` - This documentation

## Next Steps

1. Try the interactive generator: `python generate_schema.py`
2. Build a schema library for your project
3. Use generated schemas with LumenAI API
4. Share schemas with your team
