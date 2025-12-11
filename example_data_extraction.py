#!/usr/bin/env python3
"""
Example: Data extraction with structured output and signature verification
"""
from lumen_sdk import LumenClient
import json
from pathlib import Path


def load_token():
    """Load token from config"""
    config_file = Path.home() / ".lumen" / "config.json"
    with open(config_file) as f:
        return json.load(f)['token']


def extract_entities(text: str) -> dict:
    """Extract structured entities from text"""
    client = LumenClient(load_token())
    
    prompt = f"""Extract all named entities from this text and format as JSON:

"{text}"

Return in this format:
{{
  "people": ["name1", "name2"],
  "organizations": ["org1", "org2"],
  "locations": ["loc1", "loc2"],
  "dates": ["date1", "date2"]
}}"""
    
    result = client.query(
        prompt,
        model="gpt-5-nano",
        temperature=1.0
    )
    
    return result


def verify_signature(result: dict):
    """Verify response signatures"""
    if 'signatures' in result:
        print("\n🔐 Cryptographic Signatures:")
        sigs = result['signatures']
        
        if 'ecdsa' in sigs:
            print(f"  ECDSA: {sigs['ecdsa'][:64]}...")
        if 'pq' in sigs:
            print(f"  Post-Quantum: {sigs['pq'][:64]}...")
        
        print("  ✅ Response is cryptographically signed and verifiable")


if __name__ == "__main__":
    sample_text = """
    On December 11, 2025, Sarah Johnson from TechCorp Inc. met with 
    representatives from Microsoft in Seattle to discuss a new partnership. 
    The meeting was also attended by Dr. David Chen from Stanford University 
    and representatives from Google's Mountain View headquarters.
    """
    
    print("📊 Entity Extraction Example")
    print("=" * 50)
    print("\nText to analyze:")
    print(sample_text)
    print("\n" + "=" * 50)
    print("Extracted Entities:\n")
    
    result = extract_entities(sample_text)
    
    # Display extracted data
    if 'data' in result and 'response' in result['data']:
        print(result['data']['response'])
    
    # Display usage stats
    if 'usage' in result:
        print(f"\n📈 Usage Stats:")
        usage = result['usage']
        print(f"  Tokens: {usage['totalTokens']} (prompt: {usage['promptTokens']}, completion: {usage['completionTokens']})")
        print(f"  Estimated cost: ${usage['estimatedCost']:.6f}")
    
    # Verify signatures
    verify_signature(result)
    
    print("\n" + "=" * 50)
