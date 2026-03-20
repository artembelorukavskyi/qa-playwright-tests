import requests
import pytest

BASE_URL = 'https://demoqa.com/'

@pytest.mark.api
def test_open_test_site():
    response = requests.get(f'{BASE_URL}/posts')
    assert response.status_code == 200