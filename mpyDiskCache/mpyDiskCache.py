from sys import platform
if platform == 'linux':
    import json
else:
    import ujson as json
import os

DEBUG = False

class mpyDiskCache:
    def __init__(self, directory, max_size=50, debug=DEBUG):
        self.directory = directory.rstrip('/')  # Remove trailing slash
        self.max_size = max_size
        self.ages_file = f'{self.directory}/ages.json'
        self.DEBUG = debug

        # Create the directory if it doesn't exist
        try:
            if not self._dir_exists(self.directory):
                os.mkdir(self.directory)
        except OSError as e:
            print(f"Error creating directory: {e}")
            raise

        self.ages = self._load_ages()

    def _dir_exists(self, path):
        # Check if a directory exists
        try:
            return os.listdir(path) is not None
        except OSError:
            return False

    def debug_print(self, *args, **kwargs):
        if self.DEBUG:
            print(*args, **kwargs)

    def _load_ages(self):
        try:
            if self._file_exists(self.ages_file):
                with open(self.ages_file, 'r') as f:
                    data = f.read().strip()
                    if data:
                        return json.loads(data)
            return []
        except OSError:
            return []

    def _save_ages(self):
        try:
            with open(self.ages_file, 'w') as f:
                json.dump(self.ages, f)
        except OSError:
            pass

    def _get_file_path(self, key):
        return f'{self.directory}/{key}.json'  # Manually construct path

    def _clean_up(self):
        while len(self.ages) > self.max_size:
            oldest_key = self.ages.pop(0)
            os.remove(self._get_file_path(oldest_key))
        self._save_ages()

    def _file_exists(self, filepath):
        # Check if a file exists in a directory
        try:
            with open(filepath, 'r'):
                return True
        except OSError:
            return False

    def set(self, key, value):
        try:
            file_path = self._get_file_path(key)
            # self.debug_print(f'Setting {key}:{value} in {file_path}')
            with open(file_path, 'w') as f:
                json.dump(value, f)
            if key not in self.ages:
                self.ages.append(key)
            self._clean_up()
        except BaseException as e:
            print(e)

    def get(self, key):
        try:
            file_path = self._get_file_path(key)
            # self.debug_print(f'Getting {key} from {file_path}')
            if self._file_exists(file_path):
                with open(file_path, 'r') as f:
                    return json.load(f)
        except BaseException as e:
            print(e)
        return None

    def delete(self, key):
        try:
            file_path = self._get_file_path(key)
            # self.debug_print(f'Deleting {key} from {file_path}')
            if self._file_exists(file_path):
                os.remove(file_path)
            if key in self.ages:
                self.ages.remove(key)
            self._save_ages()
        except BaseException as e:
            print(e)
