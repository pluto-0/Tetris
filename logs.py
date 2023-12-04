import tensorflow as tf

class CustomTensorBoard(tf.keras.callbacks.TensorBoard):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.writer = tf.summary.create_file_writer(self.log_dir)

    def set_model(self, model):
        self.model = model

    def log(self, step, **stats):
        with self.writer.as_default():
            for key, value in stats.items():
                tf.summary.scalar(key, value, step=step)
            self.writer.flush()