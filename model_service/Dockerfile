FROM tensorflow/serving

RUN mkdir ./models/saved_model
COPY ./model/ ./models/saved_model/

ENTRYPOINT ["/usr/bin/tf_serving_entrypoint.sh"]