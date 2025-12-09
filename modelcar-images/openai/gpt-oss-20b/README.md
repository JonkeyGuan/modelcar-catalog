# gpt-oss-20b

https://huggingface.co/openai/gpt-oss-20b

quay.io/modelcar/modelcar-catalog:gpt-oss-20b

## Building Image

This ModelCar build downloads the model locally then copies the files to a container in multiple layers to avoid podman memory issues.

### Downloading model files locally

```
mkdir -p ./modelcar-images/openai/gpt-oss-20b/models
podman run --rm --platform linux/arm64 \
    -v ./modelcar-images/openai/gpt-oss-20b/models:/models \
    --env-file modelcar-images/openai/gpt-oss-20b/downloader.env \
    quay.io/modelcar/huggingface-downloader:latest
```

### Building the ModelCar Image

```
podman build -f modelcar-images/openai/gpt-oss-20b/Containerfile modelcar-images/openai/gpt-oss-20b \
    -t quay.io/modelcar/modelcar-catalog:gpt-oss-20b  \
    --platform linux/arm64
```

## Deploying Model

This model can be deployed using vLLM on OpenShift AI using the following Helm Chart.

```
helm repo add modelcar https://modelcar.github.io/helm-charts/
helm repo update modelcar
helm upgrade -i gpt-oss-20b modelcar/vllm-kserve \
    --values modelcar-images/openai/gpt-oss-20b/values.yaml
```

For more information on the above Helm Chart, you can find the source code for that chart here:

https://github.com/modelcar/helm-charts/tree/main/charts/vllm-kserve
