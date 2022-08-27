FROM python

RUN apt-get update && apt-get install -y \ 
    python3 \
    python3-pip\
    python3-tk

COPY . /app

WORKDIR /app

COPY docker_req.txt docker_req.txt
RUN pip3 install -r docker_req.txt

ADD . /app

ENTRYPOINT ["python3"]

CMD ["steganography.py", "-i", "tests/cover_texts/songs/adele.docx", "-e", "-s", "tajnazprava.", "-b"] 
