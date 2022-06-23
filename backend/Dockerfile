FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /backend

COPY ./requirements.txt /backend/requirements.txt

COPY ./model_pkl /backend/model_pkl

RUN pip install -r requirements.txt

COPY . /backend

EXPOSE 8000

CMD ["python", "main.py"]