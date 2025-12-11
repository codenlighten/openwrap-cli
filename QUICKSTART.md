# LumenAI Quick Start Guide

## 1. Login

```bash
python lumen_cli.py login
```

Enter your email and password when prompted. Your token will be saved to `~/.lumen/config.json`.

## 2. Test Your Connection

```bash
python lumen_cli.py status
```

You should see your email and token information.

## 3. First Query

```bash
python lumen_cli.py query "What is 2+2?"
```

## 4. Try Streaming

```bash
python lumen_cli.py stream "Write a haiku about coding"
```

## 5. Use the SDK

Create a file `test.py`:

```python
from lumen_sdk import LumenClient
import json
from pathlib import Path

# Load saved token
config = json.load(open(Path.home() / ".lumen" / "config.json"))
client = LumenClient(config['token'])

# Query
result = client.query("Hello!")
print(result['data']['response'])
```

Run it:
```bash
python test.py
```

## 6. Run Examples

Try the included examples:

```bash
# Entity extraction
python example_data_extraction.py

# Code review
python example_code_review.py

# Interactive chat
python example_chatbot.py
```

## Common Commands

| Command | Description |
|---------|-------------|
| `lumen_cli.py login` | Login and save credentials |
| `lumen_cli.py status` | Check login status and usage |
| `lumen_cli.py query "text"` | Send a query |
| `lumen_cli.py stream "text"` | Stream a response |
| `lumen_cli.py keys` | Get public verification keys |
| `lumen_cli.py logout` | Clear saved credentials |

## Troubleshooting

**"Not logged in" error?**
- Run `python lumen_cli.py login` first

**"Invalid token" error?**
- Tokens expire after 7 days
- Login again: `python lumen_cli.py login`

**"Temperature not supported" error?**
- Free tier only supports temperature=1.0
- Use `gpt-5-nano` model only

**Rate limit error?**
- Free tier: 50 requests/day
- Check usage: `python lumen_cli.py status`
- Upgrade at https://open-wrapper.codenlighten.org/

## Next Steps

- Explore the full CLI: `python lumen_cli.py --help`
- Read SDK docs in `lumen_sdk.py`
- Build your own integrations
- Check out advanced examples

## Support

- Website: https://open-wrapper.codenlighten.org/
- Documentation: See README.md
- Examples: See `examples.sh`
