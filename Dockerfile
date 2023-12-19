FROM python:bookworm
WORKDIR /app
COPY . .

RUN pip install gunicorn
RUN pip install flask

CMD [ "gunicorn", "--bind", "0.0.0.0:8891", "wsgi:app" ]

EXPOSE 8891