# qwen3-4b

https://huggingface.co/Qwen/Qwen3-4B

quay.io/modelcar/modelcar-catalog:qwen3-4b

### Downloading model files locally

```
mkdir -p ./modelcar-images/qwen/qwen3-4b/models
podman run --rm --platform linux/arm64 \
    -v ./modelcar-images/qwen/qwen3-4b/models:/models \
    --env-file modelcar-images/qwen/qwen3-4b/downloader.env \
    quay.io/modelcar/huggingface-downloader:latest
```

## Building Image

```
podman build -f modelcar-images/qwen/qwen3-4b/Containerfile modelcar-images/qwen/qwen3-4b \
    -t quay.io/modelcar/modelcar-catalog:qwen3-4b  \
    --platform linux/arm64
```

## Deploying Model

This model can be deployed using vLLM on OpenShift AI using the following Helm Chart.

```
helm repo add modelcar https://modelcar.github.io/helm-charts/
helm repo update modelcar
helm upgrade -i qwen3-4b modelcar/vllm-kserve \
    --values modelcar-images/qwen/qwen3-4b/values.yaml
```

For more information on the above Helm Chart, you can find the source code for that chart here:

https://github.com/modelcar/helm-charts/tree/main/charts/vllm-kserve
