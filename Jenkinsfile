pipeline {
    agent any

    environment {
        GIT_PROJECT_NAME = "WebGoat"
        GIT_PROJECT_URL ="http://github.com/WebGoat/${GIT_PROJECT_NAME}.git"
        GIT_PROJECT_VERSION = "8.1.0"
        GIT_PROJECT_BRANCH = "refs/tags/v${GIT_PROJECT_VERSION}"


    }

    stages {

        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }

        stage('Clone Java Repo') {
            steps {
                checkout changelog: false, poll: false, scm: scmGit(
                    branches: [[name: "${GIT_PROJECT_BRANCH}"]],
                    extensions: [],
                    userRemoteConfigs: [[url: "${GIT_PROJECT_URL}"]]
                )
            }
        }

        stage('Install Dependencies with Maven') {
            steps {
                sh 'mvn clean install -DskipTests'

            }
        }

        stage('Copy Maven Dependencies') {
            steps {
                sh 'mvn dependency:copy-dependencies -DoutputDirectory=/tmp/folder_to_scan'
            }
        }

        stage('Run Dependency Check') {
            steps {
                sh 'mvn org.owasp:dependency-check-maven:aggregate -DscanDirectory=/tmp/folder_to_scan -Dformat=JSON -DprettyPrint=true'
            }
        }


        stage('Run python script for dependency check') {
            steps {
                sh'''
                    #!/bin/bash
                    cd /code
                    python -m venv /code/venv
                    . venv/bin/activate
                    pip install --no-cache-dir --upgrade -r requirements.txt
                    python /code/bom-convert.py /var/jenkins_home/workspace/${JOB_NAME}/target/dependency-check-report.json

                    mv /code/bom-test.json /code/${GIT_PROJECT_NAME}-${GIT_PROJECT_VERSION}-cyclonedx.json
                '''
            }
        }

        stage('curl to dependency check') {
            steps {
                sh """
                    curl -X "POST" "http://host.docker.internal:8081/api/v1/bom" \
                    -H "Content-Type: multipart/form-data" \
                    -H "X-Api-Key: ${env.DEPENDENCY_TRACK_API_KEY}" \
                    -F "autoCreate=true" \
                    -F "projectName=${GIT_PROJECT_NAME}" \
                    -F "projectVersion=${GIT_PROJECT_VERSION}" \
                    -F "bom=@/code/${GIT_PROJECT_NAME}-${GIT_PROJECT_VERSION}-cyclonedx.json"
                """
            }
        }
    }
}

// odt_rLzGPeti1xqMFwsjUg1BaR7lssnYBwRC