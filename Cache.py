class Cache:
    def __init__(self):
        self.settings = Settings()
        self.handler = Handler()
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.config_path)
        self.cache_name = self.settings.config.get('default', 'cache', 'cache_name')
        self.cache_file = self.settings.config.get('default', 'cache', 'cache_file')
        self.cache_dir = self.settings.config.get('default', 'cache', 'cache_dir')
        self.cache_path = self.cache_dir + self.cache_file
        self.cache.read(self.cache_path)
        self.downloads = self.cache.items('downloads')
    def set(self, key, value):
        self.config.set('cache', key, value)
        with open(self.cache_path, 'wb') as configfile:
            self.config.write(configfile)
    def get(self, key):
        return self.config.get('cache', key)
    def has_key(self, key):
        return self.config.has_option('cache', key)
    def get_cache_name(self):
        return self.cache_name
    def get_downloads(self):
        return self.config.items('downloads')
    def get_download_count(self):
        return len(self.downloads)
    def get_download_size(self):
        return sum([int(x.split(',')[1]) for x in self.downloads])
    def load_cache(self):
        with open(self.cache_path, 'rb') as configfile:
            self.config.readfp(configfile)
    def write_cache(self):
        with open(self.cache_path, 'wb') as file:
            self.config.write(file)