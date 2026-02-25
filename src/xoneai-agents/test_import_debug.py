#!/usr/bin/env python3
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
# Add the xoneai-agents directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'xoneai-agents'))

print("Testing import functionality...")

try:
    import xoneaiagents
    print("✓ xoneaiagents module is available")
    
    # Test importing specific classes
    try:
        from xoneaiagents import Agent, Task, AgentTeam
        print("✓ Successfully imported Agent, Task, AgentManager from xoneaiagents")
    except ImportError as e:
        print(f"❌ Failed to import specific classes: {e}")
        
except ImportError as e:
    print(f"❌ xoneaiagents module not available: {e}")

# Test the xoneai package
try:
    import xoneai
    print("✓ xoneai package is available")
    
    # Test importing from xoneai
    try:
        from xoneai import Agent, Task, AgentManager
        print("✓ Successfully imported Agent, Task, AgentManager from xoneai")
    except ImportError as e:
        print(f"❌ Failed to import from xoneai: {e}")
        
except ImportError as e:
    print(f"❌ xoneai package not available: {e}")

# Check what's in the xoneai package
try:
    import xoneai
    print(f"xoneai package contents: {dir(xoneai)}")
    if hasattr(xoneai, '__all__'):
        print(f"xoneai.__all__: {xoneai.__all__}")
    
    # Check what we can actually import
    print("\nTesting actual imports:")
    for symbol in ['XoneAI', '__version__', 'Agent', 'Task', 'Agents']:
        if hasattr(xoneai, symbol):
            print(f"✓ {symbol} is available")
        else:
            print(f"❌ {symbol} is NOT available")
            
except Exception as e:
    print(f"Error checking xoneai package: {e}")