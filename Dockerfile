FROM python:3.6

COPY . /jtpl
WORKDIR /jtpl
RUN pip install -r requirements.txt
RUN python setup.py install
