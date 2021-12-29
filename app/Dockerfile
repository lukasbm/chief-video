FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

COPY . .

EXPOSE 5000
CMD gunicorn --workers=3 -b 0.0.0.0:5000 --log-level debug app:app
# CMD python3 -m flask run --host=0.0.0.0
