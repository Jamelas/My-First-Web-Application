FROM python:latest
WORKDIR /src
COPY . .

RUN pip install requests

RUN rm -r .git
RUN rm -r .gitignore
RUN rm -r data/.gitignore

CMD python main.py