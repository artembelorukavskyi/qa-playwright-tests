import pytest
from config import settings


@pytest.mark.api
def test_login(users_api):
    response = users_api.login(settings.USER_EMAIL, settings.USER_PASSWORD)

    login_data = response.json()
    assert login_data.get('success') is True
    assert login_data.get('status') == 200
    assert login_data.get('message') == 'Login successful'


@pytest.mark.api
def test_login_fail_wrong_password(users_api):
    response = users_api.login(settings.USER_EMAIL, 'WrongPassword123')
    assert response.status in (400, 401)

    login_data = response.json()
    assert login_data.get('success') is False


@pytest.mark.api
def test_get_user_profile(users_api, auth_token):
    response = users_api.get_profile(auth_token)
    assert response.status == 200

    response_data = response.json()
    assert response_data.get('success') is True

    data = response_data.get('data')
    assert data['id'] is not None
    assert data['name'] == settings.USER_NAME
    assert data['email'] == settings.USER_EMAIL
    assert data['phone'] == settings.USER_PHONE
    assert data['company'] == settings.USER_COMPANY


@pytest.mark.api
def test_get_user_profile_invalid_token(users_api):
    response = users_api.get_profile('test-token')
    assert response.status == 401


@pytest.mark.api
def test_create_note(notes_api, auth_token):
    payload = {
        'title': 'New Book',
        'description': 'This is a new book',
        'category': 'Home'
    }
    response = notes_api.create_note(auth_token, payload)
    assert response.status == 200

    response_data = response.json()
    assert response_data['message'] == 'Note successfully created'

    data = response_data.get('data')
    assert data['id'] is not None
    assert data['title'] == 'New Book'
    assert data['description'] == 'This is a new book'
    assert data['category'] == 'Home'
    assert data['user_id'] == settings.USER_ID


@pytest.mark.api
def test_get_all_notes(notes_api, auth_token):
    response = notes_api.get_all(auth_token)
    assert response.status == 200

    response_data = response.json()
    all_notes = response_data.get('data')
    assert all_notes is not None
    assert len(all_notes) > 0

    first_note = all_notes[0]
    assert first_note['title'] == 'New Book'
    assert first_note['description'] == 'This is a new book'
    assert first_note['category'] == 'Home'
    assert first_note['user_id'] == settings.USER_ID


@pytest.mark.api
def test_get_notes_by_id(notes_api, auth_token):
    response = notes_api.get_by_id(auth_token, settings.NOTES_ID)
    assert response.status == 200

    response_data = response.json()
    assert response_data['status'] == 200
    assert response_data['message'] == 'Note successfully retrieved'

    data = response_data.get('data')
    assert data['id'] is not None
    assert data['title'] == 'New Note'
    assert data['description'] == 'This is a new Notes'
    assert data['category'] == 'Home'
    assert data['user_id'] == settings.USER_ID


@pytest.mark.api
def test_get_notes_by_wrong_id(notes_api, auth_token):
    response = notes_api.get_by_id(auth_token, '123456789')
    assert response.status == 400
