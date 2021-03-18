pipeline {
	agent any
 	options {
 		buildDiscarder(logRotator(numToKeepStr: '5', daysToKeepStr: '2'))
 	}
	environment {
        registry = 'brounea/fourthPart'
        registryCredential = 'docker_hub'
        dockerImage = ''
    }
	stages {
		stage('Git checkout') {
			steps {
				script {
					properties([pipelineTriggers([pollSCM('*/30 * * * *')])])
				}
                // Git checkout my project from remote (git 'https://github.com/brounea/fourthpart.git')
				checkout scm
			}
		}
		stage('Pip install missing dependencies') {
			steps {
				script {
					if (isUnix()) {
						sh 'pip3 install flask requests selenium pymysql -t ./'
					} else {
						bat 'pip3 install flask requests selenium pymysql -t ./'
					}
				}
			}
		}
		stage('run rest_app bkend step') {
			steps {
				script {
					PythonFileExe('rest_app.py',1)
				}
			}
		}
		stage('run backend testing step') {
			steps {
				script {
					PythonFileExe('backend_testing.py test',0)
				}
			}
		}
		stage('run clean environment step') {
			steps {
				script {
					PythonFileExe('clean_environment.py',0)
				}
			}
		}
	    stage('build and push image') {
            steps {
                script {
                    dockerImage = docker.build registry + ":$BUILD_NUMBER"
                    docker.withRegistry('', registryCredential) {
                    dockerImage.push()
                    }
                }
            }
         }
        stage('Run docker compose -d') {
            steps {
                script {
                     sh 'docker compose up -d'
                }
            }
        }
		stage('run docker environment step') {
			steps {
				script {
					PythonFileExe('docker_backend_testing.py',0)
				}
			}
		}
		stage('Clean docker environment') {
            steps {
                script {
                 sh "docker-compose down"
                sh "docker image rm $registry:$BUILD_NUMBER"
                }
            }
        }
    }
	post {
	    failure {
	        mail body: "Jenkins-${JOB_NAME}-${BUILD_NUMBER} FAILED Check issue: $env.JOB_URL",
	        bcc: '', cc: '', from: 'Jenkins@gmail.com', replyTo: 'no-reply@gmail.com',
	        subject: "Jenkins-${JOB_NAME}-${BUILD_NUMBER} FAILED", to: 'arnon.brouner@gmail.com'
	    }
	}
}
def PythonFileExe(pyfilename, bckground){
// run python file, used for the testing files and fail the build in case of error
	try{
		if (isUnix()) {
		   if (${bckground} == 0) {
		      //running normal process
			    sh "python3.9 ${pyfilename}"
			}
			else {
			 //running in the background
			    sh "nohup python3.9 ${pyfilename} &"
			}
		} else {
		//windows we dont care :)
			bat "python ${pyfilename}"
		}
	} catch (Throwable e) {
		echo "Caught in runPythonFile for ${pyfilename}, ${e.toString()}"
		// mark the job as failed
		currentBuild.result = "FAILURE"
	    }
    }

