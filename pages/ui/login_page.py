from playwright.sync_api import Locator, Page, Request, Route

from config import settings


class QABrainsLoginPage:
    def __init__(self, page: Page, config: settings.QABrainsConfig | None = None):
        self.page: Page = page
        self.config: settings.QABrainsConfig = config or settings.QABrainsConfig()
        self.email_input: Locator = page.locator('#email')
        self.password_input: Locator = page.locator('#password')
        self.submit_button: Locator = page.locator('button[type="submit"]')
        self.success_heading: Locator = page.get_by_role('heading', name=self.config.success_heading)

    def open(self):
        self.page.goto(self.config.url, wait_until='domcontentloaded')

    def has_ssl_error_page(self) -> bool:
        return self.page.get_by_text('Invalid SSL certificate').count() > 0

    def login(self, email: str, password: str):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()

    def login_as_default_user(self):
        self.login(self.config.default_email, self.config.default_password)


class ExpandTestingLoginPage:
    def __init__(self, page: Page):
        self.page: Page = page
        self.username_input: Locator = page.locator('#username')
        self.password_input: Locator = page.locator('#password')
        self.submit_button: Locator = page.locator('#submit-login')
        self.flash_message: Locator = page.locator('#flash')

    def open(self):
        self.page.goto(settings.PRACTICE_LOGIN_URL)

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.submit_button.click()

    def login_as_default_user(self):
        self.login(settings.PRACTICE_DEFAULT_USERNAME, settings.PRACTICE_DEFAULT_PASSWORD)

    def open_and_login_as_default_user(self):
        self.open()
        self.login_as_default_user()

    def route_secure_page_text(self, source_text: str, target_text: str):
        def route_handler(route: Route, _request: Request):
            response = route.fetch()
            body = response.text()
            route.fulfill(
                status=response.status,
                headers=response.headers,
                body=body.replace(source_text, target_text),
            )

        self.page.route(settings.PRACTICE_AUTHENTICATE_ROUTE_PATTERN, route_handler)
