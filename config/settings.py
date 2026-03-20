import os
from dataclasses import dataclass


PRACTICE_LOGIN_URL = 'https://practice.expandtesting.com/login'
PRACTICE_DEFAULT_USERNAME = 'practice'
PRACTICE_DEFAULT_PASSWORD = 'SuperSecretPassword!'
PRACTICE_SECURE_AREA_MESSAGE = 'You logged into a secure area!'
PRACTICE_AUTHENTICATE_ROUTE_PATTERN = '**/authenticate'

BASE_URL = 'https://practice.expandtesting.com'
USER_EMAIL = 'artem.belorukavskyi@ukr.net'
USER_PASSWORD = 'qweqwe'
USER_TOKEN = 'ca2d3596b40e4418a0d5c8bee4045dbbca11769869e64a91948a6d875b1c3330'
USER_NAME = 'artem.belorukavskyi'
USER_ID = '69bea106b070fb02951b7531'
USER_PHONE = '0680000001'
USER_COMPANY = 'Playtika'

NOTES_ID = '69c1654729cd8502964a7658'


def env(key: str, default: str) -> str:
    return os.getenv(key, default)


@dataclass(frozen=True)
class QABrainsConfig:
    url: str = env('QABRAINS_URL', 'https://practice.qabrains.com/')
    default_email: str = env('QABRAINS_DEFAULT_EMAIL', 'qa_testers@qabrains.com')
    default_password: str = env('QABRAINS_DEFAULT_PASSWORD', 'Password123')
    success_heading: str = env('QABRAINS_SUCCESS_HEADING', 'Login Successful')


@dataclass(frozen=True)
class WikipediaConfig:
    portal_url: str = 'https://www.wikipedia.org/'
    main_page_url: str = 'https://en.wikipedia.org/wiki/Main_Page'
    english_link_text: str = 'English'
    talk_link_text: str = 'Talk'
