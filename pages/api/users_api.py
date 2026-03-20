from pages.api.base_api import BaseAPI


class UsersAPI(BaseAPI):

    def login(self, email: str, password: str):
        return self.post(url='/notes/api/users/login',
            form={'email': email, 'password': password}
        )

    def get_profile(self, token: str):
        return self.get(
            '/notes/api/users/profile',
            headers={'x-auth-token': token},
        )
