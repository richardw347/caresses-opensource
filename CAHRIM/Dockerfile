FROM ubuntu:16.04

ENV DEBIAN_FRONTEND noninteractive
ENV USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends ubuntu-desktop && \
    apt-get install -y gnome-panel gnome-settings-daemon metacity nautilus gnome-terminal && \
    apt-get install -y wget && \
    apt-get install -y tar

RUN apt-get install -y --no-install-recommends python \
    libx11-dev libxfixes-dev libxi-dev \
    libxcb1-dev libx11-xcb-dev libxcb-glx0-dev \
    libdbus-1-dev libxkbcommon-dev libxkbcommon-x11-dev \
    binutils g++ make zlib1g-dev libssl-dev \
    libgl1-mesa-dev xz-utils

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

RUN mkdir -p /opt/caresses/CAHRIM
COPY . /opt/caresses/CAHRIM
COPY caresses-conf.json /opt/caresses/
WORKDIR /opt/caresses/CAHRIM

RUN pip install -r requirements.txt

