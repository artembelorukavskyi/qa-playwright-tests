# QA Playwright Tests

Playwright + Pytest framework for UI/API test automation with Allure reports, Docker execution, and Jenkins pipeline.

## What's in the Repository

- UI tests (`tests/ui`) and API tests (`tests/api`) with `ui` and `api` markers.
- **Load tests (Locust)** (`tests/load/`) for performance and load testing.
- Page Objects in `pages/`:
- Page Object-и в `pages/`:
  - `WikipediaPage`
  - `QABrainsLoginPage`
- API клієнти в `api/`:
- API clients in `api/`:
  - `BaseAPI` — base class with `get()` and `post()` methods
  - `UsersAPI` — login and user profile retrieval
  - `NotesAPI` — creating and retrieving notes
- Global Pytest hooks/fixtures in `tests/conftest.py`:
  - `wikipedia_page` — UI fixture (function scope)
  - `auth_token` — сесійний токен, отриманий через `users_api.login()`
  - `auth_token` — session token obtained via `users_api.login()`
  - `note_payload` — default note payload (function scope)
  - `wrong_api_request` — context without auth token for negative tests
  - automatic video recording to `allure-results/videos/`
  - screenshot and video attached to Allure on test failure
  - human-readable test names in Allure
- Docker runner (`Dockerfile`) for running tests.
- Jenkins Docker image (`Dockerfile.jenkins`) with Docker-in-Docker support.
- Jenkins pipeline (`Jenkinsfile`) with parameterized Locust test execution.
- `docker-compose.yml` for local Jenkins + ngrok setup.

## Structure

```text
qa-playwright-tests/
├── pages/
│   ├── allo_tv_page.py
│   ├── login_page.py
│   └── wikipedia_page.py
├── tests/
│   ├── api/
│   │   ├── test_api_example.py
│   │   ├── test_api_playwright.py
│   │   ├── test_api_pytest.py
│   │   └── new.py                # scratch file, not collected by pytest
│   ├── ui/
│   │   ├── test_alert.py
│   │   ├── test_iframe.py
│   │   ├── test_login.py
│   │   ├── test_make_screenshot.py
│   │   ├── test_new_tab.py
│   │   ├── test_selector.py
│   │   ├── test_sorter.py
│   │   └── test_wiki_page.py
│   ├── load/
│   │   └── test_login.py         # Locust load tests
│   └── conftest.py
├── config/
│   ├── settings.py               # BASE_URL, USER_EMAIL, USER_PASSWORD, USER_TOKEN, USER_ID, NOTES_ID, etc.
│   └── __init__.py
├── api/
│   ├── base_api.py
│   ├── users_api.py
│   └── notes_api.py
├── screenshots/                  # screenshots on test failure
├── AGENTS.md
├── Dockerfile                    # Docker image for running Playwright tests
├── Dockerfile.jenkins            # Docker image for Jenkins with Docker-in-Docker
├── Jenkinsfile                   # Pipeline for Playwright and Locust tests
├── docker-compose.yml
├── pytest.ini
└── requirements.txt
```

## Prerequisites

## Передумови
- `pip`
- Docker + Docker Compose (for containerized execution/CI)
- Jenkins (if running the pipeline locally)

## Local Setup (without Docker)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
playwright install chromium
```

Verify test collection:

```bash
.venv/bin/pytest --collect-only -q
```

Run tests:

```bash
# All tests
.venv/bin/pytest

# UI only
# Тільки UI

# API only
.venv/bin/pytest -m api

# Parallel execution
# Паралельно
```

## Pytest Configuration

Config in `pytest.ini`:

- `--maxfail=3`
- `--tb=short`
- `--alluredir=allure-results`
## Налаштування Pytest
Конфіг у `pytest.ini`:
- `pythonpath = .`

## Dockerfile

**Dockerfile** (main image for Playwright tests):

```dockerfile
**Dockerfile** (основний образ для Playwright тестів):

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN playwright install chromium --with-deps

