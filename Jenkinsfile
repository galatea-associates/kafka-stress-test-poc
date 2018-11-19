pipeline {
    agent any
    stages {
        stage('Build'){
            steps{
                echo 'hello world'
                sh ''' python3 --version
                       pip3 --version'''
            }
        }
        stage('Static code metrics'){
            steps{
                echo "Cover Coverage"
                sh ''' source active ${BUILD_TAG}
                       py.test --cov=Kafka-Python test/'''
            }
        }
    }
}