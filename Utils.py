class Utils:
    def __init__(self):
        #TODO To be added. Should handle download logging, download stats, check if already downloaded, managing continuation after intruption.
        self.handler = Handler()

    def get_random_proxy(self):
        return self.handler.get_random_proxy()

    def get_random_user_agent(self):
        return self.handler.get_random_user_agent()

    def get_proxy_dict(self):
        return self.handler.get_proxy_dict()

    def get_user_agent_dict(self):
        return self.handler.get_user_agent_dict()

    def get_random_user_agent_dict(self):
        return {'User-Agent': self.get_random_user_agent()}

    def get_random_proxy_dict(self):
        return {'http': 'http://' + self.get_random_proxy()['ip'] + ':' + self.get_random_proxy()['port']}

    def get_random_user_agent_and_proxy_dict(self):
        return {'User-Agent': self.get_random_user_agent(), 'http': 'http://' + self.get_random_proxy()['ip'] + ':' + self.get_random_proxy()['port']}
