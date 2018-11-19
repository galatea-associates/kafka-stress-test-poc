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
                echo "PEP8 style check"
                sh  ''' source activate ${BUILD_TAG}
                        pylint3 --disable=C . || true
                    '''
                echo "Cover Coverage"
                sh ''' source active ${BUILD_TAG}
                       py.test --cov=Kafka-Python test/'''
            }
        }
    }
}