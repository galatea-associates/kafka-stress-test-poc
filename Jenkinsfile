pipeline {
    agent any
    stages {
        stage('Build'){
            steps{
                echo 'hello world'
                sh ''' sudo apt-get install python3 -y
                       which python
                       python --version
                       which pip 
                       which python3
                       python3 --version'''
            }
        }
        stage('Static code metrics'){
            steps{
                echo "Cover Coverage"
                sh ''' source active ${BUILD_TAG}
                       coverage run '''
            }
        }
    }
}