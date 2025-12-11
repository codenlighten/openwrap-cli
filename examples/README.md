# Examples Directory

This directory contains practical examples demonstrating different use cases of the LumenAI CLI and SDK.

## Running Examples

All examples require authentication. Make sure you're logged in first:

```bash
python ../lumen_cli.py login
```

## Available Examples

### 1. Data Extraction (`example_data_extraction.py`)

Extract structured entities from unstructured text.

```bash
python example_data_extraction.py
```

**What it does**:
- Defines a strict JSON schema for entities (people, organizations, locations, dates)
- Extracts structured data from a news article
- Validates output against schema

**Use cases**:
- Document processing
- Information extraction
- Database population from text

---

### 2. Code Review (`example_code_review.py`)

Automated code review with structured feedback.

```bash
python example_code_review.py
```

**What it does**:
- Defines schema for code review (issues, suggestions, severity)
- Reviews Python code for quality, security, performance
- Returns structured feedback

**Use cases**:
- Automated PR reviews
- Code quality checks
- Security audits

---

### 3. Interactive Chatbot (`example_chatbot.py`)

Context-aware chatbot with conversation history.

```bash
python example_chatbot.py
```

**What it does**:
- Maintains conversation context across turns
- Streaming responses for real-time interaction
- Graceful exit handling

**Use cases**:
- Customer support
- Interactive assistants
- Educational tools

---

### 4. Strict Schema Validation (`example_strict_schema.py`)

Demonstrate strict JSON schema validation with `additionalProperties: false`.

```bash
python example_strict_schema.py
```

**What it does**:
- Creates schemas with strict validation
- Ensures no extra fields in responses
- Multiple extraction examples (person, product, event)

**Use cases**:
- API response validation
- Data quality assurance
- Type-safe data pipelines

---

## Advanced Examples (Parent Directory)

### Recursive Research Agent (`../recursive_researcher.py`)

Automatically explore knowledge branches using `missingContext`.

```bash
python ../recursive_researcher.py deep
```

**Modes**:
- `deep` - Deep recursive research
- `multi` - Multi-schema extraction
- `pipeline` - Chained agent pipeline

---

### Agent Orchestration Patterns (`../agent_patterns.py`)

Multi-agent collaboration patterns.

```bash
python ../agent_patterns.py synthesis
```

**Modes**:
- `graph` - Build knowledge graphs
- `compare` - Comparative analysis
- `refine` - Iterative refinement
- `synthesis` - Multi-agent synthesis

---

### Ultimate Demo (`../ultimate_demo.py`)

Complete demonstration of the cognitive architecture.

```bash
python ../ultimate_demo.py
```

**Showcases**:
- Recursive deep research
- Schema-driven extraction
- Multi-agent collaboration
- Iterative refinement with missingContext

---

## Creating Your Own Examples

### Basic Pattern

```python
from lumen_sdk import LumenClient
import json
from pathlib import Path

# Load credentials
config_file = Path.home() / ".lumen" / "config.json"
with open(config_file, 'r') as f:
    config = json.load(f)

client = LumenClient(config['token'])

# Your code here
result = client.query(
    "Your prompt",
    model="gpt-5-nano",
    temperature=1.0
)

print(result['data']['response'])
```

### With Schema Validation

```python
schema = {
    "type": "object",
    "properties": {
        "field1": {"type": "string"},
        "field2": {"type": "number"}
    },
    "required": ["field1"],
    "additionalProperties": False
}

# Note: Free tier may not support output_schema parameter
# Use prompting instead:
prompt = f"""Extract data according to this schema:
{json.dumps(schema, indent=2)}

Text: "your text here"

Return ONLY valid JSON."""

result = client.query(prompt, model="gpt-5-nano", temperature=1.0)
```

### With Streaming

```python
for chunk in client.stream(
    "Your prompt",
    model="gpt-5-nano",
    temperature=1.0
):
    print(chunk, end='', flush=True)
```

## Tips

1. **Free Tier Limits**:
   - 50 requests/day
   - gpt-5-nano only
   - temperature fixed at 1.0

2. **Rate Limiting**:
   - Add delays between requests (0.5-1 second)
   - Use `time.sleep()` in loops

3. **Error Handling**:
   - Check for 401 errors (token expired)
   - Handle JSON parsing errors
   - Validate schema extraction results

4. **Schema Design**:
   - Keep schemas simple and focused
   - Use `additionalProperties: false` for strict validation
   - Test schemas with various inputs

5. **Cost Management**:
   - Monitor usage with `lumen_cli.py status`
   - Use streaming for long responses
   - Cache results when possible

## Contributing

Have a cool example? Submit a PR with:
- Clear documentation
- Error handling
- Free tier compatibility
- Usage instructions

## Questions?

Check the main [README](../README.md) or [ARCHITECTURE](../ARCHITECTURE.md) docs.
