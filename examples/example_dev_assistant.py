#!/usr/bin/env python3
"""
Example: Autonomous Development Assistant

Demonstrates how to build a development assistant that:
- Generates code from natural language
- Plans terminal command sequences
- Debugs errors with recursive context exploration
- Reviews code with multi-perspective analysis
"""

import sys
import os
from pathlib import Path
import json

# Add parent directory to path for imports
parent = str(Path(__file__).parent.parent)
sys.path.insert(0, parent)

from lumen_sdk import LumenClient, LumenAuth
from recursive_researcher import RecursiveResearcher


def get_client():
    """Load token from config and create client"""
    from pathlib import Path
    import json
    
    config_file = Path.home() / ".lumen" / "config.json"
    if not config_file.exists():
        print("❌ Not logged in. Please run: lumen-cli login")
        sys.exit(1)
    
    with open(config_file) as f:
        config = json.load(f)
        token = config.get('token')
    
    if not token:
        print("❌ No token found. Please run: lumen-cli login")
        sys.exit(1)
    
    return LumenClient(token)


class DevelopmentAssistant:
    """Self-aware development assistant using recursive research"""
    
    def __init__(self, client: LumenClient):
        self.client = client
        self.researcher = RecursiveResearcher(client, max_depth=2)
    
    def generate_code(self, requirement: str, context: dict = None):
        """Generate code from natural language requirement"""
        
        prompt = f"""Generate production-ready code for the following requirement:

{requirement}

Context:
{json.dumps(context or {}, indent=2)}

Provide:
1. Implementation code with proper error handling
2. Required dependencies
3. Test cases
4. Usage example

Format as JSON with keys: code, dependencies, tests, usage"""

        # Use schema for structured output
        schema = {
            "type": "object",
            "properties": {
                "code": {"type": "string"},
                "dependencies": {"type": "array", "items": {"type": "string"}},
                "tests": {"type": "string"},
                "usage": {"type": "string"},
                "explanation": {"type": "string"}
            },
            "required": ["code", "dependencies", "tests", "usage"],
            "additionalProperties": False
        }
        
        result = self.researcher.research(prompt, schema=schema)
        return result.extracted_data if result.extracted_data else result.answer
    
    def plan_terminal_commands(self, task: str):
        """Plan a sequence of terminal commands for a task"""
        
        prompt = f"""Plan terminal commands to accomplish: {task}

For each command provide:
- cmd: The actual command to run
- purpose: What it does
- safe: Boolean indicating if it's safe to run automatically
- abort_on_failure: Whether to stop if this command fails

Format as JSON array of command objects."""

        schema = {
            "type": "object",
            "properties": {
                "commands": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "cmd": {"type": "string"},
                            "purpose": {"type": "string"},
                            "safe": {"type": "boolean"},
                            "abort_on_failure": {"type": "boolean"}
                        },
                        "required": ["cmd", "purpose", "safe"]
                    }
                },
                "rollback_commands": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "required": ["commands"],
            "additionalProperties": False
        }
        
        result = self.researcher.research(prompt, schema=schema)
        return result.extracted_data if result.extracted_data else {"commands": []}
    
    def debug_error(self, error_log: str, codebase_context: str = ""):
        """Analyze error and suggest fixes"""
        
        prompt = f"""Analyze this error and provide a fix:

ERROR LOG:
{error_log}

CODEBASE CONTEXT:
{codebase_context}

Provide:
1. Root cause analysis
2. Affected code locations
3. Fix strategy
4. Code changes (diff format)
5. Test cases to prevent regression"""

        schema = {
            "type": "object",
            "properties": {
                "root_cause": {"type": "string"},
                "affected_code": {"type": "array", "items": {"type": "string"}},
                "fix_strategy": {"type": "string"},
                "code_changes": {"type": "string"},
                "test_cases": {"type": "array", "items": {"type": "string"}},
                "prevention_tips": {"type": "string"}
            },
            "required": ["root_cause", "fix_strategy", "code_changes"],
            "additionalProperties": False
        }
        
        result = self.researcher.research(prompt, schema=schema)
        return result.extracted_data if result.extracted_data else {}
    
    def review_code(self, code: str, focus_areas: list = None):
        """Review code like a senior engineer"""
        
        focus = focus_areas or ["security", "performance", "maintainability"]
        
        prompt = f"""Review this code focusing on: {', '.join(focus)}

CODE:
{code}

Provide detailed analysis for each focus area with:
- Issues found (severity, location, description)
- Suggestions for improvement
- Code examples of fixes"""

        schema = {
            "type": "object",
            "properties": {
                "security_issues": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "severity": {"type": "string"},
                            "location": {"type": "string"},
                            "issue": {"type": "string"},
                            "fix": {"type": "string"}
                        }
                    }
                },
                "performance_issues": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "location": {"type": "string"},
                            "issue": {"type": "string"},
                            "fix": {"type": "string"}
                        }
                    }
                },
                "maintainability_suggestions": {"type": "array", "items": {"type": "string"}},
                "overall_assessment": {"type": "string"}
            },
            "additionalProperties": False
        }
        
        result = self.researcher.research(prompt, schema=schema)
        return result.extracted_data if result.extracted_data else {}


