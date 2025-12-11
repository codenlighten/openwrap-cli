#!/usr/bin/env python3
"""
LumenAI CLI - Command-line interface for LumenAI API Gateway
"""
import argparse
import json
import os
import sys
from pathlib import Path
import requests
from getpass import getpass
from typing import Optional, Dict, Any


class LumenCLI:
    BASE_URL = "https://open-wrapper.codenlighten.org"
    CONFIG_DIR = Path.home() / ".lumen"
    CONFIG_FILE = CONFIG_DIR / "config.json"
    
    def __init__(self):
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        if self.CONFIG_FILE.exists():
            with open(self.CONFIG_FILE, 'r') as f:
                return json.load(f)
        return {}
    
    def save_config(self):
        """Save configuration to file"""
        self.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(self.CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=2)
        # Secure the config file (Unix-like systems)
        if os.name != 'nt':
            os.chmod(self.CONFIG_FILE, 0o600)
    
    def login(self, email=None, password=None):
        """Login to LumenAI"""
        print("🔆 LumenAI Login")
        print("-" * 40)
        
        # Get credentials
        if not email:
            email = input("Email: ")
        if not password:
            password = getpass("Password: ")
        
        # Make login request
        try:
            response = requests.post(
                f"{self.BASE_URL}/api/auth/login",
                json={
                    "email": email,
                    "password": password
                },
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Save token and user info
                self.config['token'] = data.get('token') or data.get('access_token')
                self.config['email'] = email
                self.config['user'] = data.get('user', {})
                self.save_config()
                
                print("\n✅ Login successful!")
                print(f"Logged in as: {email}")
                if 'tier' in self.config['user']:
                    print(f"Subscription tier: {self.config['user']['tier']}")
                return True
            else:
                print(f"\n❌ Login failed: {response.status_code}")
                try:
                    error = response.json()
                    print(f"Error: {error.get('error', error.get('message', 'Unknown error'))}")
                except:
                    print(f"Error: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"\n❌ Connection error: {e}")
            return False
    
    def logout(self):
        """Logout and clear stored credentials"""
        if self.CONFIG_FILE.exists():
            self.CONFIG_FILE.unlink()
            print("✅ Logged out successfully")
        else:
            print("ℹ️  Not currently logged in")
    
    def status(self):
        """Show current login status"""
        if not self.config.get('token'):
            print("❌ Not logged in")
            print(f"Run: {sys.argv[0]} login")
            return False
        
        print("✅ Logged in")
        print(f"Email: {self.config.get('email')}")
        if 'user' in self.config:
            user = self.config['user']
            if 'tier' in user:
                print(f"Tier: {user['tier']}")
            if 'requests_today' in user:
                print(f"Requests today: {user['requests_today']}")
        print(f"\nToken: {self.config['token'][:20]}...")
        return True
    
    def register(self, email=None, password=None):
        """Register a new account"""
        print("🔆 LumenAI Registration")
        print("-" * 40)
        
        if not email:
            email = input("Email: ")
        if not password:
            password = getpass("Password: ")
            password_confirm = getpass("Confirm Password: ")
            if password != password_confirm:
                print("❌ Passwords don't match")
                return False
        
        try:
            response = requests.post(
                f"{self.BASE_URL}/api/auth/register",
                json={
                    "email": email,
                    "password": password
                },
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code in [200, 201]:
                print("\n✅ Registration successful!")
                print("You can now login with your credentials")
                return True
            else:
                print(f"\n❌ Registration failed: {response.status_code}")
                try:
                    error = response.json()
                    print(f"Error: {error.get('error', error.get('message', 'Unknown error'))}")
                except:
                    print(f"Error: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"\n❌ Connection error: {e}")
            return False
    
    def query(self, prompt, model="gpt-5-nano", temperature=1.0, max_tokens=None, 
              output_schema=None, signature_type=None):
        """Query LumenAI with structured output"""
        if not self.config.get('token'):
            print("❌ Not logged in. Run: lumen_cli.py login")
            return None
        
        payload = {
            "query": prompt,
            "model": model,
            "temperature": temperature
        }
        
        if max_tokens:
            payload["max_tokens"] = max_tokens
        if output_schema:
            payload["output_schema"] = output_schema
        if signature_type:
            payload["signature_type"] = signature_type
        
        try:
            response = requests.post(
                f"{self.BASE_URL}/api/query",
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.config['token']}"
                }
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                print("❌ Authentication failed. Token may have expired. Try logging in again.")
                return None
            else:
                print(f"❌ Query failed: {response.status_code}")
                print(f"Response: {response.text}")
                try:
                    error = response.json()
                    print(f"Error details: {json.dumps(error, indent=2)}")
                except:
                    pass
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection error: {e}")
            return None
    
    def stream_query(self, prompt, model="gpt-5-nano", temperature=1.0, max_tokens=None):
        """Stream query responses from LumenAI"""
        if not self.config.get('token'):
            print("❌ Not logged in. Run: lumen_cli.py login")
            return
        
        payload = {
            "query": prompt,
            "model": model,
            "temperature": temperature
        }
        
        if max_tokens:
            payload["max_tokens"] = max_tokens
        
        try:
            response = requests.post(
                f"{self.BASE_URL}/api/query/stream",
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.config['token']}"
                },
                stream=True
            )
            
            if response.status_code == 200:
                print()  # New line before streaming
                for line in response.iter_lines(decode_unicode=True):
                    if line and line.startswith('data: '):
                        data_str = line[6:]  # Remove 'data: ' prefix
                        try:
                            data = json.loads(data_str)
                            if 'chunk' in data:
                                print(data['chunk'], end='', flush=True)
                            elif data.get('done'):
                                print()  # New line after completion
                                break
                        except json.JSONDecodeError:
                            continue
            elif response.status_code == 401:
                print("❌ Authentication failed. Token may have expired. Try logging in again.")
            else:
                print(f"❌ Stream query failed: {response.status_code}")
                print(f"Response: {response.text}")
                try:
                    error = response.json()
                    print(f"Error details: {json.dumps(error, indent=2)}")
                except:
                    pass
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection error: {e}")
    
    def get_keys(self):
        """Get public keys for signature verification"""
        try:
            response = requests.get(f"{self.BASE_URL}/api/query/keys")
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Failed to get keys: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection error: {e}")
            return None
    
    def generate_schema(self, description: str) -> Optional[Dict[str, Any]]:
        """Generate a JSON schema from natural language description"""
        if not self.config.get('token'):
            print("❌ Not logged in. Run: lumen_cli.py login")
            return None
        
        # Example of proper schema format
        example = {
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "number", "minimum": 0}
                },
                "required": ["name"],
                "additionalProperties": False
            }
        }
        
        prompt = f"""Generate a JSON schema for: {description}

Return JSON in this exact format:
{json.dumps(example, indent=2)}

Guidelines:
- Use types: string, number, integer, boolean, array, object
- Add constraints: minimum, maximum, minLength, maxLength, enum, minItems, maxItems
- List required fields in "required" array
- Always set "additionalProperties": false
- Nest objects for complex structures

Return ONLY valid JSON."""
        
        try:
            result = self.query(prompt, model="gpt-5-nano", temperature=1.0)
            if not result:
                return None
            
            # Handle different response structures
            if 'data' in result and 'response' in result['data']:
                response_text = result['data']['response']
            elif 'response' in result:
                response_text = result['response']
            else:
                print(f"❌ Unexpected response structure: {json.dumps(result, indent=2)}")
                return None
            
            # Extract JSON from response
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0]
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0]
            
            generated = json.loads(response_text.strip())
            
            # Validate it has the schema key
            if 'schema' not in generated:
                # Sometimes the AI returns the schema directly without wrapping
                if 'type' in generated and 'properties' in generated:
                    # It's a schema, wrap it
                    generated = {'schema': generated}
                else:
                    print(f"❌ Generated response doesn't contain 'schema' key")
                    print(f"Response was: {response_text[:200]}...")
                    return None
            
            return generated
            
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse generated schema: {e}")
            return None
        except Exception as e:
            print(f"❌ Error generating schema: {e}")
            return None
    
    def validate_with_schema(self, text: str, schema: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract data from text using a schema"""
        if not self.config.get('token'):
            print("❌ Not logged in. Run: lumen_cli.py login")
            return None
        
        prompt = f"""Extract data from this text according to the schema:

Text: "{text}"

Schema: {json.dumps(schema, indent=2)}

Return data matching the schema exactly."""
        
        # Note: Currently free tier doesn't support output_schema parameter
        # So we rely on the prompt to guide the response format
        result = self.query(prompt, model="gpt-5-nano", temperature=1.0)
        return result


def main():
    parser = argparse.ArgumentParser(
        description="LumenAI CLI - Command-line interface for LumenAI API Gateway",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Login command
    login_parser = subparsers.add_parser('login', help='Login to LumenAI')
    login_parser.add_argument('--email', '-e', help='Email address')
    login_parser.add_argument('--password', '-p', help='Password (not recommended, will prompt if not provided)')
    
    # Logout command
    subparsers.add_parser('logout', help='Logout and clear credentials')
    
    # Status command
    subparsers.add_parser('status', help='Check login status')
    
    # Register command
    register_parser = subparsers.add_parser('register', help='Register new account')
    register_parser.add_argument('--email', '-e', help='Email address')
    register_parser.add_argument('--password', '-p', help='Password')
    
    # Query command
    query_parser = subparsers.add_parser('query', help='Send a query to LumenAI')
    query_parser.add_argument('prompt', help='The prompt to send')
    query_parser.add_argument('--model', '-m', default='gpt-5-nano', 
                             help='Model to use (default: gpt-5-nano)')
    query_parser.add_argument('--temperature', '-t', type=float, default=1.0,
                             help='Temperature (default: 1.0)')
    query_parser.add_argument('--max-tokens', type=int, help='Maximum tokens to generate')
    query_parser.add_argument('--schema', help='JSON schema for structured output (as JSON string)')
    query_parser.add_argument('--signature', choices=['ecdsa', 'pqc', 'hybrid'],
                             help='Signature type for response verification')
    query_parser.add_argument('--json', '-j', action='store_true',
                             help='Output full JSON response')
    
    # Stream command
    stream_parser = subparsers.add_parser('stream', help='Stream a query response')
    stream_parser.add_argument('prompt', help='The prompt to send')
    stream_parser.add_argument('--model', '-m', default='gpt-5-nano',
                              help='Model to use (default: gpt-5-nano)')
    stream_parser.add_argument('--temperature', '-t', type=float, default=1.0,
                              help='Temperature (default: 1.0)')
    stream_parser.add_argument('--max-tokens', type=int, help='Maximum tokens to generate')
    
    # Keys command
    subparsers.add_parser('keys', help='Get public keys for signature verification')
    
    # Generate schema command
    generate_parser = subparsers.add_parser('generate-schema', 
                                           help='Generate JSON schema from description')
    generate_parser.add_argument('description', help='Natural language description of the schema')
    generate_parser.add_argument('--save', '-s', help='Save schema to file')
    generate_parser.add_argument('--example', '-e', action='store_true',
                                help='Include example data in output')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate',
                                           help='Extract data from text using a schema file')
    validate_parser.add_argument('text', help='Text to extract data from')
    validate_parser.add_argument('--schema-file', '-f', required=True,
                                help='Path to JSON schema file')
    
    # List schemas command
    subparsers.add_parser('list-schemas', help='List saved schema files')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    cli = LumenCLI()
    
    if args.command == 'login':
        success = cli.login(args.email, args.password)
        sys.exit(0 if success else 1)
    
    elif args.command == 'logout':
        cli.logout()
    
    elif args.command == 'status':
        cli.status()
    
    elif args.command == 'register':
        success = cli.register(args.email, args.password)
        sys.exit(0 if success else 1)
    
    elif args.command == 'query':
        schema = None
        if args.schema:
            try:
                schema = json.loads(args.schema)
            except json.JSONDecodeError:
                print("❌ Invalid JSON schema")
                sys.exit(1)
        
        result = cli.query(
            args.prompt,
            model=args.model,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
            output_schema=schema,
            signature_type=args.signature
        )
        
        if result:
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                # Print just the response content
                if 'data' in result and 'response' in result['data']:
                    print(result['data']['response'])
                elif 'response' in result:
                    print(result['response'])
                elif 'content' in result:
                    print(result['content'])
                else:
                    print(json.dumps(result, indent=2))
            sys.exit(0)
        else:
            sys.exit(1)
    
    elif args.command == 'stream':
        cli.stream_query(
            args.prompt,
            model=args.model,
            temperature=args.temperature,
            max_tokens=args.max_tokens
        )
    
    elif args.command == 'keys':
        keys = cli.get_keys()
        if keys:
            print(json.dumps(keys, indent=2))
    
    elif args.command == 'generate-schema':
        print(f"🔧 Generating schema for: {args.description}")
        print("⏳ Please wait...\n")
        
        generated = cli.generate_schema(args.description)
        
        if generated and 'schema' in generated:
            schema = generated['schema']
            
            print("✅ Schema generated successfully:\n")
            print(json.dumps(schema, indent=2))
            
            if args.example and 'example' in generated:
                print("\n📋 Example data:\n")
                print(json.dumps(generated['example'], indent=2))
            
            # Save to file if requested
            if args.save:
                filename = args.save
                if not filename.endswith('.json'):
                    filename += '.json'
                
                with open(filename, 'w') as f:
                    json.dump(schema, f, indent=2)
                print(f"\n💾 Schema saved to: {filename}")
                print(f"Use with: python lumen_cli.py validate \"your text\" -f {filename}")
            
            sys.exit(0)
        else:
            print("❌ Failed to generate schema")
            sys.exit(1)
    
    elif args.command == 'validate':
        # Load schema from file
        schema_file = Path(args.schema_file)
        if not schema_file.exists():
            print(f"❌ Schema file not found: {args.schema_file}")
            sys.exit(1)
        
        with open(schema_file, 'r') as f:
            schema = json.load(f)
        
        print(f"📋 Using schema from: {args.schema_file}")
        print(f"📝 Extracting data from: {args.text[:50]}...")
        print("⏳ Please wait...\n")
        
        result = cli.validate_with_schema(args.text, schema)
        
        if result:
            print("✅ Extracted data:\n")
            response_text = result['data']['response']
            
            # Try to parse as JSON if possible
            try:
                if '```json' in response_text:
                    response_text = response_text.split('```json')[1].split('```')[0]
                elif '```' in response_text:
                    response_text = response_text.split('```')[1].split('```')[0]
                
                data = json.loads(response_text.strip())
                print(json.dumps(data, indent=2))
            except:
                # If not JSON, just print the response
                print(response_text)
            
            sys.exit(0)
        else:
            print("❌ Validation failed")
            sys.exit(1)
    
    elif args.command == 'list-schemas':
        # List JSON files in current directory
        schema_files = list(Path('.').glob('*.json'))
        
        if schema_files:
            print("📁 Schema files in current directory:\n")
            for schema_file in sorted(schema_files):
                # Try to read and show basic info
                try:
                    with open(schema_file, 'r') as f:
                        schema = json.load(f)
                    
                    # Count properties
                    props = schema.get('properties', {})
                    required = schema.get('required', [])
                    
                    print(f"  • {schema_file.name}")
                    print(f"    Properties: {len(props)}, Required: {len(required)}")
                except:
                    print(f"  • {schema_file.name}")
            print()
        else:
            print("📭 No schema files found in current directory")
            print("Create one with: python lumen_cli.py generate-schema \"your description\"")


if __name__ == "__main__":
    main()
