FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install flask PyJWT
EXPOSE 5001
CMD ["python", "app.py"]