def demo_code_generation():
    """Demo: Generate code from natural language"""
    print("\n" + "="*70)
    print("DEMO 1: Code Generation from Natural Language")
    print("="*70)
    
    client = get_client()
    assistant = DevelopmentAssistant(client)
    
    requirement = """
    Create a Python function that:
    - Takes a list of URLs
    - Fetches content from each URL concurrently
    - Returns a dictionary mapping URLs to their content
    - Has proper timeout handling (5 seconds per request)
    - Uses async/await
    """
    
    context = {
        "language": "Python 3.10+",
        "libraries": ["aiohttp", "asyncio"],
        "style": "Type hints and docstrings required"
    }
    
    print(f"\n📝 Requirement:\n{requirement}")
    print(f"\n🔧 Context:\n{json.dumps(context, indent=2)}")
    print("\n⏳ Generating code...\n")
    
    result = assistant.generate_code(requirement, context)
    
    if isinstance(result, dict):
        print("✅ Generated Code:")
        print("-" * 70)
        print(result.get('code', 'No code generated'))
        print("\n📦 Dependencies:")
        for dep in result.get('dependencies', []):
            print(f"  - {dep}")
        print("\n🧪 Tests:")
        print(result.get('tests', 'No tests generated'))
        print("\n💡 Usage Example:")
        print(result.get('usage', 'No usage example'))
    else:
        print(result)


def demo_terminal_commands():
    """Demo: Plan terminal command sequences"""
    print("\n" + "="*70)
    print("DEMO 2: Terminal Command Planning")
    print("="*70)
    
    client = get_client()
    assistant = DevelopmentAssistant(client)
    
    task = "Set up a new FastAPI project with PostgreSQL, Redis, and Docker"
    
    print(f"\n🎯 Task: {task}")
    print("\n⏳ Planning command sequence...\n")
    
    result = assistant.plan_terminal_commands(task)
    
    if isinstance(result, dict) and 'commands' in result:
        print("✅ Command Plan:")
        print("-" * 70)
        for i, cmd in enumerate(result['commands'], 1):
            safety = "✅ SAFE" if cmd.get('safe') else "⚠️  REQUIRES REVIEW"
            abort = "🛑 ABORT ON FAILURE" if cmd.get('abort_on_failure') else "⏭️  CONTINUE ON FAILURE"
            
            print(f"\n{i}. {cmd['purpose']}")
            print(f"   Command: {cmd['cmd']}")
            print(f"   Safety:  {safety}")
            print(f"   On Fail: {abort}")
        
        if result.get('rollback_commands'):
            print("\n🔙 Rollback Plan:")
            for cmd in result['rollback_commands']:
                print(f"  - {cmd}")
    else:
        print(result)


