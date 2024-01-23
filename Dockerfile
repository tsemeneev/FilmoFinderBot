FROM joyzoursky/python-chromedriver:latest

WORKDIR /src
COPY requirements.txt /src
RUN pip install -r requirements.txt

COPY . /src

CMD ["python", "bot.py"]