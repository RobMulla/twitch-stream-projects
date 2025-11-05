PROJECT_ID=twitch-streaming-476615
ZONE=europe-west4-a
TPU_NAME=rob-twitch-tpu

gcloud compute tpus tpu-vm ssh $TPU_NAME \
    --project=$PROJECT_ID \
    --zone=$ZONE
