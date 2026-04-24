FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install flask PyJWT
RUN pip install -r requirements.txt
EXPOSE 5002
CMD ["python", "app.py"]
ENV PYTHONUNBUFFERED=1