import os

class Environment:
    DEV = "dev"
    PROD = "prod"

    URLS = {
        DEV: "https://playground.learnqa.ru/api_dev",
        PROD: "https://playground.learnqa.ru/api"
    }

    # def __init__(self):
    #     try:
    #         self.env = os.environ['ENV']
    #     except KeyError:
    #         self.env = self.DEV

    @property
    def env(self):
        return os.environ.get('ENV', self.PROD)

    def get_base_url(self):
        if self.env in self.URLS:
            return self.URLS[self.env]
        else:
            raise Exception(f"Environment variable {self.env} is not defined")

ENV_OBJECT = Environment()