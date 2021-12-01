FROM python:3.9

# set display port to avoid crash
ENV DISPLAY=:99

# upgrade pip
RUN pip install --upgrade pip

WORKDIR /currency_client

COPY . ./

RUN pip install -r requirements.txt
