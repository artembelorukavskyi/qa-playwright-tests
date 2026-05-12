import pytest
from playwright.sync_api import Playwright, APIRequestContext

from config import settings


@pytest.fixture(scope='session')
def api_request_context(playwright: Playwright) -> APIRequestContext:
    headers = {
        'x-auth-token': settings.USER_TOKEN
    }

    request_context = playwright.request.new_context(
        base_url=settings.BASE_URL,
        extra_http_headers=headers,
    )

    yield request_context
    request_context.dispose()


@pytest.fixture(scope='session')
def wrong_api_request(playwright: Playwright) -> APIRequestContext:
    context = playwright.request.new_context(
        base_url=settings.BASE_URL
    )

    yield context
    context.dispose()


def test_login(api_request_context):
    payload = {
        'email': settings.USER_EMAIL,
        'password': settings.USER_PASSWORD,
    }

    response = api_request_context.post(
        url=f'{settings.BASE_URL}/users/login',
        form=payload,
    )

    login_data = response.json()

    assert response.status == 200, response.text()
    assert login_data.get('success') is True
    assert login_data.get('status') == 200
    assert login_data.get('message') == 'Login successful'
    assert login_data.get('data')['token'] == settings.USER_TOKEN


def test_get_user_profile(api_request_context):
    response = api_request_context.get(
        url=f'{settings.BASE_URL}/users/profile',
        headers={'x-auth-token': settings.USER_TOKEN},
    )

    assert response.status == 200, response.text()

    response_data = response.json()
    assert response_data.get('success') is True

    data = response_data.get('data')

    assert data['id'] is not None
    assert data['name'] == settings.USER_NAME
    assert data['email'] == settings.USER_EMAIL
    assert data['phone'] == settings.USER_PHONE
    assert data['company'] == settings.USER_COMPANY


def test_get_user_profile_fail(wrong_api_request):
    response = wrong_api_request.get(
        url=f'{settings.BASE_URL}/users/profile',
        headers={'x-auth-token': 'test-token'},
    )

    assert response.status == 401


def test_create_note(api_request_context):
    payload = {
        'title': 'New Book',
        'description': 'This is a new book',
        'category': 'Home',
    }

    response = api_request_context.post(
        url=f'{settings.NOTES_URL}',
        data=payload,
        headers={'x-auth-token': settings.USER_TOKEN},
    )

    assert response.status == 200, response.text()

    response_data = response.json()
    assert response_data['message'] == 'Note successfully created'

    data = response_data.get('data')

    assert data['id'] is not None
    assert data['title'] == 'New Book'
    assert data['description'] == 'This is a new book'
    assert data['category'] == 'Home'
    assert data['user_id'] == settings.USER_ID


def test_get_all_notes(api_request_context):
    response = api_request_context.get(
        url=f'{settings.NOTES_URL}',
        headers={'x-auth-token': settings.USER_TOKEN},
    )

    assert response.status == 200, response.text()

    response_data = response.json()
    all_notes = response_data.get('data')

    assert all_notes is not None
    assert len(all_notes) > 0

    first_note = all_notes[0]

    assert first_note['title'] == 'New Book'
    assert first_note['description'] == 'This is a new book'
    assert first_note['category'] == 'Home'
    assert first_note['user_id'] == settings.USER_ID


def test_get_notes_by_id(api_request_context):
    response = api_request_context.get(
        url=f'{settings.NOTES_URL}/{settings.NOTES_ID}',
        headers={'x-auth-token': settings.USER_TOKEN},
    )

    assert response.status == 200, response.text()

    response_data = response.json()

    assert response_data['status'] == 200
    assert response_data['message'] == 'Note successfully retrieved'

    data = response_data.get('data')

    assert data['id'] is not None
    assert data['title'] == 'New Book'
    assert data['description'] == 'This is a new book'
    assert data['category'] == 'Home'
    assert data['user_id'] == settings.USER_ID


def test_get_notes_by_wrong_id(wrong_api_request):
    response = wrong_api_request.get(
        url=f'{settings.NOTES_URL}/123456789',
        headers={'x-auth-token': settings.USER_TOKEN},
    )

    assert response.status == 400
