FROM python:3.7

#RUN apt-get update && apt-get upgrade -y
RUN apt-get update &&\
    # apt-get install python3.7 -y &&\
    apt-get install libpcap-dev libpq-dev -y &&\
    # apt-get install python3.7-dev libmysqlclient-dev -y &&\
    apt-get install python3-pip -y &&\
    apt-get install graphviz -y


#WORKDIR /usr/documents/hackathon/rooftop_solar_energy
WORKDIR /streamlit-docker

# Exposing default port for streamlit
EXPOSE 8501

# Install requirements
RUN pip3 install --upgrade setuptools
RUN pip3 install --upgrade pip
COPY requirements.txt ./
RUN pip install -r requirements.txt
# Copy necessary files
COPY . .
CMD streamlit run app.py


# streamlit-specific commands for config
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN mkdir -p /root/.streamlit
RUN bash -c 'echo -e "\
[general]\n\
email = \"\"\n\
" > /root/.streamlit/credentials.toml'