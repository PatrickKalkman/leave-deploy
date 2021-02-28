FROM tensorflow/serving:2.4.1

# Add Tini
ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--"]

RUN mkdir ./models/saved_model
COPY ./model/ ./models/saved_model/

CMD ["/usr/bin/tf_serving_entrypoint.sh"]