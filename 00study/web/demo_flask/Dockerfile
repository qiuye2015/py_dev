# docker build -t fjp-app:latest .

# docker run --name fjp-app -d -p 8000:5000 \
# -e SECRET_KEY=57d40f677aff4d8d96df97223c74d217 \
# -e MAIL_USERNAME=<your-gmail-username> \
# -e MAIL_PASSWORD=<your-gmail-password> fjp-app:latest

# docker exec -it fjp-app sh
# docker login
# docker tag flasky:latest <your-dockerhub-username>/flasky:latest
# docker push <your-dockerhub-username>/flasky:latest
# docker run --name flasky -d -p 8000:5000 <your-dockerhub-username>/flasky:latest

FROM python:3.8-alpine

ENV FLASK_APP app.py
ENV FLASK_CONFIG production

RUN adduser -D fjp
USER fjp

WORKDIR /home/fjp

COPY requirements requirements
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY apps apps
COPY migrations migrations
COPY flasky.py config.py boot.sh ./

# run-time configuration
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
