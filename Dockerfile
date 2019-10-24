FROM alpine:3.7

RUN apk add --no-cache python3-dev \
    && apk add --no-cache gcc \
    && apk add --no-cache musl-dev \
    && pip3 install --upgrade pip
# Create a dir in the image    
WORKDIR /app
# copy the source code to the image
COPY . /app

RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python3"]

CMD ["entry_docker.py"]