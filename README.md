# dep-check-track
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Jenkins Badge](https://img.shields.io/badge/Jenkins-D24939?logo=jenkins&logoColor=fff&style=for-the-badge)
![OWASP Dependency-Check Badge](https://img.shields.io/badge/OWASP%20Dependency--Check-F78D0A?logo=dependencycheck&logoColor=fff&style=for-the-badge)

![dependcy tracl](images/img.png)
## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [Running Dependency Track with docker-compose](#run-dependency-track--with-docker-compose-)
  - [Running Jenkins with Dependency Check](#running-jenkins-with-dependency-check)
- [Configuration](#configuration)
    - [Dockerfile](#dockerfile)

## Introduction
In this project will demonstrate how to run a [Jenkins](https://www.jenkins.io/) CI pipeline
with [OWASP Dependency Check](https://owasp.org/www-project-dependency-check/) 
to scan the [WebGoat-v.8.10](https://github.com/WebGoat/WebGoat/tree/v8.1.0) project for open source packages with known vulnerabilities and report them via [Dependency Track](https://dependencytrack.org/).


## Prerequisites

Please ensure you have the following on your machine :
- [git](https://git-scm.com/downloads) installed on your machine.
- [Docker](https://www.docker.com/get-started/) installed on your machine.
- [Docker Compose](https://docs.docker.com/compose/install/) installed on your machine.

## Getting Started

- Clone the project to your machine with the following git command :
    ```shell
    git clone https://github/ramibo/dep-check-track.git
    ```
- Change the directory to the project directory :
    ```shell
    cd dep-check-track
    ```

- Create a docker network :

  It will be used to connect the dependency track with jenkins. 
  ```shell
  docker network create myowaspnetwork
  ```
### Run Dependency Track ( with docker-compose )

- Run the dependency track container with the following command :
  ```shell
  docker-compose up -d
  ```
  As success message you should see something like this :

  <img src="images/img_1.png" alt="Your Image Description" style="width: 50%;" />
  

- Open your web browser and access dependency track web ui via http://localhost:8080


- Login with the default credentials (admin/admin):

  **Username** : admin

  **Password** : admin


- Change the default password and login credentials and relogin to the application.


- On the left side menu go to Administration -> Access Management -> Teams -> click on **Automation** team or create a new team.
  - Copy the **API key** and save it for later use.
  - At the **Permissions** section of the team ,click on the ```+``` symbole -> select all the permissions and click on the select button.

    <img src="images/img_3.png" alt="Your Image Description" style="width: 60%;" />


- Create a policy for the project : #Todo
  - Go to Administration -> Project -> Policies -> click on the ```+``` symbole.
  - Enter the policy name and description.
  - Select the **Automation** team.
  - Select the **High** severity level.
  - Select the **Fail build** option.
  - Click on the **Save** button.

### Running Jenkins with Dependency Check

- Build the jenkins docker image via Dockerfile
  ```shell
  docker build -t rammatz/jenkins-image:latest .
  ```


- Run the Jenkins image as a docker container ( Replace the DEPENDENCY_TRACK_API_KEY value with your api key saved in the previous step ):

  ```shell
  docker run --detach \
           --name jenkins-container \
           --network dep-check-track_myowaspnetwork \
           -p 8082:8080 \
           -p 50000:50000 \
           -v /tmp/jenkins/home:/var/jenkins_home \
           -e DEPENDENCY_TRACK_API_KEY=<YOUR_API_KEY> \
           rammatz/jenkins-image:latest
  ```

- Get the initial admin password for Jenkins and copy it to the clipboard :
  ```shell
  docker exec -it jenkins-container cat /var/jenkins_home/secrets/initialAdminPassword
  ```
  Or
  ```shell
  cat /tmp/jenkins/home/secrets/initialAdminPassword
  ```
  


#### Jenkins initial setup
- Open your web browser and access Jenkins web ui via http://localhost:8082
- Paste the initial admin password you copied in the previous step.
- Install the recommended plugins
- Define the admin user and password
- Set the jenkins url to http://localhost:8082




#### Jenkins pipeline configuration
- Go to jenkins home page and click on **New Item**.
- Enter the item name , select **Pipeline** and click on **OK**.
- At the **Pipeline** section select **Pipeline script and paste script from [Jenkinsfile](Jenkinsfile) file.
- Click on **Save** button.
- Click on **Build Now** button to run the pipeline.

#### Results
- After the pipeline finished running you should see the following results :

  - In Jenkins:

    <img src="images/img_4.png" alt="Your Image Description" style="width: 75%;" />
    
  - In Dependency Track:  

    <img src="images/img_5.png" alt="Your Image Description" style="width: 75%;" />
  
  
### Another helpful links



