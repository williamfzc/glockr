FROM python:3-alpine

RUN apk add --no-cache gcc make g++ \
    && pip install glockr==0.1.2 \
    && apk del gcc make g++

EXPOSE 9410

CMD ["python", "-m", "glockr.server"]
