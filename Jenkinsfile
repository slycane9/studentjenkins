pipeline { 
    agent any 
    options {
        skipStagesAfterUnstable()
    }
    
    stages {
        stage('Build') { 
            steps { 
                sh '''#!/bin/bash
                pwd
                echo copying tests to git repo
                cp /u/srolo/netsec-tests/test1-2.py $(pwd)/newsapp/newslister/tests.py
                '''
            }
        }
        
        stage('Submit Check'){
            steps {
                script {
                    try{
                        sh 'ls submit.txt'
                        echo "Submission mode activated"}
                    catch(err){
                        echo "Submission mode not activated"
                        currentBuild.result = 'ABORTED' }
                }
            }
        }
        
        stage('Test'){
            when {expression{currentBuild.result != 'ABORTED'}}
            steps {
                sh 'echo test phase'
                script{
                    try{
                        withEnv(['PATH+JENKINSHOME=/u/srolo/.local/bin']) {
                            sh '''#!/bin/bash
                            cd newsapp
                            pipenv install django
                            pipenv run pip install newsapi-python
                            pipenv run pip install cryptography
                            pipenv run python generate_secret.py
                            pipenv run python manage.py migrate --run-syncdb
                            pipenv run python manage.py test || exit -1
                            mail -s "Lab 1 Success" serdjanrolovic@gmail < result.txt
                            ls
                            '''
                            
                        }
                    }
                    catch(err){
                        currentBuild.result = 'FAILURE'
                    }
                }
            }
        }
        
        stage('Send Fail Results') {
            steps { 
                sh '''#!/bin/bash
                ls
                mail -s "Lab 1 Results" serdjanrolovic@gmail < newsapp/result.txt
                '''
            }
        }
    }
    
    post {  
         always {  
             echo 'This will always run'  
         }  
         success {  
             echo 'This will run only if successful'
             sh 'mail -s "Lab 1 Passed" serdjanrolovic@gmail < newsapp/result.txt'
         }  
         failure {  
             sh 'mail -s "Lab 1 Passed" serdjanrolovic@gmail < newsapp/result.txt'         }  
     }  
}
