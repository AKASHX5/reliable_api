# Step 1: Start Minikube
minikube start

# Step 2: Configure Docker to Use Minikube's Docker Daemon
eval $(minikube docker-env)

# Step 3: Build Docker Image inside Minikube
docker build -t reliable_api:latest .

docker ps
# Step 4: Apply Configuration Files
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# Step 5: Verify the Deployment
kubectl get deployments
kubectl get pods
kubectl get services

# Step 6: Access the Application
minikube service reliable-api-service
#this will open the url in browser.