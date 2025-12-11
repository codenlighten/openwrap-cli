# LumenAI CLI & SDK

Command-line interface and Python SDK for the LumenAI API Gateway.

## Features

- ✅ JWT authentication with secure credential storage
- ✅ Query AI models (GPT-5 series, GPT-4o-mini)
- ✅ Real-time streaming responses
- ✅ Structured JSON output
- ✅ Cryptographic signatures (ECDSA, Post-Quantum)
- ✅ Usage tracking and cost monitoring
- ✅ Python SDK for programmatic access

## Installation

```bash
pip install -r requirements.txt
```

For CLI command shortcut (optional):
```bash
pip install -e .
# Then use: lumen login, lumen query, etc.
```

## Usage

### Authentication

#### Login
```bash
python lumen_cli.py login
```

Or with email:
```bash
python lumen_cli.py login --email your@email.com
```

#### Check Status
```bash
python lumen_cli.py status
```

#### Logout
```bash
python lumen_cli.py logout
```

#### Register New Account
```bash
python lumen_cli.py register
```

### Querying

#### Send a Query
```bash
python lumen_cli.py query "What is the capital of France?"
```

With options:
```bash
python lumen_cli.py query "Explain quantum computing" --model gpt-5-mini --temperature 0.7
```

#### Stream a Response
```bash
python lumen_cli.py stream "Write a short story about AI"
```

With model selection:
```bash
python lumen_cli.py stream "Explain machine learning" --model gpt-5-pro
```

#### Structured Output (JSON Schema)
```bash
# Basic schema
python lumen_cli.py query "List 3 countries" --schema '{"type":"object","properties":{"countries":{"type":"array"}}}'

# Strict schema with required fields and no additional properties
python lumen_cli.py query "Analyze sentiment" --schema '{"type":"object","properties":{"sentiment":{"type":"string"},"score":{"type":"number"}},"required":["sentiment","score"],"additionalProperties":false}'
```

#### Cryptographic Signatures
```bash
python lumen_cli.py query "Hello" --signature ecdsa
python lumen_cli.py query "Hello" --signature pqc
python lumen_cli.py query "Hello" --signature hybrid
```

#### Get Public Keys
```bash
python lumen_cli.py keys
```

### Available Models
- `gpt-5-nano` (Free tier)
- `gpt-5-mini`
- `gpt-5-1`
- `gpt-5-pro`
- `gpt-4o-mini`

## Python SDK Usage

```python
from lumen_sdk import LumenClient, LumenAuth

# Option 1: Login and get token
auth = LumenAuth()
token = auth.login("your@email.com", "password")

# Option 2: Use existing token from CLI
import json
from pathlib import Path
config = json.load(open(Path.home() / ".lumen" / "config.json"))
token = config['token']

# Create client
client = LumenClient(token)

# Simple query
result = client.query("What is Python?")
print(result['data']['response'])

# Stream response
for chunk in client.stream("Write a story"):
    print(chunk, end='', flush=True)

# Structured output with strict schema
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "number", "minimum": 0, "maximum": 150},
        "tags": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1,
            "maxItems": 5
        }
    },
    "required": ["name", "age"],
    "additionalProperties": False  # Reject any extra fields
}

result = client.query("Extract person info", output_schema=schema)

# Get public keys
keys = client.get_keys()
```

## JSON Schema Features

LumenAI supports full JSON schema validation with:

- **`properties`**: Define allowed fields and their types
- **`required`**: Array of mandatory field names  
- **`additionalProperties: false`**: Reject unexpected fields
- **`enum`**: Restrict to specific values
- **`minimum`/`maximum`**: Number constraints
- **`minLength`/`maxLength`**: String length constraints
- **`minItems`/`maxItems`**: Array size constraints
- **`pattern`**: Regex validation
- **Nested objects**: Complex hierarchical schemas

See `schema_reference.py` for complete examples.

## Examples

### Code Review
```bash
python example_code_review.py
```
Analyzes Python code and provides structured feedback.

### Interactive Chatbot
```bash
python example_chatbot.py
```
Real-time chat interface with conversation context.

### Entity Extraction
```bash
python example_data_extraction.py
```
Extract people, organizations, locations, and dates from text.

### Strict Schema Validation
```bash
python example_strict_schema.py
```
Advanced JSON schemas with `properties`, `required` array, and `additionalProperties: false` for type-safe responses.

### Schema Generator
```bash
python generate_schema.py
```
Interactive tool to generate JSON schemas from natural language descriptions. Uses a meta-schema approach to create reusable schemas.

## SDK Reference

See `lumen_sdk.py` for full API documentation.

### Key Methods

- `LumenAuth.login(email, password)` - Authenticate and get token
- `LumenAuth.register(email, password)` - Register new account
- `LumenClient.query(query, model, temperature, ...)` - Send query
- `LumenClient.stream(query, model, temperature, ...)` - Stream response
- `LumenClient.get_keys()` - Get public verification keys

## Notes

**Free Tier Limitations:**
- Only `gpt-5-nano` model available
- Temperature must be 1.0 (not configurable)
- 50 requests/day
- Upgrade to Starter tier for full features

## Project Structure

```
lumen-greg/
├── lumen_cli.py           # CLI application
├── lumen_sdk.py           # Python SDK
├── example_*.py           # Example integrations
├── schema_generator.py    # Schema generation demo
├── generate_schema.py     # Interactive schema generator
├── examples.sh            # Shell script with usage examples
├── setup.py              # Package installation
├── requirements.txt       # Dependencies
├── README.md             # Documentation
└── SCHEMA_REFERENCE.md   # JSON schema guide
```

## Configuration

Credentials are stored securely in `~/.lumen/config.json`

The config includes:
- JWT token (auto-expires after 7 days)
- Email
- User information (tier, usage stats)

## Features

- ✅ Secure credential storage
- ✅ JWT token management
- ✅ Interactive password prompts (hidden input)
- ✅ Status checking with usage info
- ✅ Account registration support
