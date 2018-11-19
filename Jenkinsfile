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
                echo "Code Coverage"
                sh ''' coverage run --cov=SimpleProducer.py 1 1 2 3
                       python -m coverage xml -o ./reports/coverage.xml'''
            }
        }
    }
}