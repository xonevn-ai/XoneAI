#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src/xoneai-agents')

import warnings
warnings.simplefilter('always')  # Enable all warnings

print("Testing import with all warnings enabled...")
print("Importing xoneaiagents...")

try:
    import xoneaiagents
    print("✅ Import successful!")
    
    print("Testing Agent creation...")
    agent = xoneaiagents.Agent(instructions="Test agent", llm="gpt-4o-mini")
    print("✅ Agent created successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()