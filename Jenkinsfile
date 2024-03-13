pipeline {
    agent any
    environment {
        PROJECT_ID = 'multi-ks8-416911'
                CLUSTER_NAME = 'k8s-project'
                LOCATION = 'us-east1-b'
                CREDENTIALS_ID = 'kubernetes'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'cf87cc0d-dd7a-4cdb-8945-a0a678c812', url: 'https://github.com/Egaresg26/PokeAPI_Minpro.git']])
            }
        }
        stage('Build image') {
            steps {
                script {
                    app = docker.build("egarg26/pokeapibri:${env.BUILD_ID}")
                    }
            }
        }

        stage('Push image') {
            steps {
                script {
                    withCredentials( \
                                 [string(credentialsId: 'docker',\
                                 variable: 'docker')]) {
                        sh "docker login -u egarg26  --password-stdin ${docker}"
                    }
                    app.push("${env.BUILD_ID}")
                 }

            }
        }

        stage('Deploy to K8s') {
            steps{
                echo "Deployment started ..."
                sh 'ls -ltr'
                sh 'pwd'
                sh "sed -i 's/pokeapibri:latest/pokeapibri:${env.BUILD_ID}/g' deployment.yaml"
                step([$class: 'KubernetesEngineBuilder', \
                  projectId: env.PROJECT_ID, \
                  clusterName: env.CLUSTER_NAME, \
                  location: env.LOCATION, \
                  manifestPattern: 'deployment.yaml', \
                  credentialsId: env.CREDENTIALS_ID, \
                  verifyDeployments: true])
                }
            }
        }
}
