"""
Vector Stores Capabilities Example

Demonstrates vector store management using XoneAI capabilities.
"""

from xoneai.capabilities import vector_store_create, vector_store_search

print("=== Vector Store Operations ===")
print("Available functions:")
print("  vector_store_create(name)")
print("  vector_store_search(vector_store_id, query)")

print("\n=== Create Vector Store ===")
try:
    store = vector_store_create(name="test-store")
    print(f"Created: {store}")
except Exception as e:
    print(f"Note: {e}")

print("\nSee CLI: xoneai vector-stores create --name 'my-store'")
print("See CLI: xoneai vector-stores search <store_id> <query>")
