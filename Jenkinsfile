pipeline {
    agent any

    options {
        ansiColor('xterm')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 30, unit: 'MINUTES')
    }

    parameters {
        string(name: 'LOCUST_USERS', defaultValue: '10', description: 'Кількість віртуальних користувачів для Locust.')
        string(name: 'LOCUST_SPAWN_RATE', defaultValue: '2', description: 'Швидкість спавну (користувачів/сек).')
        string(name: 'LOCUST_RUN_TIME', defaultValue: '1m', description: 'Тривалість навантажувального тесту.')
    }

    environment {
        DOCKER_IMAGE = "playwright-pytest-app"
        PW_CONTAINER = "pw-tests-${env.BUILD_NUMBER}"
        LOCUST_CONTAINER = "locust-tests-${env.BUILD_NUMBER}"
    }

    stages {
        stage('Cleanup Workspace') {
            steps {
                deleteDir()
                sh "docker rm -f ${env.PW_CONTAINER} ${env.LOCUST_CONTAINER} || true"
            }
        }

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker') {
            steps {
                sh "docker build -t ${env.DOCKER_IMAGE} ."
            }
        }

        stage('Run Playwright Tests') {
            steps {
                script {
                    catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                        sh """
                        docker run --name ${env.PW_CONTAINER} \
                        -u 0 ${env.DOCKER_IMAGE} \
                        python3 -m pytest -v --color=yes tests/ui tests/api \
                        --junitxml=results.xml \
                        --alluredir=allure-results/json
                        """
                    }
                }
            }
        }

        stage('Run Locust Tests') {
            steps {
                script {
                    catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                        sh """
                        docker run --name ${env.LOCUST_CONTAINER} \
                        -u 0 ${env.DOCKER_IMAGE} \
                        locust -f tests/load/test_login.py --headless \
                        -u ${params.LOCUST_USERS} \
                        -r ${params.LOCUST_SPAWN_RATE} \
                        --run-time ${params.LOCUST_RUN_TIME} \
                        --html locust-report.html
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                // Копіюємо звіти з контейнерів на хост Jenkins
                sh "docker cp ${env.PW_CONTAINER}:/app/allure-results ."
                sh "docker cp ${env.PW_CONTAINER}:/app/results.xml ."
                sh "docker cp ${env.LOCUST_CONTAINER}:/app/locust-report.html ."

                // Публікація Allure-звіту
                allure includeProperties: false, results: [[path: 'allure-results/json']]

                // Публікація JUnit результатів (для графіків)
                junit 'results.xml'

                // Архівуємо HTML звіт Locust
                archiveArtifacts artifacts: 'locust-report.html', allowEmptyArchive: true
            }
        }
        cleanup {
            // Гарантоване видалення контейнерів після завершення роботи
            sh "docker rm -f ${env.PW_CONTAINER} ${env.LOCUST_CONTAINER} || true"
        }
    }
}