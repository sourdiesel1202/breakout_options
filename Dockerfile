FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN ln -sf /usr/share/zoneinfo/America/New_York /etc/timezone && \
    ln -sf /usr/share/zoneinfo/America/New_York /etc/localtime && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get update

CMD ["waitress-serve", "--listen=*:5000", "wsgi:app"]