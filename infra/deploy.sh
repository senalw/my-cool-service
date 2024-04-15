#!/bin/bash

set -e  # Exit immediately if a command fails

# Check for required tools
check_command() {
  if ! command -v "$1" &> /dev/null; then
    echo "$1 not found. Please install $1."
    exit 1
  fi
}

check_command docker
check_command kubectl
check_command terraform

# Generate certificates
./generate_certificates.sh

# Build Docker image
cd ../ && docker build -t my-cool-service:latest -f Dockerfile . && cd infra

# Check Docker image build status
echo "my-cool-service:latest built successfully"

# Start Minikube with Docker driver
minikube start --driver=docker

# Wait for Minikube cluster to come online
sleep 30

# Verify Minikube cluster status
minikube status

# Check if Minikube cluster started successfully
if [[ $(minikube status | grep "Running" | wc -l) -eq 0 ]]; then
  echo "Minikube cluster failed to start."
  exit 1
fi

echo "Minikube cluster started successfully (using Docker driver)!"

# Change kubectl context to Minikube
kubectl config use-context minikube

# Load build my-cool-service:latest docker image
minikube image load my-cool-service:latest

# Initialize Terraform
terraform init

# Apply Terraform configuration
terraform apply -auto-approve

# Log success message
echo "Cluster created successfully"

# Perform port forwarding (run in background)
kubectl port-forward service/swisscom-cool-service 8010:8010 &

# Log port forwarding information
echo "Port forwarding set up. Access your service at http://localhost:8010/docs"
