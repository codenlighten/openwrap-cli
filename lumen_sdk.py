#!/usr/bin/env python3
"""
LumenAI SDK - Python SDK for programmatic access to LumenAI API
"""
import json
import requests
from typing import Optional, Dict, Any, Iterator


class LumenClient:
    """Python client for LumenAI API Gateway"""
    
    def __init__(self, token: str, base_url: str = "https://open-wrapper.codenlighten.org"):
        """
        Initialize LumenAI client
        
        Args:
            token: JWT authentication token
            base_url: Base URL for LumenAI API
        """
        self.token = token
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })
    
    def query(
        self,
        query: str,
        model: str = "gpt-5-nano",
        temperature: float = 1.0,
        max_tokens: Optional[int] = None,
        output_schema: Optional[Dict[str, Any]] = None,
        signature_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send a query to LumenAI
        
        Args:
            query: The prompt/question to send
            model: Model to use (gpt-5-nano, gpt-5-mini, gpt-5-1, gpt-5-pro, gpt-4o-mini)
            temperature: Temperature for response randomness (0.0-2.0)
            max_tokens: Maximum tokens to generate
            output_schema: JSON schema for structured output. Can include:
                - properties: Define allowed fields and their types
                - required: Array of mandatory field names
                - additionalProperties: Set to False to reject extra fields
                Example: {
                    "type": "object",
                    "properties": {"name": {"type": "string"}},
                    "required": ["name"],
                    "additionalProperties": False
                }
            signature_type: Signature type (ecdsa, pqc, hybrid)
        
        Returns:
            API response as dictionary
        
        Raises:
            requests.HTTPError: If API request fails
        """
        payload = {
            "query": query,
            "model": model,
            "temperature": temperature
        }
        
        if max_tokens:
            payload["max_tokens"] = max_tokens
        if output_schema:
            payload["output_schema"] = output_schema
        if signature_type:
            payload["signature_type"] = signature_type
        
        response = self.session.post(
            f"{self.base_url}/api/query",
            json=payload
        )
        
        # Debug logging
        if response.status_code != 200:
            print(f"Error {response.status_code}: {response.text}", file=__import__('sys').stderr)
        
        response.raise_for_status()
        return response.json()
    
    def stream(
        self,
        query: str,
        model: str = "gpt-5-nano",
        temperature: float = 1.0,
        max_tokens: Optional[int] = None
    ) -> Iterator[str]:
        """
        Stream a query response from LumenAI
        
        Args:
            query: The prompt/question to send
            model: Model to use
            temperature: Temperature for response randomness
            max_tokens: Maximum tokens to generate
        
        Yields:
            Response chunks as they arrive
        
        Raises:
            requests.HTTPError: If API request fails
        """
        payload = {
            "query": query,
            "model": model,
            "temperature": temperature
        }
        
        if max_tokens:
            payload["max_tokens"] = max_tokens
        
        response = self.session.post(
            f"{self.base_url}/api/query/stream",
            json=payload,
            stream=True
        )
        response.raise_for_status()
        
        for line in response.iter_lines(decode_unicode=True):
            if line and line.startswith('data: '):
                data_str = line[6:]
                try:
                    data = json.loads(data_str)
                    if 'chunk' in data:
                        yield data['chunk']
                    elif data.get('done'):
                        break
                except json.JSONDecodeError:
                    continue
    
    def get_keys(self) -> Dict[str, Any]:
        """
        Get public keys for signature verification
        
        Returns:
            Dictionary containing ECDSA and PQ public keys
        
        Raises:
            requests.HTTPError: If API request fails
        """
        response = requests.get(f"{self.base_url}/api/query/keys")
        response.raise_for_status()
        return response.json()
    
    def openai_chat(
        self,
        messages: list,
        model: str = "gpt-5-nano",
        temperature: float = 1.0,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        OpenAI-compatible chat completions endpoint
        
        Args:
            messages: List of message objects with 'role' and 'content'
            model: Model to use
            temperature: Temperature for response randomness
            max_tokens: Maximum tokens to generate
            stream: Whether to stream the response
        
        Returns:
            Chat completion response
        
        Raises:
            requests.HTTPError: If API request fails
        """
        payload = {
            "messages": messages,
            "model": model,
            "temperature": temperature,
            "stream": stream
        }
        
        if max_tokens:
            payload["max_tokens"] = max_tokens
        
        response = self.session.post(
            f"{self.base_url}/api/openai/chat",
            json=payload
        )
        response.raise_for_status()
        return response.json()


class LumenAuth:
    """Authentication helper for LumenAI"""
    
    def __init__(self, base_url: str = "https://open-wrapper.codenlighten.org"):
        self.base_url = base_url
    
    def register(self, email: str, password: str) -> Dict[str, Any]:
        """
        Register a new account
        
        Args:
            email: Email address
            password: Password
        
        Returns:
            Registration response
        
        Raises:
            requests.HTTPError: If registration fails
        """
        response = requests.post(
            f"{self.base_url}/api/auth/register",
            json={"email": email, "password": password},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()
    
    def login(self, email: str, password: str) -> str:
        """
        Login and get JWT token
        
        Args:
            email: Email address
            password: Password
        
        Returns:
            JWT authentication token
        
        Raises:
            requests.HTTPError: If login fails
        """
        response = requests.post(
            f"{self.base_url}/api/auth/login",
            json={"email": email, "password": password},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        data = response.json()
        return data.get('token') or data.get('access_token')


# Example usage
if __name__ == "__main__":
    # Authenticate
    auth = LumenAuth()
    # token = auth.login("your@email.com", "your_password")
    
    # Use pre-existing token
    from pathlib import Path
    import json
    
    config_file = Path.home() / ".lumen" / "config.json"
    if config_file.exists():
        with open(config_file) as f:
            config = json.load(f)
            token = config.get('token')
    else:
        print("Please login first using: python lumen_cli.py login")
        exit(1)
    
    # Create client
    client = LumenClient(token)
    
    # Simple query
    print("=== Simple Query ===")
    result = client.query("What is 2+2?")
    print(result['data']['response'])
    print()
    
    # Stream query
    print("=== Streaming Query ===")
    for chunk in client.stream("Write a haiku about coding"):
        print(chunk, end='', flush=True)
    print("\n")
    
    # Structured output
    print("=== Structured Output ===")
    schema = {
        "type": "object",
        "properties": {
            "languages": {
                "type": "array",
                "items": {"type": "string"}
            }
        }
    }
    result = client.query("List 3 programming languages", output_schema=schema)
    print(json.dumps(result['data'], indent=2))
