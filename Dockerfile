FROM python:3.10

# Add the MySQL repository
RUN apt-get update && apt-get install -y gnupg2
RUN wget -O /etc/apt/trusted.gpg.d/mysql.gpg https://repo.mysql.com/RPM-GPG-KEY-mysql
RUN echo "deb http://repo.mysql.com/apt/debian/ bullseye mysql-8.0" > /etc/apt/sources.list.d/mysql.list

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
