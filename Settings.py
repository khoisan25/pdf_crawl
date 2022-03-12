import configparser

class Settings:
    def __init__(self):
        self.utils = Utils()
        self.config = configparser.ConfigParser()
        self.config.read('settings.ini')
        self.crawler_depth = self.config.get('default', 'crawler', 'depth')
        self.crawler_method = self.config.get('default', 'crawler', 'method')
        self.crawler_threads = self.config.get('default', 'crawler', 'threads')
        self.crawler_timeout = self.config.get('default', 'crawler', 'timeout')
        self.crawler_user_agent = self.config.get('default', 'crawler', 'user_agent')
        self.crawler_proxy = self.config.get('default', 'crawler', 'proxy')
        self.crawler_max_download_size = self.config.get('default', 'crawler', 'max_download_size')
        self.crawler_file_extension = self.config.get('default', 'crawler', 'file_extension')
        self.crawler_config_name = self.config.get('default', 'crawler', 'config_name')
        self.config_name = self.settings.config.get('default', 'handler', 'config_name')
        self.output_dir = self.settings.config.get('default', 'handler', 'output_dir')
        self.log_file = self.settings.config.get('default', 'handler', 'log_file')