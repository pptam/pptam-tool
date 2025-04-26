for dir in $(find . -maxdepth 2 -type f -name Dockerfile -exec dirname {} \;); do
  echo "Building Docker image in directory: $dir"
  IMAGE_NAME=$(basename "$dir")
  docker build -t 10.10.10.240/library/$IMAGE_NAME:latest "$dir"
  docker push 10.10.10.240/library/$IMAGE_NAME:latest
 done
