FROM python:3.10.7-slim
WORKDIR /user/cpb/Desktop/weather/app
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000","--reload"]