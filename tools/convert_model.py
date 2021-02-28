import tensorflow as tf

model = tf.keras.models.load_model('./model/best-model.h5')
export_path = './model/1'

tf.saved_model.save(
    model,
    export_path)