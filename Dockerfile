FROM ubuntu:20.04

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/

RUN apt-get update -y \
&& apt-get install -y software-properties-common \
&& add-apt-repository ppa:deadsnakes/ppa \
&& apt-get install openjdk-8-jdk -y \
&& apt-get install python3-pip -y \
&& export JAVA_HOME \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*


ARG GOOGLE_SECRET

RUN apt-get -yyy update && apt-get -yyy install software-properties-common

COPY requirements.txt requirements.txt
RUN pip install anvil-app-server
RUN pip install -r requirements.txt
RUN anvil-app-server || true

VOLUME /apps
WORKDIR /apps

COPY FinancialShitApp FinancialShitApp
RUN mkdir /anvil-data

COPY lessons lessons

RUN useradd anvil
RUN useradd python
RUN chown -R anvil:anvil /anvil-data
USER anvil

EXPOSE 6061

ENTRYPOINT ["anvil-app-server", "--data-dir", "/anvil-data", "--port", "6061"]
CMD ["--app", "FinancialShitApp", "--google-client-id", "993595845237-q5llasdn2l27h6rk1p18rancmpf8gdhm.apps.googleusercontent.com", "--google-client-secret", "$GOOGLE_SECRET"]
