FROM python:3.13
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 9999
CMD ["python", "gate.py"]
