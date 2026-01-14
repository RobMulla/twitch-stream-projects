import kagglehub

# Download latest version
path = kagglehub.dataset_download("robikscube/mrbeast-youtube-stats-daily")

print("Path to dataset files:", path)
