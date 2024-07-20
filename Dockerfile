FROM python:3.11

WORKDIR /apps

COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache -r requirements.txt

COPY . .

EXPOSE 81

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "81", "--reload"]
