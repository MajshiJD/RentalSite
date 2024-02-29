FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /code

ENV DockerHOME=/code

COPY requirments.txt .

RUN pip install -r requirments.txt

COPY . .

EXPOSE 8000  

CMD ["python", "manage.py","runserver","0.0.0.0:8000"]

