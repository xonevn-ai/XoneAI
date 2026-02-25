#!/usr/bin/env python3
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
# Add the xoneai-agents directory to the path  
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'xoneai-agents'))

print("Testing import functionality...")

# Check if xoneai is found
try:
    import xoneai
    print(f"✓ xoneai package found at: {xoneai.__file__}")
    print(f"xoneai.__path__: {xoneai.__path__}")
    print(f"xoneai dir: {dir(xoneai)}")
except Exception as e:
    print(f"Error importing xoneai: {e}")

# Check xoneai.xoneai
try:
    import xoneai.xoneai
    print(f"✓ xoneai.xoneai package found at: {xoneai.xoneai.__file__}")
    print(f"xoneai.xoneai dir: {dir(xoneai.xoneai)}")
    if hasattr(xoneai.xoneai, '__all__'):
        print(f"xoneai.xoneai.__all__: {xoneai.xoneai.__all__}")
    
    # Check what we can actually import
    print("\nTesting actual imports from xoneai.xoneai:")
    for symbol in ['XoneAI', '__version__', 'Agent', 'Task', 'XoneAIAgents']:
        if hasattr(xoneai.xoneai, symbol):
            print(f"✓ {symbol} is available")
        else:
            print(f"❌ {symbol} is NOT available")
            
except Exception as e:
    print(f"Error importing xoneai.xoneai: {e}")

# Test direct import
try:
    from xoneai.xoneai import XoneAI, __version__
    print(f"✓ Direct import from xoneai.xoneai works: XoneAI={XoneAI}, __version__={__version__}")
except Exception as e:
    print(f"❌ Direct import from xoneai.xoneai failed: {e}")

# Test import from xoneaiagents
print("\nTesting xoneaiagents:")
try:
    import xoneaiagents
    print(f"✓ xoneaiagents is available: {xoneaiagents}")
    print(f"xoneaiagents.__all__: {xoneaiagents.__all__}")
except Exception as e:
    print(f"❌ xoneaiagents import failed: {e}")