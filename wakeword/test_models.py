from openwakeword.model import Model

model = Model(inference_framework="onnx")

print(model.models.keys())