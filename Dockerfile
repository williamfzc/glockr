FROM python:3-alpine

# dep
RUN apk add --no-cache gcc make g++

# glockr package, splited for cache usage
RUN pip install glockr==0.1.1

EXPOSE 9410

CMD ["python", "-m", "glockr.server"]
