FROM python:3.6

COPY . /yajinja
WORKDIR /yajinja
RUN pip install -r requirements.txt
RUN python setup.py install
