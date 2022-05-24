FROM pandoc/minimal:2.18-ubuntu

RUN ln -snf /usr/share/zoneinfo/Etc/UTC /etc/localtime \
    && echo "Etc/UTC" > /etc/timezone
RUN apt-get update
RUN apt-get install -y texlive-full
