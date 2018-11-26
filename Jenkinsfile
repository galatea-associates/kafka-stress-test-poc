#!/usr/bin/env groovy

// Based on https://github.com/jerearista/python-jenkinsfile-testing/blob/master/Jenkinsfile
pipeline {
    agent any
    options {
        buildDiscarder(
            // Only keep the 10 most recent builds
            logRotator(numToKeepStr:'10'))
    }
    environment {
        projectName = 'Kafka_Python'
        VIRTUAL_ENV = "${env.WORKSPACE}/venv"
    }
    stages {
        stage('Install Requirements'){
            steps {
                sh """
                    echo ${SHELL}
                    [ -d venv ] && rm -rf venv
                    virtualenv venv --python=python3.6
                    #. venv/bin/activate
                    export PATH=${VIRTUAL_ENV}/bin:${PATH}
                    python3 -m pip install -r requirements.txt
                    make clean
                """
            }
        }

        stage ('Check_style') {
            steps {
                sh """
                    #. venv/bin/activate
                    [ -d report ] || mkdir report
                    export PATH=${VIRTUAL_ENV}/bin:${PATH}
                """
                sh """
                    export PATH=${VIRTUAL_ENV}/bin:${PATH}
                    make flake8 | tee report/flake8.log || true
                """
                sh """
                    export PATH=${VIRTUAL_ENV}/bin:${PATH}
                    make pylint | tee report/pylint.log || true
                """
                step([$class: 'WarningsPublisher',
                  parserConfigurations: [[
                    parserName: 'Pep8',
                    pattern: 'report/flake8.log'
                  ],
                  [
                    parserName: 'pylint',
                    pattern: 'report/pylint.log'
                  ]],
                  unstableTotalAll: '0',
                  usePreviousBuildAsReference: true
                ])
            }
        }

         stage ('Unit Tests') {
            steps {
                sh """
                    #. venv/bin/activate
                    export PATH=${VIRTUAL_ENV}/bin:${PATH}
                    make unittest || true
                """
            }

            post {
                always {
                    junit keepLongStdio: true, testResults: 'report/pytest.xml'
                    publishHTML target: [
                        reportDir: 'report/coverage',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report - Unit Test'
                    ]
                }
            }
        }

        stage ('System Tests') {
            steps {
                sh """
                    #. venv/bin/activate
                    export PATH=${VIRTUAL_ENV}/bin:${PATH}
                    make systest || true
                """
            }

            post {
                always {
                    junit keepLongStdio: true, testResults: 'report/pytest.xml'
                    publishHTML target: [
                        reportDir: 'report/coverage',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report - System Test'
                    ]
                }
            }
        }

         stage ('Docs') {
            steps {
                sh """
                    #. venv/bin/activate
                    export PATH=${VIRTUAL_ENV}/bin:${PATH}
                    PYTHONPATH=. pdoc --html --html-dir docs --overwrite ${env.projectName}
                """
            }

            post {
                always {
                    publishHTML target: [
                        reportDir: 'docs/Kafka_Python',
                        reportFiles: 'index.html',
                        reportName: 'Module Documentation'
                    ]
                }
            }
        } 

        stage ('Cleanup') {
            steps {
                sh 'rm -rf venv'
            }
        }
        
    }
} 