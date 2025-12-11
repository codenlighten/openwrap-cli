#!/usr/bin/env python3
"""
Example: Interactive chatbot using LumenAI streaming
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lumen_sdk import LumenClient
import json


def load_token():
    """Load token from config"""
    config_file = Path.home() / ".lumen" / "config.json"
    with open(config_file) as f:
        return json.load(f)['token']


def chat():
    """Interactive chat loop"""
    client = LumenClient(load_token())
    
    print("🤖 LumenAI Interactive Chat")
    print("=" * 50)
    print("Type 'quit' or 'exit' to end the conversation\n")
    
    conversation_history = []
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break
        
        if not user_input:
            continue
        
        # Add context from previous messages
        context = "\n".join([
            f"User: {msg['user']}\nAssistant: {msg['assistant']}"
            for msg in conversation_history[-3:]  # Last 3 exchanges
        ])
        
        if context:
            prompt = f"Previous conversation:\n{context}\n\nUser: {user_input}\n\nAssistant:"
        else:
            prompt = user_input
        
        print("Assistant: ", end='', flush=True)
        
        # Stream the response
        response_text = ""
        try:
            for chunk in client.stream(prompt, model="gpt-5-nano", temperature=1.0):
                print(chunk, end='', flush=True)
                response_text += chunk
            print("\n")
            
            # Save to history
            conversation_history.append({
                "user": user_input,
                "assistant": response_text
            })
            
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    try:
        chat()
    except KeyboardInterrupt:
        print("\n\n👋 Chat ended")
        sys.exit(0)
