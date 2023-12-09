def test_micro_py_cache():
    import os
    from mpyDiskCache.mpyDiskCache import mpyDiskCache

    # Setup test environment
    test_dir = 'test_cache_dir'
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    print("Initializing cache...")
    cache = mpyDiskCache(test_dir, max_size=3)

    # Test set and get
    print("Testing set and get...")
    cache.set('key1', 'value1')
    assert cache.get('key1') == 'value1', "Set or Get failed"
    print("Set and Get test passed.")

    # Test cache limit
    print("Testing cache size limit...")
    cache.set('key2', 'value2')
    cache.set('key3', 'value3')
    cache.set('key4', 'value4')
    assert cache.get('key1') is None, "Cache max_size constraint failed"
    print("Cache size limit test passed.")

    # Test delete
    print("Testing delete functionality...")
    cache.delete('key2')
    assert cache.get('key2') is None, "Delete failed"
    print("Delete test passed.")

    # Test thread safety and concurrency
    print("Testing thread safety and concurrency...")
    import _thread
    import time
    def cache_write_thread(key, value):
        cache.set(key, value)

    _thread.start_new_thread(cache_write_thread, ('thread_key1', 'thread_val1'))
    _thread.start_new_thread(cache_write_thread, ('thread_key2', 'thread_val2'))

    # Allow some time for threads to execute
    time.sleep(1)

    assert cache.get('thread_key1') == 'thread_val1', "Thread safety failed on write"
    assert cache.get('thread_key2') == 'thread_val2', "Thread safety failed on write"
    print("Thread safety and concurrency test passed.")

    # Test set and get with various data structures
    print("Testing set and get with various data structures...")
    nested_dict = {'a': 1, 'b': {'c': 2, 'd': 3}}
    test_list = [1, 2, 3, 4, 5]
    test_tuple = (1, 2, 3, 4, 5)

    cache.set('nested_dict', nested_dict)
    cache.set('test_list', test_list)
    cache.set('test_tuple', test_tuple)

    assert cache.get('nested_dict') == nested_dict, "Nested dict failed"
    assert cache.get('test_list') == test_list, "List failed"
    assert cache.get('test_tuple') == list(test_tuple), "Tuple failed"  # Tuples are converted to lists
    print("Set and Get with various data structures test passed.")

    # Clean up
    print("Cleaning up...")
    for file in os.listdir(test_dir):
        os.remove(os.path.join(test_dir, file))
    os.rmdir(test_dir)

    print("All tests passed!")

# Run the test suite
test_micro_py_cache()
