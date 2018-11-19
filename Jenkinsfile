pipeline {
    agent any
    stages {
        stage('Build'){
            steps{
                echo 'hello world'
                sh ''' which python
                       pyhton --version
                       which pip 
                       which python3
                       pyhton3 --version'''
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