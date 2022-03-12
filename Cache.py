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
    def set(self, key, value):
        self.config.set('cache', key, value)
        with open(self.cache_path, 'wb') as configfile:
            self.config.write(configfile)
    def get(self, key):
        return self.config.get('cache', key)
    def has_key(self, key):
        return self.config.has_option('cache', key)