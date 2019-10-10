
import os

class NoSuchKeyException(Exception):
	def __init__(self, key):
		super().__init__('No such key [%s] in this config file' % key)

class ConfigFile (object):
	def __init__(self, path):
		self._path = None
		self._data = {}
		self._lines = []
		self._set_path(path)
		if os.path.exists(self._path):
			self.load()
		
	def get(self, key):
		if key in self._data:
			return self._data[key]
		raise NoSuchKeyException(key)
		
	def set(self, key, val):
		self._data[key] = val
		
	def delete_key(self, key):
		if key in self._data:
			del self._data[key]
		else:
			raise NoSuchKeyException(key)
			
	def key_exists(self, key):
		return key in self._data

	def load(self, path=None):
		if path:
			self._set_path(path)
		with open(self._path) as f:
			self._lines = f.read().split('\n')
		lines = list(filter(lambda l:'=' in l and not l.startswith('#'), self._lines))
		self._data = {}
		for line in lines:
			parts = line.split('=')
			key = parts[0]
			val = '='.join(parts[1:])
			self._data[key] = val
			
	def save(self):
		keys = list(self._data.keys())
		out = []
		for line in self._lines:
			if '=' in line and not line.startswith('#'):
				parts = line.split('=')
				key = parts[0]
				if key in keys:
					out += ['%s=%s' % (key, self._data[key])]
					keys.remove(key)
			else:
				out += [line]
		for key in keys:
			out += ['%s=%s' % (key, self._data[key])]
		self._lines = out
		with open(self._path, 'w') as f:
			f.write('\n'.join(out))
			
	def _set_path(self, path):
		self._path = os.path.abspath(path)
