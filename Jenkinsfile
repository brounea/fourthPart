pipeline {
	agent any
 	options {
 		buildDiscarder(logRotator(numToKeepStr: '5', daysToKeepStr: '2'))
 	}
	environment {
        registry = 'arnonbrouner/fourthpart'
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
		stage('run rest_app step') {
			steps {
				sh 'nohup python3 rest_app.py & '
			}
		}
		stage('run backend testing step') {
			steps {
				sh 'python3 backend_testing.py'
			}
		}
		stage('run clean environment step') {
			steps {
				sh 'python3 clean_environment.py'
			}
		}
	    stage('build and push image') {
            steps {
                script {
                    dockerImage = docker.build registry + ':$BUILD_NUMBER'
                    docker.withRegistry('', registryCredential) {
                    dockerImage.push()
                    }
                }
            }
         }
         stage('Create image version into the env file') {
			steps {
				script {
					sh "echo IMAGE_TAG=${BUILD_NUMBER} > .env"
				}
			}
		}
        stage('Run docker compose') {
            steps {
                script {
                     sh 'docker-compose up -d'
                }
            }
        }
        stage('Sleeping 15s ...') {
            steps {
                script {
                    sleep 15
                }
            }
        }
		stage('run docker_backend_testing.py step') {
			steps {
				sh 'python3 docker_backend_testing.py'

			}
		}
        stage('step dkr dwn & rmi ') {
			steps {
			    script {
				    sh "docker-compose down"
                    sh "docker rmi $registry:${BUILD_NUMBER}"
                }
			}
	    }
	    stage('Deploying HELM chart') {
			steps {
				script {
					sh "helm install release helm4/ --set image.version=$registry:${BUILD_NUMBER}"
				}
			}
		}
		stage('Wait for helm 20 sec...') {
            steps {
                script {
                    sleep 20
                }
            }
        }
        stage('Minikube Save service URLto file') {
			steps {
				script {
					sh 'minikube service fourthpartlbservice --url > k8s_url.txt &'
				}
			}
		}
//		stage('Wait for minikube service cmd for 20 sec...') {
//            steps {
//                script {
//                    sleep 20
//                }
//            }
//        }
//        stage('Test k8s services') {
//			steps {
//				script {
//					runPythonFile('K8S_backend_testing.py')
//				}
//			}
//		}

    }
}