class BaseAPI:
    def __init__(self, request):
        self.request = request

    def get(self, url, **kwargs):
        return self.request.get(url, **kwargs)

    def post(self, url, **kwargs):
        return self.request.post(url, **kwargs)
