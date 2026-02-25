#!/usr/bin/env python3
"""
Test script to verify Memory import works correctly
"""

import sys
import os

# Add the xoneai-agents source to Python path
sys.path.insert(0, '/home/runner/work/XoneAI/XoneAI/src/xoneai-agents')

try:
    from xoneaiagents.memory import Memory
    print('SUCCESS: Memory import works correctly')
    print('Memory class found:', Memory)
    
    # Try to create a minimal instance to ensure it doesn't fail immediately
    config = {"provider": "none"}  # Use the simplest provider
    memory = Memory(config=config)
    print('SUCCESS: Memory instance created successfully')
    
except ImportError as e:
    print('ERROR:', e)
    import traceback
    traceback.print_exc()
except Exception as e:
    print('UNEXPECTED ERROR:', e)
    import traceback
    traceback.print_exc()
