#!/usr/bin/env python3
"""
Test suite for LumenAI CLI and SDK
"""
import sys
import json
from pathlib import Path
from lumen_sdk import LumenClient


def load_client():
    """Load client from saved config"""
    config_file = Path.home() / ".lumen" / "config.json"
    if not config_file.exists():
        print("❌ Not logged in. Run: python lumen_cli.py login")
        sys.exit(1)
    
    config = json.load(open(config_file))
    return LumenClient(config['token'])


def test_basic_query():
    """Test basic query"""
    print("🧪 Testing basic query...")
    client = load_client()
    result = client.query("Say 'test successful'", model="gpt-5-nano")
    
    if 'data' in result and 'response' in result['data']:
        print("✅ Basic query works")
        return True
    else:
        print("❌ Basic query failed")
        return False


def test_streaming():
    """Test streaming"""
    print("\n🧪 Testing streaming...")
    client = load_client()
    chunks = []
    
    for chunk in client.stream("Count to 3", model="gpt-5-nano"):
        chunks.append(chunk)
    
    if len(chunks) > 0:
        print(f"✅ Streaming works ({len(chunks)} chunks received)")
        return True
    else:
        print("❌ Streaming failed")
        return False


def test_get_keys():
    """Test public keys retrieval"""
    print("\n🧪 Testing public keys...")
    client = load_client()
    keys = client.get_keys()
    
    if 'ecdsa' in keys and 'pq' in keys:
        print("✅ Public keys retrieved")
        print(f"  - ECDSA key length: {len(keys['ecdsa']['publicKey'])}")
        print(f"  - PQ key length: {len(keys['pq']['publicKey'])}")
        return True
    else:
        print("❌ Failed to get public keys")
        return False


def test_usage_stats():
    """Test usage stats in response"""
    print("\n🧪 Testing usage stats...")
    client = load_client()
    result = client.query("Hi", model="gpt-5-nano")
    
    if 'usage' in result and 'userStats' in result:
        usage = result['usage']
        stats = result['userStats']
        print("✅ Usage stats available")
        print(f"  - Tokens used: {usage['totalTokens']}")
        print(f"  - Today's requests: {stats['todayRequests']}")
        print(f"  - Today's cost: ${stats['todayCost']:.6f}")
        return True
    else:
        print("❌ Usage stats not available")
        return False


def test_different_models():
    """Test if we can query different models"""
    print("\n🧪 Testing model availability...")
    client = load_client()
    
    # Test gpt-5-nano (should work on free tier)
    try:
        result = client.query("Hi", model="gpt-5-nano")
        print("✅ gpt-5-nano: Available")
        nano_works = True
    except Exception as e:
        print(f"❌ gpt-5-nano: {e}")
        nano_works = False
    
    return nano_works


def run_all_tests():
    """Run all tests"""
    print("="*50)
    print("LumenAI SDK Test Suite")
    print("="*50)
    
    tests = [
        test_basic_query,
        test_streaming,
        test_get_keys,
        test_usage_stats,
        test_different_models
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            results.append(False)
    
    print("\n" + "="*50)
    print(f"Results: {sum(results)}/{len(results)} tests passed")
    print("="*50)
    
    if all(results):
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
