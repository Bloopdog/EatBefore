FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt amqp.reqs.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r amqp.reqs.txt
COPY ./notification.py ./log_template.py ./amqp_setup.py ./
CMD [ "python", "./notification.py" ]