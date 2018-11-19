pipeline {
    agent any
    stages {
        stage('Build'){
            steps{
                echo 'hello world'
                sh ''' which python
                       which pip '''
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