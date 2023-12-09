from sys import platform
if platform == 'linux':
    import json
else:
    import ujson as json
import os
# import _thread

DEBUG = True

class mpyDiskCache:
    def __init__(self, directory, max_size=50,debug=DEBUG):
        self.directory = directory
        self.max_size = max_size
        self.ages_file = os.path.join(self.directory, 'ages.json')
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except OSError:
                pass
        self.ages = self._load_ages()
        self.DEBUG = debug
    
    def debug_print(self,*args,**kwargs):
        if self.DEBUG == True:
            print(*args, **kwargs)
    
    def _load_ages(self):
        if os.path.exists(self.ages_file):
            try:
                with open(self.ages_file, 'r') as f:
                    data = f.read().strip()
                    if data:  # Check if the file is not empty
                        return json.loads(data)
                    else:
                        return []
            except OSError:
                pass
        return []

    def _save_ages(self):
        try:
            with open(self.ages_file, 'w') as f:
                json.dump(self.ages, f)
        except OSError:
            pass

    def _get_file_path(self, key):
        return os.path.join(self.directory, '{}.json'.format(key))

    def _clean_up(self):
        while len(self.ages) > self.max_size:
            oldest_key = self.ages.pop(0)
            os.remove(self._get_file_path(oldest_key))
        self._save_ages()

    def set(self, key, value):
        try:
            file_path = self._get_file_path(key)
            self.debug_print(f'Setting {key}:{value} in {file_path}')
            with open(file_path, 'w') as f:
                json.dump(value, f)
            if key not in self.ages:
                self.ages.append(key)
            self._clean_up()
        except OSError:
            pass

    def get(self, key):
        try:
            file_path = self._get_file_path(key)
            self.debug_print(f'Setting {key} from {file_path}')
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    return json.load(f)
        except OSError:
            pass
        return None

    def delete(self, key):
        try:
            file_path = self._get_file_path(key)
            self.debug_print(f'Deleting {key} from {file_path}')
            if os.path.exists(file_path):
                os.remove(file_path)
            if key in self.ages:
                self.ages.remove(key)
            self._save_ages()
        except OSError:
            pass

# Usage Example
# cache = mpyDiskCache('path_to_cache_directory')
# cache.set('key1', 'value1')
# debug_print(cache.get('key1'))
