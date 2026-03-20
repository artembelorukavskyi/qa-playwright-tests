# AGENTS.md

Guidance for AI coding agents working on the QA Playwright Tests project.

## Project Overview

**Type**: Python-based test automation framework combining UI and API testing with load testing capabilities.

**Stack**: Playwright (UI), Pytest, Requests (API), Locust (load testing), Allure (reporting), Docker, Jenkins

**Key Locations**:
- UI tests: `tests/ui/` (marked with `@pytest.mark.ui`)
- API tests: `tests/api/` (marked with `@pytest.mark.api`)
- Load tests: `tests/load/` (Locust-based, excluded from regular pytest runs via `norecursedirs`)
- Pages (POM): `pages/` — `WikipediaPage`, `QABrainsLoginPage`, `ExpandTestingLoginPage`, `AlloTVPage`
- API clients: `api/` - BaseAPI and specialized API classes (`UsersAPI`, `NotesAPI`)
- Configuration: `config/settings.py` - centralized settings with dataclasses and module-level constants

## Architecture Patterns

### Page Object Model (POM)
All UI elements are encapsulated in page classes in `pages/`. Each page class:
- Takes a `page: Page` object (Playwright) in `__init__`
- Optionally accepts a config dataclass (e.g., `WikipediaConfig`, `QABrainsConfig`)
- Stores element locators as class attributes (e.g., `self.email_input: Locator`)
- Provides high-level action methods (e.g., `login()`, `navigate()`)

Example: `ExpandTestingLoginPage` in `pages/login_page.py`

Pages that target external sites without a config dataclass (e.g., `AlloTVPage` in `pages/allo_tv_page.py`) use `page: Page` only and hard-code the URL in `navigate()`. Use `locator.is_visible()` for conditional actions (e.g., dismissing promo modals before interacting).

**Network interception**: `ExpandTestingLoginPage.route_secure_page_text()` demonstrates using `page.route()` to intercept responses and modify the body before the page receives it. Use this pattern when you need to stub or mutate server responses in UI tests.

### API Testing Pattern
API clients inherit from `BaseAPI` and use Playwright's `APIRequestContext`:
- `BaseAPI` provides wrapper methods (`get()`, `post()`)
- Subclasses (e.g., `UsersAPI`, `NotesAPI`) define endpoint-specific methods
- Fixtures in `conftest.py` inject `APIRequestContext` instances with preconfigured base URLs and headers
- Authentication via token headers: `headers={'x-auth-token': token}`

**Dual-context fixture pattern** (important distinction):
- `api_login_request_context` (session) → `users_login_api`: sets `content-type: application/x-www-form-urlencoded` at context level; used for form-based login flows
- `api_request_context` (session) → `users_api`, `notes_api`: no preset auth headers; auth token is passed **per-request** via `headers={'x-auth-token': token}`

`tests/api/new.py` is a scratch/exploration file with inline fixtures. It is **not collected** by pytest (filename does not match `python_files = test_*.py`) and should not be used as a template.

### Configuration Management
All configuration uses frozen dataclasses in `config/settings.py`:
- Constants for test data and URLs
- `QABrainsConfig`, `WikipediaConfig` with optional env var overrides via `env()` helper
- Injected into Page/API classes via constructor, enabling easy mocking/testing
- Module-level constants used directly in API tests: `USER_TOKEN`, `USER_NAME`, `USER_ID`, `USER_PHONE`, `USER_COMPANY`, `NOTES_ID` — these are not in dataclasses

## Test Execution Commands

```bash
# Collect tests (verify structure)
pytest --collect-only -q

# Run all tests
pytest

# By marker
pytest -m ui          # UI only
pytest -m api         # API only
pytest -m load        # Load tests (Locust)

# Parallel execution
pytest -n auto        # xdist plugin

# Docker execution
docker build -t playwright-pytest-app .
docker run playwright-pytest-app pytest -m ui --alluredir=allure-results

# Generate Allure report
allure serve allure-results
```

## Critical Developer Workflows

### Adding a New UI Test
1. Create/update a Page Object in `pages/`
2. Define locators in `__init__` using Playwright's `page.locator()` or `page.get_by_role()`
3. Create action methods like `login()`, `search()`, returning appropriate values
4. In test file (`tests/ui/`), instantiate the page and use its methods
5. Markers: Add `@pytest.mark.ui` to test function

