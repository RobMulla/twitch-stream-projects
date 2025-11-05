PROJECT_ID=twitch-streaming-476615
ZONE=europe-west4-a

gcloud compute tpus tpu-vm list \
    --project=$PROJECT_ID \
    --zone=$ZONE
