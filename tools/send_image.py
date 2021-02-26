import nsvision as nv
import numpy as np
from min_tfs_client.requests import TensorServingClient
from min_tfs_client.tensors import tensor_proto_to_ndarray

image = nv.imread('test_images/2216849948.jpg', resize=(512, 512), normalize=False)
image = nv.expand_dims(image, axis=0)

input = np.array(image.tolist())
input = np.float32(input)
print(type(input[0][0][0][0]))

client = TensorServingClient(host="127.0.0.1", port=8500, credentials=None)
response = client.predict_request(
    model_name="saved_model",
    model_version=1,
    input_dict={
        # These input keys are model-specific
        "conv2d_4_input": input
    },
)

print(response)
float_output = tensor_proto_to_ndarray(
    # This output key is model-specific
    response.outputs["dense_3"]
)

print(type(float_output[0][0]))