FROM ubuntu:16.04

ENV DEBIAN_FRONTEND noninteractive
ENV USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends ubuntu-desktop && \
    apt-get install -y gnome-panel gnome-settings-daemon metacity nautilus gnome-terminal && \
    apt-get install -y tightvncserver && \
    apt-get install -y wget && \
    apt-get install -y tar && \
    mkdir /root/.vnc

# Install Choregraphe Suite 2.5.5.5
RUN wget -P /root/ https://community-static.aldebaran.com/resources/2.5.5/Choregraphe/choregraphe-suite-2.5.5.5-linux64-setup.run
RUN chmod +x /root/choregraphe-suite-2.5.5.5-linux64-setup.run
RUN /root/choregraphe-suite-2.5.5.5-linux64-setup.run --mode unattended --installdir /opt/Aldebaran --licenseKeyMode evaluation
RUN rm /root/choregraphe-suite-2.5.5.5-linux64-setup.run

# Install pynaoqi 2.5.5.5 library
RUN wget -P /root/ https://community-static.aldebaran.com/resources/2.5.5/sdk-python/pynaoqi-python2.7-2.5.5.5-linux64.tar.gz
RUN tar -xvzf /root/pynaoqi-python2.7-2.5.5.5-linux64.tar.gz -C /root/
RUN rm /root/pynaoqi-python2.7-2.5.5.5-linux64.tar.gz
ENV PYTHONPATH /root/pynaoqi-python2.7-2.5.5.5-linux64/lib/python2.7/site-packages
ENV LD_LIBRARY_PATH /opt/Aldebaran/lib/


RUN apt-get install -y python-pip python-pyaudio python-numpy python-mysql.connector python-tk python-matplotlib

# RUN pip install pexpect glob2 beautifulsoup4==4.9.3 requests==2.2.1 isodate nltk==3.4.5 colorama paramiko==1.18.3 matplotlib==2.1.1 feedparser==4.1

RUN mkdir -p /opt/caresses
COPY . /opt/caresses