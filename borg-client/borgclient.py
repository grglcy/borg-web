import requests


class BorgClient(object):
    def __init__(self, url: str, username: str, password: str):
        self.url = url
        self.client = requests.Session()
        self.referer = self.url
        self.username = username
        self.password = password

        self.__login()

    def __login(self):
        url = f"{self.url}/accounts/login/"

        post_data = {
            "username": self.username,
            "password": self.password,
        }
        return self.__post(url, post_data).text

    def __post(self, url, post_data):
        self.client.get(url=url)
        csrf_token = self.client.cookies['csrftoken']

        post_data['csrfmiddlewaretoken'] = csrf_token

        headers = dict(self.client.headers)
        headers['X-CSRFToken'] = csrf_token
        headers['Referer'] = self.referer

        post_responce = self.client.post(url=url, data=post_data, headers=headers)
        return post_responce

    def post_error(self, post_data):
        url = f"{self.url}/post/error"

        return self.__post(url, post_data).text

    def post_repo(self, post_data):
        url = f"{self.url}/post/repo"

        return self.__post(url, post_data).text

    def post_archive_and_cache(self, post_data):
        url = f"{self.url}/post/archive"

        return self.__post(url, post_data).text
