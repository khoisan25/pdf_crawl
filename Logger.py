class Logger:
    def __init__(self):
        self.settings = Settings()
        self.log_name = self.settings.config.get('default', 'logger', 'log_name')
        self.log_file = self.settings.config.get('default', 'logger', 'log_file')
        self.log_dir = self.settings.config.get('default', 'logger', 'log_dir')
        self.log_path = self.log_dir + self.log_file
        self.log = open(self.log_path, 'a')
    def log(self, message):
        self.log.write(message + '\n')