import random

class CustomUserAgentMiddleware:
    def __init__(self, user_agents):
        self.user_agents = user_agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user_agents=crawler.settings.getlist('USER_AGENTS')
        )

    def process_request(self, request, spider):
        if self.user_agents:
            ua = random.choice(self.user_agents)
            request.headers['User-Agent'] = ua





