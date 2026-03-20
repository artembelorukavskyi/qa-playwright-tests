from locust import HttpUser, task, between, constant_throughput, events
from config import settings
import logging

logger = logging.getLogger(__name__)

# RUN: locust -f tests/load/test_login.py --run-time 2m


WRONG_PASSWORDS = '123'


@events.request.add_listener
def request_handler(name, response_time, context, **kwargs):
    user_name = context.get('user', settings.USER_EMAIL)

    if name == 'Login User':
        logging.info(f'User -> {user_name} successfully login. Request time: {response_time:.2f}ms')
    elif name == 'Logout User':
        logging.info(f'User -> {user_name} logout. Request time: {response_time:.2f}ms')


class LoginUser(HttpUser):
    # wait_time = between(1, 3)
    wait_time = constant_throughput(5)
    host = settings.BASE_URL
    token = None


    @task(10)
    def login_successful(self):
        payload = {
            'email': settings.USER_EMAIL,
            'password': settings.USER_PASSWORD,
        }
        response = self.client.post(
            '/notes/api/users/login',
            data = payload,
            name = f'Login User: {settings.USER_EMAIL}',
            context = {'user': settings.USER_EMAIL},
        )
        if response.status_code == 200:
            data = response.json()
            self.token = data.get('data', {}).get('token')
        else:
            logger.error(f'Login failed: {response.status_code} - {response.text}')

    @task(1)
    def login_failed_wrong_password(self):
        payload = {
            'email': settings.USER_EMAIL,
            'password': WRONG_PASSWORDS,
        }
        with self.client.post(
            '/notes/api/users/login',
            data=payload,
            name=f'User: {settings.USER_EMAIL} login with wrong password',
            context={'user': settings.USER_EMAIL},
            catch_response=True
        ) as response:
            if response.status_code in (400, 401):
                response.success()
            else:
                response.failure(f'Expected status_code 400 or 401, got {response.status_code}: {response.text}')


    def on_start(self):
        payload = {
            'email': settings.USER_EMAIL,
            'password': settings.USER_PASSWORD,
        }
        response = self.client.post(
            '/notes/api/users/login',
            data=payload,
            name=f'Login User: {settings.USER_EMAIL}',
            context={'user': settings.USER_EMAIL},
        )
        if response.status_code == 200:
            data = response.json()
            self.token = data.get('data', {}).get('token')

    def on_stop(self):
        if self.token:
            self.client.delete(
                '/notes/api/users/logout',
                headers={'x-auth-token': self.token},
                name=f'Login User: {settings.USER_EMAIL}',
                context = {'user': settings.USER_EMAIL},
            )
