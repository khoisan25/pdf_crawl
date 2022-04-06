import logging

class Logger:
    def __init__(self, name):
        self.settings = Settings()
        self.log_name = self.settings.config.get('default', 'logger', 'log_name')
        self.log_file = self.name +"-"+ self.settings.config.get('default', 'logger', 'log_file')
        self.log_dir = self.settings.config.get('default', 'logger', 'log_dir')
        self.log_level = self.settings.config.get('default', 'logger', 'log_level')
        self.log_path = self.log_dir + self.log_file
        self.log = logging.getLogger(self.log_name)
        self.log.setLevel(self.log_level)
        self.log_handler = logging.FileHandler(self.log_path)
        self.log_handler.setLevel(self.log_level)
        self.log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.log_handler.setFormatter(self.log_formatter)
        self.log.addHandler(self.log_handler)
        self.log.info('Logger initialized.')

    def log(self, message):
        self.log.info(message)

    def close(self):
        self.log.info('Logger closed.')
        self.log.removeHandler(self.log_handler)
        self.log_handler.close()

    def __del__(self):
        self.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()