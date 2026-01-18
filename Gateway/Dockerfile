FROM python:3.12.1

WORKDIR /app/WrapperAPI

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8000

EXPOSE 8000
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]


