# JSON Schema Quick Reference

## Basic Structure

```json
{
  "type": "object",
  "properties": { /* field definitions */ },
  "required": [ /* mandatory fields */ ],
  "additionalProperties": false
}
```

## Type Validation

| Type | Description | Example |
|------|-------------|---------|
| `string` | Text | `{"type": "string"}` |
| `number` | Any number | `{"type": "number"}` |
| `integer` | Whole number | `{"type": "integer"}` |
| `boolean` | true/false | `{"type": "boolean"}` |
| `array` | List | `{"type": "array", "items": {...}}` |
| `object` | Nested object | `{"type": "object", "properties": {...}}` |

## String Constraints

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 100,
  "pattern": "^[A-Z][a-z]+$",
  "enum": ["option1", "option2", "option3"]
}
```

## Number Constraints

```json
{
  "type": "number",
  "minimum": 0,
  "maximum": 100,
  "exclusiveMinimum": 0,
  "exclusiveMaximum": 100
}
```

## Array Constraints

```json
{
  "type": "array",
  "items": {"type": "string"},
  "minItems": 1,
  "maxItems": 10,
  "uniqueItems": true
}
```

## Object with Required Fields

```json
{
  "type": "object",
  "properties": {
    "id": {"type": "string"},
    "name": {"type": "string"},
    "age": {"type": "integer", "minimum": 0}
  },
  "required": ["id", "name"],
  "additionalProperties": false
}
```

## Nested Objects

```json
{
  "type": "object",
  "properties": {
    "user": {
      "type": "object",
      "properties": {
        "name": {"type": "string"},
        "email": {"type": "string"}
      },
      "required": ["name", "email"],
      "additionalProperties": false
    },
    "metadata": {
      "type": "object",
      "properties": {
        "created": {"type": "string"},
        "updated": {"type": "string"}
      },
      "additionalProperties": false
    }
  },
  "required": ["user"],
  "additionalProperties": false
}
```

## Enum Values

```json
{
  "type": "object",
  "properties": {
    "status": {
      "type": "string",
      "enum": ["pending", "approved", "rejected"]
    },
    "priority": {
      "type": "string",
      "enum": ["low", "medium", "high"]
    }
  },
  "required": ["status", "priority"],
  "additionalProperties": false
}
```

## Real-World Examples

### Product Schema
```json
{
  "type": "object",
  "properties": {
    "id": {"type": "string"},
    "name": {"type": "string", "minLength": 1},
    "price": {
      "type": "object",
      "properties": {
        "amount": {"type": "number", "minimum": 0},
        "currency": {"type": "string", "enum": ["USD", "EUR", "GBP"]}
      },
      "required": ["amount", "currency"],
      "additionalProperties": false
    },
    "tags": {
      "type": "array",
      "items": {"type": "string"},
      "minItems": 1,
      "maxItems": 5
    },
    "in_stock": {"type": "boolean"}
  },
  "required": ["id", "name", "price"],
  "additionalProperties": false
}
```

### User Profile Schema
```json
{
  "type": "object",
  "properties": {
    "username": {"type": "string", "minLength": 3, "maxLength": 20},
    "email": {"type": "string"},
    "age": {"type": "integer", "minimum": 13, "maximum": 120},
    "settings": {
      "type": "object",
      "properties": {
        "notifications": {"type": "boolean"},
        "theme": {"type": "string", "enum": ["light", "dark"]}
      },
      "additionalProperties": false
    }
  },
  "required": ["username", "email"],
  "additionalProperties": false
}
```

### Analytics Schema
```json
{
  "type": "object",
  "properties": {
    "event": {"type": "string"},
    "timestamp": {"type": "string"},
    "metrics": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {"type": "string"},
          "value": {"type": "number"}
        },
        "required": ["name", "value"],
        "additionalProperties": false
      }
    },
    "metadata": {
      "type": "object",
      "additionalProperties": true
    }
  },
  "required": ["event", "timestamp"],
  "additionalProperties": false
}
```

## CLI Usage

### Basic Schema
```bash
python lumen_cli.py query "Extract data" \
  --schema '{"type":"object","properties":{"name":{"type":"string"}},"required":["name"],"additionalProperties":false}'
```

### With Enum
```bash
python lumen_cli.py query "What's the status?" \
  --schema '{"type":"object","properties":{"status":{"type":"string","enum":["active","inactive"]}},"required":["status"],"additionalProperties":false}'
```

### Nested Object
```bash
python lumen_cli.py query "Get user" \
  --schema '{"type":"object","properties":{"user":{"type":"object","properties":{"name":{"type":"string"}},"required":["name"]}},"required":["user"],"additionalProperties":false}'
```

## SDK Usage

```python
from lumen_sdk import LumenClient

client = LumenClient(token)

# Define schema
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
        }
    },
    "required": ["sentiment", "confidence"],
    "additionalProperties": False
}

# Use in query
result = client.query(
    "Analyze this text",
    model="gpt-5-nano",
    output_schema=schema
)
```

## Best Practices

1. ✅ **Always use `additionalProperties: false`** for strict validation
2. ✅ **Define `required` fields** to enforce mandatory data
3. ✅ **Use enums** for fields with fixed options
4. ✅ **Add constraints** (min/max) to validate ranges
5. ✅ **Nest schemas** for complex structures
6. ✅ **Be specific** with types (integer vs number)
7. ✅ **Document expected values** in your prompts
8. ✅ **Validate responses** against the schema

## Common Patterns

### ID + Timestamp Pattern
```json
{
  "id": {"type": "string"},
  "created_at": {"type": "string"},
  "updated_at": {"type": "string"}
}
```

### Pagination Pattern
```json
{
  "items": {"type": "array", "items": {...}},
  "page": {"type": "integer", "minimum": 1},
  "total": {"type": "integer", "minimum": 0}
}
```

### Error Response Pattern
```json
{
  "error": {"type": "boolean"},
  "message": {"type": "string"},
  "code": {"type": "integer"}
}
```

## Resources

- Full examples: `example_strict_schema.py`
- Complete reference: `schema_reference.py`
- SDK docs: `lumen_sdk.py`
- JSON Schema spec: https://json-schema.org/
