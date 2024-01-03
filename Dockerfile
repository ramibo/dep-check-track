# use jsk11 version as webgoat 8.1.0 maven-compiler plugin requires jdk11
FROM jenkins/jenkins:jdk11

USER root

RUN apt-get update
RUN apt-get --yes --allow-downgrades install curl vim telnet wget maven python3 python3-pip python3-venv
RUN ln -s /usr/bin/python3 /usr/bin/python

RUN java -version

# Copy requirements file
COPY ./requirements.txt /code/requirements.txt

## Install Python dependencies while still as root
#WORKDIR /code
#RUN python -m venv /code/venv && \
#    /code/venv/bin/pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of the codebase into the image
COPY ./bom-convert.py /code/bom-convert.py


RUN chown -R jenkins /code
RUN chmod -R 777 /code
RUN chown -R jenkins /var/jenkins_home


RUN mkdir /tmp/folder_to_scan
RUN chown -R jenkins /tmp/folder_to_scan

RUN chmod 777 /tmp


# Switch back to the Jenkins user
USER jenkins

