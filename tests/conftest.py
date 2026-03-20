import os
from typing import Generator

import allure
import pytest
from playwright.sync_api import Playwright, APIRequestContext

from pages.api.notes_api import NotesAPI
from pages.api.users_api import UsersAPI
from config import settings

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLURE_RESULTS_DIR = os.path.join(ROOT_DIR, 'allure-results')
SCREENSHOTS_DIR = os.path.join(ALLURE_RESULTS_DIR, 'screenshots')
JSON_RESULTS_DIR = os.path.join(ALLURE_RESULTS_DIR, 'json')


def pytest_configure(config):
    if hasattr(config, 'option') and hasattr(config.option, 'allure_report_dir'):
        config.option.allure_report_dir = JSON_RESULTS_DIR


@pytest.fixture(scope='function', autouse=True)
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        'record_video_dir': os.path.join(ALLURE_RESULTS_DIR, 'videos'),
    }


def pytest_itemcollected(item):
    raw_name = item.name.split('[')[0]
    pretty_name = raw_name.replace('test_', '').replace('_', ' ').capitalize()
    item.user_properties.append(('allure_title', pretty_name))

    if hasattr(item, 'function'):
        item.function.__doc__ = pretty_name


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    for prop in item.user_properties:
        if prop[0] == 'allure_title':
            allure.dynamic.title(prop[1])

    if report.when == 'call':
        page = item.funcargs.get('page')
        if page:
            try:
                video_path = None
                if page.video:
                    video_path = page.video.path()

                if report.failed:
                    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

                    clean_name = item.name.replace("[", "_").replace("]", "_")
                    screenshot_path = os.path.join(SCREENSHOTS_DIR, f'{clean_name}.png')

                    page.screenshot(path=screenshot_path, full_page=True)

                    allure.attach.file(
                        screenshot_path,
                        name='failure_screenshot',
                        attachment_type=allure.attachment_type.PNG
                    )

                    page.context.close()

                    if video_path and os.path.exists(video_path):
                        allure.attach.file(
                            video_path,
                            name='failure_video',
                            attachment_type=allure.attachment_type.WEBM
                        )
                else:
                    page.context.close()
                    if video_path and os.path.exists(video_path):
                        try:
                            os.remove(video_path)
                        except OSError:
                            pass

            except Exception as e:
                print(f"\n[Post-test cleanup error]: {e}")


@pytest.fixture(scope='session')
def api_request_context(playwright: Playwright) -> Generator[APIRequestContext, None, None]:
    context = playwright.request.new_context(base_url=settings.BASE_URL)
    yield context
    context.dispose()


@pytest.fixture(scope='session')
def users_api(api_request_context: APIRequestContext) -> UsersAPI:
    return UsersAPI(api_request_context)


@pytest.fixture(scope='session')
def notes_api(api_request_context: APIRequestContext) -> NotesAPI:
    return NotesAPI(api_request_context)


@pytest.fixture(scope='session')
def auth_token(users_api: UsersAPI) -> str:
    response = users_api.login(settings.USER_EMAIL, settings.USER_PASSWORD)
    payload = response.json()
    return payload['data']['token']


@pytest.fixture
def note_payload() -> dict:
    return {
        'title': 'New Note',
        'description': 'This is a new Notes',
        'category': 'Home'
    }
