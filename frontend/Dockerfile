FROM python:3.7-slim

WORKDIR /frontend

COPY requirements.txt /frontend

RUN pip install -r requirements.txt

COPY . /frontend

EXPOSE 8501

CMD ["streamlit", "run", "ui.py"]