### Adding a New API Test
1. Create an API client class extending `BaseAPI` in `api/`
2. Inject `api_request_context` fixture into test (or session fixture like `users_login_api`)
3. Use the client's methods to make requests
4. Marker: Add `@pytest.mark.api`

### Debugging Failures
- Screenshots automatically attached to Allure on failure (see `pytest_runtest_makereport` in `conftest.py`)
- Videos recorded to `allure-results/videos/` for all tests (via `browser_context_args` fixture)
- Failed test names auto-beautified: `test_login_page` → "Login page" in Allure

## Important Conventions

### Pytest Configuration (`pytest.ini`)
- `norecursedirs = tests/load` - prevents Locust tests from running with regular pytest
- `addopts = -v --maxfail=3 --tb=short --alluredir=allure-results --strict-markers` - verbose, fail-fast (3 max), short tracebacks, Allure integration
- Test path: `testpaths = tests`
- Pythonpath: `.` (enables direct imports like `from config import settings`)

### Fixture Scope Rules
- `wikipedia_page` (function) - new instance per test
- `browser_context_args` (function) - enables video recording per browser context
- `note_payload` (function) - default note dict `{title, description, category}`
- `api_request_context`, `api_login_request_context` (session) - two separate Playwright request contexts (see Dual-context pattern above)
- `users_login_api`, `users_api`, `notes_api` (session) - API client instances
- `auth_token` (session) - derived from `users_api.login()`; reused across all tests for performance
- `wrong_api_request` (session) - context without auth headers, for negative auth tests

### Import Patterns
- Use relative imports: `from config import settings`, `from pages.login_page import LoginPage`
- Type hints with Playwright types: `page: Page`, `locator: Locator`, `context: APIRequestContext`

## Container & CI Integration

- **Local Docker**: `docker build -t playwright-pytest-app . && docker run playwright-pytest-app pytest`
- **Jenkins Pipeline** (`Jenkinsfile`):
  - Parameterized load test execution via Locust (LOCUST_USERS, SPAWN_RATE, RUN_TIME)
  - Container naming: `pw-tests-${BUILD_NUMBER}`, `locust-tests-${BUILD_NUMBER}`
  - Stages: Cleanup → Checkout → Build → Run Tests → Post (copy results, cleanup)
  - Allure report artifact collection

## Cross-Component Data Flow

1. **Config** → injected into Pages/APIs as dataclass instances
2. **Pages** → use Playwright `page` fixture; interact with UI
3. **Tests** → instantiate Pages/APIs; make assertions
4. **Fixtures** (conftest.py) → create `page` (Playwright), `api_request_context`, and convenience API fixtures
5. **Results** → pytest writes `results.xml`, Allure data to `allure-results/`; videos attached on failure

## When Adding Tests

- **Browser/Playwright-specific**: Use `page.screenshot()`, `page.locator()`, `expect()` from Playwright
- **Custom assertions**: Use pytest `assert` or Playwright's `expect()` (preferred for UI)
- **Parametrization**: Use `@pytest.mark.parametrize` (respects pytest.ini `--strict-markers`)
- **Skipping**: Use `@pytest.mark.skip(reason="...")` or `pytest.skip()`
- **Waits**: Rely on Playwright's auto-waiting; override with `timeout=` parameter if needed

## Key Files to Understand

- `tests/conftest.py` - Pytest hooks for Allure integration, fixture definitions
- `config/settings.py` - All constants and config dataclasses
- `pages/login_page.py` - `QABrainsLoginPage` (config-driven) and `ExpandTestingLoginPage` (settings constants + `page.route()` network interception)
- `pages/allo_tv_page.py` - `AlloTVPage`: example page without config dataclass; uses `is_visible()` for conditional UI interaction
- `pages/wikipedia_page.py` - `WikipediaPage`: config-driven POM pattern
- `api/base_api.py`, `api/users_api.py` - API client pattern; extend BaseAPI for new endpoints
- `pytest.ini` - Test discovery rules, marker definitions, Allure configuration

