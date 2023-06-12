FROM tensorflow/tensorflow:latest-gpu as base
FROM base as builder
RUN mkdir /wheels
COPY wheels /wheels
RUN mkdir /install
COPY requirements.txt /install
RUN pip3 install --no-index --find-links=/wheels -r /install/requirements.txt
FROM base as app
#COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/ /usr/