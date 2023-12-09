
# mpyDiskCache

`mpyDiskCache` is a simple, file-based caching system for MicroPython environments. It is designed to be lightweight and easy to use, providing a way to store and retrieve Python objects to and from the filesystem.

## Features

- Simple key-value storage mechanism.
- Stores data in JSON format.
- Configurable cache size with automatic oldest-item eviction.
- Debug mode for easy troubleshooting.
- Pure python so it should work linux and windows too.

## Installation
`mpremote mip install github:ShyftXero/mpyDiskCache`

OR

Copy the `mpyDiskCache.py` file into your MicroPython project directory.

## Usage

```python
from mpyDiskCache import mpyDiskCache

# Create a cache instance
cache = mpyDiskCache('path_to_cache_directory')

# Set a value in the cache
cache.set('key1', 'value1')

# Get a value from the cache
value = cache.get('key1')
print(value)

# Delete a value from the cache
cache.delete('key1')
```

## API

- `mpyDiskCache(directory, max_size=50, debug=False)`: Creates a new cache instance.
- `set(key, value)`: Stores a value under the specified key.
- `get(key)`: Retrieves the value associated with the specified key.
- `delete(key)`: Removes the value associated with the specified key from the cache.

## Debugging

Enable debugging to get console output for operations performed by the cache:

```python
cache = mpyDiskCache('path_to_cache_directory', debug=True)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
