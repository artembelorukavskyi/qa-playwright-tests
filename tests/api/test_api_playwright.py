import pytest

from config import settings


@pytest.mark.api
def test_login(users_api):
    response = users_api.login(settings.USER_EMAIL, settings.USER_PASSWORD)
    assert response.status == 200

    data = response.json()
    token = data['data']['token']
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0


@pytest.mark.api
def test_get_user_profile(users_api, auth_token):
    response = users_api.get_profile(auth_token)
    assert response.status == 200

    data = response.json()['data']
    assert data['name'] == settings.USER_NAME
    assert data['email'] == settings.USER_EMAIL
    assert data['phone'] == settings.USER_PHONE
    assert data['company'] == settings.USER_COMPANY


@pytest.mark.api
def test_get_user_profile_fail(users_api):
    response = users_api.get_profile('wrong-token')
    assert response.status == 401


@pytest.mark.api
def test_create_note(auth_token, notes_api, note_payload):
    response = notes_api.create_note(auth_token, note_payload)
    assert response.status == 200

    data = response.json()['data']
    assert data['title'] == note_payload['title']
    assert data['user_id'] == settings.USER_ID
    assert data['description'] == note_payload['description']
    assert data['category'] == note_payload['category']


@pytest.mark.api
def test_get_all_notes(notes_api, auth_token, note_payload):
    response = notes_api.get_all(auth_token)
    assert response.status == 200

    response_data = response.json()['data']
    assert len(response_data) > 0

    first_note = response_data[0]
    assert first_note['title'] == note_payload['title']
    assert first_note['description'] == note_payload['description']
    assert first_note['category'] == note_payload['category']


@pytest.mark.api
def test_get_note_by_id(notes_api, auth_token, note_payload):
    response = notes_api.get_by_id(auth_token, settings.NOTES_ID)
    assert response.status == 200

    data = response.json()['data']
    assert data['id'] == settings.NOTES_ID
    assert data['title'] == note_payload['title']
    assert data['description'] == note_payload['description']
    assert data['category'] == note_payload['category']


@pytest.mark.api
def test_get_notes_by_wrong_id(auth_token, notes_api):
    invalid_id = "123456789"
    response = notes_api.get_by_id(auth_token, invalid_id)
    assert response.status == 400
