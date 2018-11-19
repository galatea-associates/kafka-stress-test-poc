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
                sh  ''' pylint3 --disable=C . || true
                    '''
                echo "Cover Coverage"
                sh ''' py.test --cov=Kafka-Python test/'''
            }
        }
    }
}