COPY . .

ENV PYTHONUNBUFFERED=1
```

**Dockerfile.jenkins** (Docker image for Jenkins with Docker-in-Docker):

Includes:
- Jenkins LTS base image
- Python 3 and pip for running tests
- Docker CLI and Docker Compose Plugin for launching containers from Jenkins
- Jenkins LTS базовий образ
This allows Jenkins to run Docker containers during pipeline execution.
- Docker CLI та Docker Compose Plugin для запуску контейнерів з Jenkins

## Allure
Results are written to `allure-results/` by default.
Результати пишуться в `allure-results/` за замовчуванням.

```bash
allure serve allure-results
```
Logic in `tests/conftest.py`:
За логікою в `tests/conftest.py`:
- on test failure, a full-page screenshot is attached;
- the browser session video is attached to the report if the file exists.

## Running Tests in Docker

Build the image:

Збірка образу:
docker build -t playwright-pytest-app .
```

Run tests in a container:

```bash
docker run --rm -u 0 -v "$PWD:/app" playwright-pytest-app \
  python3 -m pytest -v \
  --junitxml=results.xml \
  --alluredir=allure-results \
  --reruns 1 \
  --tracing retain-on-failure
```

## Jenkins and Docker Compose

`docker-compose.yml` starts:

- `jenkins` (container `jenkins_universal` based on `Dockerfile.jenkins`)
- `ngrok` (for tunneling Jenkins)

First run:

```bash
docker volume create jenkins_home
docker compose up -d --build
```

Jenkins UI:

```text
http://localhost:8080
```

Minimum required Jenkins plugins:

- `Pipeline`
- `Git`
- `Docker Pipeline`
- `Allure Jenkins Plugin`
- `JUnit` (usually pre-installed)

## Jenkinsfile Pipeline
### 1. **Очистка та завантаження коду**
The pipeline consists of 3 main stages:

### 1. **Cleanup and Code Checkout**

```groovy
Видаляє попередні результати та завантажує останній код з Git.
### 2. **Запуск Playwright тестів**
```

Removes previous results and pulls the latest code from Git.

### 2. **Run Playwright Tests**

```groovy
stage('Run Playwright Tests') {
    sh "docker run --name pw-tests-${BUILD_NUMBER} -u 0 playwright-pytest-app \
- Запускає UI/API тести паралельно (флаг `-n auto`)
- Генерує `results.xml` для JUnit
- Результати збираються в `allure-results/`
### 3. **Запуск Locust Load тестів**
```

- Runs UI/API tests in parallel (`-n auto` flag)
- Generates `results.xml` for JUnit
- Results collected to `allure-results/`

### 3. **Run Locust Load Tests**

```groovy
stage('Run Locust Tests') {
    sh """
    docker run --name ${env.LOCUST_CONTAINER} -u 0 ${env.DOCKER_IMAGE} \
**Параметризовані параметри:**
- `LOCUST_USERS` (за замовч. `10`) — кількість віртуальних користувачів
- `LOCUST_SPAWN_RATE` (за замовч. `2`) — користувачів на секунду
- `LOCUST_RUN_TIME` (за замовч. `1m`) — тривалість тесту (30s, 2m, 5m, etc.)
```

### 4. **Публікація результатів**

- `LOCUST_USERS` (за замовч. `10`) — кількість віртуальних користувачів
**Parameterized inputs:**
- Allure звіт для Playwright тестів
- `LOCUST_USERS` (default `10`) — number of virtual users
- `LOCUST_SPAWN_RATE` (default `2`) — users spawned per second
- `LOCUST_RUN_TIME` (default `1m`) — test duration (30s, 2m, 5m, etc.)
    always {
### 4. **Publish Results**
        junit 'results.xml'
### Запуск 1: Базовий тест (значення за замовчуванням)
**Параметри:**
}
```

- Allure звіт для Playwright тестів
- JUnit звіт
- HTML звіт Locust

## Приклади запуску тестів у Jenkins
- Allure report for Playwright tests
- JUnit report
- Locust HTML report
**Параметри:**
## Jenkins Test Run Examples
**Параметри:**
### Run 1: Basic test (default values)

**Parameters:**
http://localhost:8080/job/your-job-name/build
```