def demo_debugging():
    """Demo: Debug error with recursive context exploration"""
    print("\n" + "="*70)
    print("DEMO 3: Error Debugging with Context Exploration")
    print("="*70)
    
    client = get_client()
    assistant = DevelopmentAssistant(client)
    
    error_log = """
Traceback (most recent call last):
  File "api/users.py", line 47, in create_user
    user = User(email=email, password=hash_password(password))
  File "models/user.py", line 12, in __init__
    self.validate_email(email)
  File "models/user.py", line 18, in validate_email
    raise ValueError("Invalid email format")
ValueError: Invalid email format

Input was: user@company-name.com
"""
    
    codebase_context = """
# models/user.py
import re

class User:
    def validate_email(self, email):
        pattern = r'^[a-zA-Z0-9._]+@[a-zA-Z0-9]+\\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise ValueError("Invalid email format")
"""
    
    print(f"\n❌ Error Log:\n{error_log}")
    print(f"\n📄 Relevant Code:\n{codebase_context}")
    print("\n⏳ Analyzing error...\n")
    
    result = assistant.debug_error(error_log, codebase_context)
    
    if isinstance(result, dict):
        print("✅ Debug Analysis:")
        print("-" * 70)
        print(f"\n🔍 Root Cause:\n{result.get('root_cause', 'Unknown')}")
        print(f"\n💡 Fix Strategy:\n{result.get('fix_strategy', 'Unknown')}")
        print(f"\n🔧 Code Changes:\n{result.get('code_changes', 'None')}")
        
        if result.get('test_cases'):
            print("\n🧪 Suggested Test Cases:")
            for test in result['test_cases']:
                print(f"  - {test}")
        
        if result.get('prevention_tips'):
            print(f"\n🛡️  Prevention Tips:\n{result['prevention_tips']}")
    else:
        print(result)


def demo_code_review():
    """Demo: Multi-perspective code review"""
    print("\n" + "="*70)
    print("DEMO 4: Code Review with Multiple Perspectives")
    print("="*70)
    
    client = get_client()
    assistant = DevelopmentAssistant(client)
    
    code = """
def get_user_data(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE id = {user_id}"
    result = cursor.execute(query).fetchone()
    conn.close()
    return result

def process_users(user_ids):
    results = []
    for uid in user_ids:
        data = get_user_data(uid)
        results.append(data)
    return results
"""
    
    print(f"\n📄 Code Under Review:\n{code}")
    print("\n⏳ Performing multi-perspective analysis...\n")
    
    result = assistant.review_code(code, focus_areas=["security", "performance", "maintainability"])
    
    if isinstance(result, dict):
        print("✅ Code Review Results:")
        print("-" * 70)
        
        if result.get('security_issues'):
            print("\n🔒 Security Issues:")
            for issue in result['security_issues']:
                print(f"\n  [{issue.get('severity', 'UNKNOWN')}] {issue.get('location', 'Unknown location')}")
                print(f"  Issue: {issue.get('issue', 'Unknown issue')}")
                print(f"  Fix: {issue.get('fix', 'No fix provided')}")
        
        if result.get('performance_issues'):
            print("\n⚡ Performance Issues:")
            for issue in result['performance_issues']:
                print(f"\n  Location: {issue.get('location', 'Unknown')}")
                print(f"  Issue: {issue.get('issue', 'Unknown')}")
                print(f"  Fix: {issue.get('fix', 'No fix')}")
        
        if result.get('maintainability_suggestions'):
            print("\n🔧 Maintainability Suggestions:")
            for suggestion in result['maintainability_suggestions']:
                print(f"  - {suggestion}")
        
        if result.get('overall_assessment'):
            print(f"\n📊 Overall Assessment:\n{result['overall_assessment']}")
    else:
        print(result)


def main():
    """Run all development assistant demos"""
    print("\n" + "="*70)
    print("🛠️  AUTONOMOUS DEVELOPMENT ASSISTANT DEMO")
    print("="*70)
    print("\nDemonstrating how missingContext enables self-aware coding assistants")
    print("that understand your codebase, research best practices, and generate")
    print("production-ready code with tests and documentation.")
    
    try:
        # Demo 1: Code Generation
        demo_code_generation()
        
        input("\n\n⏸️  Press Enter to continue to next demo...")
        
        # Demo 2: Terminal Commands
        demo_terminal_commands()
        
        input("\n\n⏸️  Press Enter to continue to next demo...")
        
        # Demo 3: Debugging
        demo_debugging()
        
        input("\n\n⏸️  Press Enter to continue to next demo...")
        
        # Demo 4: Code Review
        demo_code_review()
        
        print("\n" + "="*70)
        print("✅ ALL DEMOS COMPLETE")
        print("="*70)
        print("\nKey Takeaways:")
        print("1. Agents can generate context-aware code matching your patterns")
        print("2. Terminal command planning includes safety checks and rollback")
        print("3. Debugging explores error context recursively via missingContext")
        print("4. Code review applies multiple expert perspectives simultaneously")
        print("\n💡 The same cognitive architecture powers all four capabilities!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error running demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
