FROM python:3.8
EXPOSE 8090
EXPOSE 8091
EXPOSE 8092
EXPOSE 8093
EXPOSE 8094
WORKDIR app/
COPY requirements.txt /app
RUN python -m pip install --upgrade pip && \
 python -m pip install -r requirements.txt && \
 mkdir -p /var/log/supervisor && \
 mkdir -p /etc/supervisor/conf.d && \
 mkdir -p /var/log/app
COPY ./src /app
COPY ./conf/supervisord.conf /etc/supervisor
CMD /usr/local/bin/supervisord