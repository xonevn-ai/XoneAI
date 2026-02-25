"""
Batches Capabilities Example

Demonstrates batch processing using XoneAI capabilities.
"""

from xoneai.capabilities import batch_list

print("=== Batch List ===")
try:
    batches = batch_list()
    print(f"Batches found: {len(batches)}")
    for b in batches[:5]:  # Show first 5
        print(f"  - {b.get('id', 'unknown')}: {b.get('status', 'unknown')}")
except Exception as e:
    print(f"Note: {e}")
    print("Batch operations require batch jobs to be created first.")

print("\n=== Batch Operations ===")
print("Available functions:")
print("  batch_create(input_file_id, endpoint, completion_window='24h')")
print("  batch_list()")
print("  batch_retrieve(batch_id)")
print("  batch_cancel(batch_id)")

print("\nSee CLI: xoneai batches list")
print("See CLI: xoneai batches create <input_file_id>")
