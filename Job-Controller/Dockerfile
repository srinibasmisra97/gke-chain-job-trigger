FROM python
RUN mkdir -p /app
COPY ./ /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "controller.py" ]