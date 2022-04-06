import logging

class Handler:
    def __init__(self):
        self.settings = Settings()
        self.logger = Logger('Handler')
        self.config = ConfigParser.ConfigParser()
        self.cache_file = self.settings.config.get('default', 'handler', 'cache_file')
        self.cache_dir = self.settings.config.get('default', 'handler', 'cache_dir')
        self.cache_path = self.cache_dir + self.cache_file
        self.cache.read(self.cache_path)
        self.download_count = 0
        self.download_size = 0

    def record_download(self, url, file_name, file_size):
        self.download_count += 1
        self.download_size += file_size
        '''TODO Update to dir check. No need to store in memory.'''
        self.cache.set('downloads', url, file_name + ',' + file_size)
        with open(self.cache_path, 'wb') as configfile:
            self.cache.write(configfile)
        self.logger.log('Downloaded ' + url + ' and saved to ' + file_name)

    def get_download_count(self):
        return self.download_count
    def get_download_size(self):
        return self.download_size
    def get_urls(self):
        return self.cache.items('urls')
    def get_downloads(self):
        return self.cache.items('downloads')
    def has_file_been_downloaded(self, url):
        return self.cache.has_option('downloads', url)
    def get_file_name(self, url):
        return self.cache.get('downloads', url).split(',')[0]
    def get_file_size(self, url):
        return self.cache.get('downloads', url).split(',')[1]
    def get_file_path(self, url):
        return self.cache.get('urls', url)
    def record_url(self, url, file_path):
        self.cache.set('urls', url, file_path)
        with open(self.cache_path, 'wb') as configfile:
            self.cache.write(configfile)
        self.logger.log('Crawled ' + url + ' and saved to ' + file_path)