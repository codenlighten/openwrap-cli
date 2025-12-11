#!/bin/bash
# LumenAI CLI Examples

echo "=== Authentication ==="
# Login
python lumen_cli.py login

# Check status
python lumen_cli.py status

echo ""
echo "=== Basic Queries ==="
# Simple query
python lumen_cli.py query "What is Python?"

# With specific model
python lumen_cli.py query "Explain machine learning" --model gpt-5-mini

# With temperature control
python lumen_cli.py query "Write a creative story" --temperature 1.5

echo ""
echo "=== Streaming ==="
# Stream response
python lumen_cli.py stream "Write a poem about AI"

# Stream with different model
python lumen_cli.py stream "Explain quantum computing" --model gpt-5-mini

echo ""
echo "=== Advanced Features ==="
# Structured output with JSON schema
python lumen_cli.py query "List 3 programming languages" \
  --schema '{"type":"object","properties":{"languages":{"type":"array","items":{"type":"string"}}}}'

# With ECDSA signature
python lumen_cli.py query "Hello world" --signature ecdsa

# With post-quantum signature
python lumen_cli.py query "Hello world" --signature pqc

# Hybrid signatures (both)
python lumen_cli.py query "Hello world" --signature hybrid

# Get full JSON response
python lumen_cli.py query "What is AI?" --json

echo ""
echo "=== Verification Keys ==="
# Get public keys for signature verification
python lumen_cli.py keys
