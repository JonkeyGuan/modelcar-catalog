# qwen3-8b

https://huggingface.co/Qwen/qwen3-8b

quay.io/modelcar/modelcar-catalog:qwen3-8b

## Building Image

This ModelCar build downloads the model locally then copies the files to a container in multiple layers to avoid podman memory issues.

### Downloading model files locally

```
mkdir -p ./modelcar-images/qwen/qwen3-8b/models
podman run --rm --platform linux/arm64 \
    -v ./modelcar-images/qwen/qwen3-8b/models:/models \
    --env-file modelcar-images/qwen/qwen3-8b/downloader.env \
    quay.io/modelcar/huggingface-downloader:latest
```

### Building the ModelCar Image

```
podman build -f modelcar-images/qwen/qwen3-8b/Containerfile modelcar-images/qwen/qwen3-8b \
    -t quay.io/modelcar/modelcar-catalog:qwen3-8b  \
    --platform linux/arm64
```

## Deploying Model

This model can be deployed using vLLM on OpenShift AI using the following Helm Chart.

```
helm repo add modelcar https://modelcar.github.io/helm-charts/
helm repo update modelcar
helm upgrade -i qwen3-8b modelcar/vllm-kserve \
    --values modelcar-images/qwen/qwen3-8b/values.yaml
```

For more information on the above Helm Chart, you can find the source code for that chart here:

https://github.com/modelcar/helm-charts/tree/main/charts/vllm-kserve