**Команда (якщо запускати з CLI):**

### Запуск 2: Легкий тест — 5 користувачів, 30 секунд

**Параметри:**
Click "Build" — default parameters will be used.
- LOCUST_SPAWN_RATE: 1
### Run 2: Light test — 5 users, 30 seconds

**Parameters:**

```bash
**Параметри:**
  -F LOCUST_USERS=5 \
**Command (CLI):**
  -F LOCUST_RUN_TIME=30s
```

**Команда (CLI):**

### Запуск 3: Помірний тест — 20 користувачів, 2 хвилини

**Параметри:**
**Result:** Light load for verifying API stability.
- LOCUST_SPAWN_RATE: 4
### Run 3: Moderate test — 20 users, 2 minutes

**Parameters:**

```bash
**Результат:**
- 20 віртуальних користувачів
**Command (CLI):**
- HTML звіт у `locust-report.html`
- Tiempo відповідей логується
**Параметри:**

**Результат:** 
- 20 віртуальних користувачів
- 4 користувачів на секунду запускаються
**Команда (CLI):**
**Result:**
- 20 virtual users
- 4 users spawned per second
- HTML report at `locust-report.html`
- Response times logged
- LOCUST_USERS: 100
### Run 4: Stress test — 100 users, 5 minutes
- LOCUST_RUN_TIME: 5m
**Parameters:**
**Команда (CLI):**

**Результат:**
- Значне навантаження на сервер
**Command (CLI):**
### Запуск 5:Ночний тест — 50 користувачів, 30 хвилин
**Параметри:**
  -F LOCUST_SPAWN_RATE=10 \
  -F LOCUST_RUN_TIME=5m
```

**Команда (CLI):**
- Значне навантаження на сервер
**Result:**
- Heavy server load
- Explores maximum concurrent connections
- Data on latency and error rate
- Довготривале тестування стабільності
### Run 5: Overnight test — 50 users, 30 minutes
- Детальна статистика в HTML звіті
**Parameters:**
**Команда (CLI):**

```bash
### Запуск через Jenkins UI
**Command (CLI):**
2. Натиснути **"Build with Parameters"**
3. Заповнити поля:
   - `LOCUST_USERS`: кількість користувачів
   - `LOCUST_SPAWN_RATE`: користувачів на секунду
   - `LOCUST_RUN_TIME`: час тесту (30s, 2m, 5m, 30m)
4. Натиснути **"Build"**
5. Переглянути результати:
   - Консоль виведення: `http://localhost:8080/job/your-job-name/BUILD_NUMBER/console`
**Result:**
- Long-running stability test
- Typically run outside business hours
- Detailed statistics in the HTML report
- **Trend:** Графік результатів за часом (якщо встановити Jenkins Trend Plugin)
### Running via Jenkins UI
   - Locust HTML звіт (артефакт)
1. Navigate to Job: `http://localhost:8080/job/your-job-name`
2. Click **"Build with Parameters"**
3. Fill in the fields:
   - `LOCUST_USERS`: number of users
   - `LOCUST_SPAWN_RATE`: users per second
   - `LOCUST_RUN_TIME`: test duration (30s, 2m, 5m, 30m)
4. Click **"Build"**
5. View results:
   - Console output: `http://localhost:8080/job/your-job-name/BUILD_NUMBER/console`
   - Allure report (for Playwright tests)
   - Locust HTML report (artifact)
- `@task(10) login_successful()` — успішний логін (вага 10)
### Monitoring Integration
- `@task(1) login_failed_wrong_password()` — логін з неправильним паролем (вага 1)
After a Jenkins test run you can review:
  - Використовує `catch_response=True` для контролю успіху
