#!/bin/bash

PROJECT_ID=""
ARTIFACT_ID="alexandre-repository"
IMAGE_NAME="whatsapp-gateway-image"
CLOUD_RUN_SERVICE_NAME="alex-whatsapp-gateway"
VERSION="v1"
REGION="us-central1"
IMAGE="us-central1-docker.pkg.dev/$PROJECT_ID/$ARTIFACT_ID/$IMAGE_NAME:$VERSION"

echo "📌 Imagem sendo criada: $IMAGE"

echo "🔑 Autenticando no gcloud..."
gcloud config set project $PROJECT_ID
gcloud auth configure-docker $REGION-docker.pkg.dev
gcloud config set run/region $REGION

echo "🐳 Construindo a imagem Docker..."
docker build -t $IMAGE .

echo "🚀 Enviando a imagem para o Artifact Registry..."
docker push $IMAGE

echo "🌎 Fazendo deploy no Cloud Run..."
gcloud run deploy $CLOUD_RUN_SERVICE_NAME  \
    --image $IMAGE \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --set-env-vars DFCX_PROJECT_ID= \
    --set-env-vars DFCX_AGENT_ID= \
    --set-env-vars META_WA_PHONE_NUMBER_ID= \
    --set-env-vars META_WA_ACCESS_TOKEN= \
    --set-env-vars META_WA_VERIFY_TOKEN=
    
    --port 8080

echo "✅ Deploy concluído! API está rodando em:"
gcloud run services describe $CLOUD_RUN_SERVICE_NAME --region=$REGION --format="value(status.url)"
