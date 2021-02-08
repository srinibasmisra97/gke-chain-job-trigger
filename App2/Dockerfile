FROM python
RUN mkdir /app
COPY ./service.py /app
COPY ./requirements.txt /app
COPY ./gke-chain-job-trigger.json /
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
ENV GOOGLE_APPLICATION_CREDENTIALS=/gke-chain-job-trigger.json
CMD [ "python", "service.py" ]