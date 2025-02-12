FROM python:3.13
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 8081
CMD ["python", "bot.py"]