- **Locally:** Download `locust-report.html` from artifacts
- **Trend:** Results graph over time (install Jenkins Trend Plugin)
- **Email:** Result notifications (configurable in Post Actions)
- `@task(1) login_failed_wrong_password()` — логін з неправильним паролем (вага 1)
## Locust Load Tests
**З Web UI:**
**tests/load/test_login.py** — load testing of the API login endpoint.
### Локальний запуск Locust
### What Is Tested
**Headless режим (без UI):**

```bash
    wait_time = constant_throughput(5)  # 5 requests per second
  -u 10 \
  -r 2 \
  --run-time 2m \
**Tasks:**
- `-u, --users` — кількість користувачів
- `@task(10) login_successful()` — successful login (weight 10)
  - Retrieves token, stores in `self.token`
- `@task(1) login_failed_wrong_password()` — login with wrong password (weight 1)
  - Expects status code 400 or 401
  - Uses `catch_response=True` to control pass/fail

### Running Locust Locally
- `-r, --hatch-rate` — користувачів/сек на яких запускати
**Headless mode (no UI):**
- `--html` — генерує HTML звіт

### Hooks для логування

Event listener `request_handler` логує успішні логіни та логауты:

```python
@events.request.add_listener
### Важливо
**With Web UI:**
- Logout в `on_stop()` видаляє сесію користувача
- `catch_response=True` дозволяє явно контролювати, що вважати успіхом/невдачею
```

### Важливо
Open http://localhost:8089 and configure parameters via the UI.
### Приклад звіту тестування (10 користувачів, 1 хвилина)
**Parameters:**
| Метрика | Значення |
- `-u, --users` — number of users
- `-r, --hatch-rate` — users to spawn per second
- `--run-time` — duration (30s, 2m, 5m)
- `--html` — generates an HTML report
### Приклад звіту тестування (10 користувачів, 1 хвилина)
### Logging Hooks
**Aggregated статистика:**
Event listener `request_handler` logs successful logins and logouts:
| Метрика | Значення |
|---------|----------|
| Total Requests | 50 |
**Детальна статистика по типам запитів:**
| Average Response Time | 10812 ms |
| Min | 140 ms |
| Max | 17831 ms |
| Median | 13000 ms |
| Requests/sec | 0.72 |
### Notes

- Token is retrieved in `on_start()` for each user
- Logout in `on_stop()` removes the user session
- `catch_response=True` allows explicit control over what counts as success/failure
|------|------|--------|---------|-----|-----|-----|-----|
## Locust Test Results
| POST | Login User: artem.bilorukavskyi@ukr.net | 36 | 0(0.00%) | 11884 | 232 | 17831 | 14000 |
### Sample report (10 users, 1 minute)

**Aggregated statistics:**

| Metric | Value |
|--------|-------|
| DELETE | Login User | 9400 | 9400 | 9400 | 9400 | 9400 | 9400 | 9400 | 9400 | 9400 | 9400 | 9400 |
**Завершення тесту:**
| POST | Login with wrong password | 6300 | 6300 | 8200 | 8200 | 8200 | 8200 | 8200 | 8200 | 8200 | 8200 | 8200 |

**Завершення тесту:**

```
[2026-03-24 16:05:42,950] cc0317773f3a/INFO/locust.main: writing html report to file: locust-report.html
**Аналіз результатів:**
**Detailed statistics by request type:**

- ✅ **0% помилок** — API стабільна, всі запити успішні
- **36 успішних логінів** — основний скенарій виконується без збоїв
- **4 тестів неправильного пароля** — перевірка обробки помилок працює коректно
- **10 логаутів** — сесії закриваються чисто
- **Середній час відповіді:** 10.8 сек для всіх операцій
## Результати тестування Playwright
### Приклад успішного запуску (28 тестів)

**Інформація про сесію:**
|------|------|-----|-----|-----|-----|-----|-----|-----|-----|-------|--------|------|
### Приклад успішного запуску (28 тестів)

