FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt amqp.reqs.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r amqp.reqs.txt
COPY ./payment.py ./log_template.py ./amqp_setup.py  ./
RUN mkdir ~/paypalpayoutssdk
COPY ./paypalpayoutssdk ./paypalpayoutssdk
CMD [ "python", "./payment.py" ]