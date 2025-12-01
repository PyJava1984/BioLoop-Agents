#!/bin/bash

PROJECT="YOUR_PROJECT"
REGION="us-central1"

deploy() {
  SERVICE=$1
  DIRECTORY=$2

  gcloud builds submit $DIRECTORY --tag gcr.io/$PROJECT/$SERVICE

  gcloud run deploy $SERVICE \
      --image gcr.io/$PROJECT/$SERVICE \
      --platform managed \
      --region $REGION \
      --allow-unauthenticated
}

deploy "careflow-agent" "./agents/careflow"
deploy "medcycler-agent" "./agents/medcycler"
deploy "enersense-agent" "./agents/enersense"
deploy "greenrisk-agent" "./agents/greenrisk"