**Інформація про сесію:**

**Test completion:**
**Конфігурація:**
cachedir: .pytest_cache
collecting ... collected 28 items
```

**Конфігурація:**
**Results analysis:**
- Python: 3.10.12
- ✅ **0% errors** — API is stable, all requests successful
- **36 successful logins** — main scenario runs without failures
- **4 wrong-password tests** — error handling works correctly
- **10 logouts** — sessions closed cleanly
- **Average response time:** 10.8 sec across all operations
- **Peak load:** 0.72 requests/sec
| # | Test | Status | Progress |
## Playwright Test Results
| 1 | tests/ui/test_alert.py::test_alert_on_page | PASSED | 3% |
### Sample successful run (28 tests)
| 3 | tests/ui/test_login.py::test_login_page | PASSED | 10% |
**Session info:**
| 5 | tests/ui/test_login.py::test_change_text_after_login | PASSED | 17% |
| 6 | tests/ui/test_make_screenshot.py::test_screenshot | PASSED | 21% |
| 7 | tests/ui/test_new_tab.py::test_new_tab | PASSED | 25% |
| 8 | tests/ui/test_selector.py::test_selector | PASSED | 28% |
| 9 | tests/ui/test_sorter.py::test_sorter | PASSED | 32% |
| 10 | tests/ui/test_wiki_page.py::test_wikipedia_about | PASSED | 35% |
| 11 | tests/ui/test_wiki_page.py::test_wiki_talk_page | PASSED | 39% |
**Configuration:**
| 13 | tests/api/test_api_example.py::test_open_test_site | PASSED | 46% |
| 14 | tests/api/test_api_playwright.py::test_login | PASSED | 50% |
| 15 | tests/api/test_api_playwright.py::test_get_user_profile | PASSED | 53% |
| 16 | tests/api/test_api_playwright.py::test_get_user_profile_fail | PASSED | 57% |
| 17 | tests/api/test_api_playwright.py::test_create_note | PASSED | 60% |
| 18 | tests/api/test_api_playwright.py::test_get_all_notes | PASSED | 64% |
**All test statuses:**
| 20 | tests/api/test_api_playwright.py::test_get_notes_by_wrong_id | PASSED | 71% |
| 21 | tests/api/test_api_pytest.py::test_login | PASSED | 75% |
| 22 | tests/api/test_api_pytest.py::test_login_fail_wrong_password | PASSED | 78% |
| 23 | tests/api/test_api_pytest.py::test_get_user_profile | PASSED | 82% |
| 24 | tests/api/test_api_pytest.py::test_get_user_profile_invalid_token | PASSED | 85% |
| 25 | tests/api/test_api_pytest.py::test_create_note | PASSED | 89% |
| 26 | tests/api/test_api_pytest.py::test_get_all_notes | PASSED | 92% |
| 27 | tests/api/test_api_pytest.py::test_get_notes_by_id | PASSED | 96% |
**Результат:**

**Результат:**

```
============================== 28 passed ==============================
```

✅ **Усі 28 тестів пройшли успішно!**

✅ **Усі 28 тестів пройшли успішно!**
- **UI тести:** 12 тестів PASSED
- **API тести:** 16 тестів PASSED
- **Час виконання:** ~5 хвилин
## Важливо про стабільність тестів

Тести залежать від зовнішніх сайтів (`wikipedia.org`, `qa-practice.com`, `expandtesting.com`, `practice.qabrains.com`, `demoqa.com`, `allo.ua`), тому можливі флейки через мережу, зміни сторінок або тимчасову недоступність сервісів.

## Нотатка про безпеку

## Нотатка про безпеку

У `docker-compose.yml` зараз прописані `NGROK_AUTHTOKEN` і фіксований ngrok URL. Для спільного репозиторію краще винести секрети у змінні оточення або `.env` і не комітити токени у відкритому вигляді.

**Result:**
