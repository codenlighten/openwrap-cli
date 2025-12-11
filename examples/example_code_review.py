#!/usr/bin/env python3
"""
Example: Using LumenAI for code review
"""
from lumen_sdk import LumenClient
import json
from pathlib import Path


def load_token():
    """Load token from config"""
    config_file = Path.home() / ".lumen" / "config.json"
    with open(config_file) as f:
        return json.load(f)['token']


def review_code(code: str, language: str = "python") -> dict:
    """Review code and return structured feedback"""
    client = LumenClient(load_token())
    
    prompt = f"""Review this {language} code and provide structured feedback:

```{language}
{code}
```

Format as JSON with:
- issues: array of {{severity, line, description}}
- suggestions: array of improvement suggestions
- overall_quality: Poor/Fair/Good/Excellent"""
    
    result = client.query(
        prompt,
        model="gpt-5-nano",
        temperature=1.0
    )
    
    return result


if __name__ == "__main__":
    sample_code = """
def calculate_sum(numbers):
    total = 0
    for i in range(len(numbers)):
        total = total + numbers[i]
    return total

result = calculate_sum([1, 2, 3, 4, 5])
print(result)
"""
    
    print("🔍 Code Review Example")
    print("=" * 50)
    print("\nCode to review:")
    print(sample_code)
    print("\n" + "=" * 50)
    print("Review Results:\n")
    
    review = review_code(sample_code)
    print(json.dumps(review['data'], indent=2))
