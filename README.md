
# 🚀 IRIS API — FastAPI + Docker + GKE Continuous Deployment

This repository demonstrates how to build, containerize, and deploy a FastAPI-based IRIS classification API onto **Google Kubernetes Engine (GKE)** using **Docker**, **Artifact Registry**, and **GitHub Actions** for continuous deployment.

---

## 📘 Overview

**Tech Stack:**

* **FastAPI** — lightweight Python web framework for serving ML models
* **Docker** — containerization for consistent deployments
* **Google Artifact Registry** — image repository
* **Google Kubernetes Engine (GKE)** — orchestration and scaling
* **GitHub Actions** — automation for CI/CD

---

## 🧩 Stage 1: FastAPI Development

1. **Create a GitHub Repository**
   Initialize your repo and clone it locally.

2. **Create FastAPI Application**
   Example structure:

   ```
   iris-fast-api/
   ├── iris-fast-api.py
   ├── requirements.txt
   ```

3. **Run the API**

   ```bash
   uvicorn iris-fast-api:app --reload --host 0.0.0.0
   ```

4. **Test the Endpoint**

   ```bash
   curl -X POST "http://34.171.251.115:8000/predict" \
   -H "Content-Type: application/json" \
   -d "{\"sepal_length\":5.1, \"sepal_width\":3.5, \"petal_length\":1.4, \"petal_width\":0.2}"
   ```

   ✅ Expected Response:

   ```json
   {"prediction":["setosa"]}
   ```

---

## 🐳 Stage 2: Dockerization

1. **Enable Docker Permissions**

   ```bash
   sudo usermod -aG docker $USER
   newgrp docker
   ```

2. **Build the Docker Image**

   ```bash
   docker build -t iris-api .
   ```

3. **Verify Image ID**

   ```bash
   docker images
   ```

4. **Run the Container**

   ```bash
   docker run -d -p 8200:8200 iris-api
   ```

   Example container ID:

   ```
   4c02061ae05d324c7e544595b2f9365873c291f644fba9488dbba5660460728a
   ```

5. **Check Logs**

   ```bash
   docker logs 4c02061ae05d324c7e544595b2f9365873c291f644fba9488dbba5660460728a
   ```

6. **List Running Containers**

   ```bash
   docker ps
   ```

7. **Test Again**

   ```bash
   curl -X POST "http://34.171.251.115:8200/predict" \
   -H "Content-Type: application/json" \
   -d "{\"sepal_length\":5.1, \"sepal_width\":3.5, \"petal_length\":1.4, \"petal_width\":0.2}"
   ```

   ✅ Expected Response:

   ```json
   {"prediction":["setosa"]}
   ```

---

## 🧱 Stage 3: Pushing to Google Artifact Registry & Deploying to GKE

1. **Create Artifact Registry Repository**

   ```bash
   gcloud artifacts repositories create iris-repo \
     --repository-format=docker \
     --location=us-central1 \
     --description="Docker Repo for ML models"
   ```

2. **Configure Docker Authentication**

   ```bash
   gcloud auth configure-docker us-central1-docker.pkg.dev
   ```

3. **Tag Image for Artifact Registry**

   ```bash
   docker tag iris-api us-central1-docker.pkg.dev/mlops-ga-474200/iris-repo/iris-api:latest
   ```

4. **Push Image to Artifact Registry**

   ```bash
   docker push us-central1-docker.pkg.dev/mlops-ga-474200/iris-repo/iris-api:latest
   ```

5. **Create GKE Cluster**

   ```bash
   gcloud container clusters create iris-gke-cluster \
     --zone us-central1 \
     --num-nodes=1
   ```

6. **Deploy Workload from Artifact Registry**

   * In Google Cloud Console → Kubernetes → Workloads → Deploy from Container Image
     or
   * Via CLI:

     ```bash
     gcloud container clusters get-credentials iris-gke-cluster --zone us-central1 --project mlops-ga-474200
     kubectl apply -f k8s/deployment.yaml
     kubectl apply -f k8s/service.yaml
     ```

7. **Verify Pods and Services**

   ```bash
   kubectl get pods
   kubectl get service
   ```

8. **Adjust Service Port Mapping**

   ```bash
   kubectl edit service deployment-1-iris-service
   ```

   Change:

   ```yaml
   ports:
     - port: 80
       targetPort: 8200
   ```

9. **Test Deployed API**

   ```bash
   curl -X POST "http://136.114.80.150:80/predict" \
   -H "Content-Type: application/json" \
   -d "{\"sepal_length\":5.1, \"sepal_width\":3.5, \"petal_length\":1.4, \"petal_width\":0.2}"
   ```

   ✅ Expected Response:

   ```json
   {"prediction":["setosa"]}
   ```

---

## ⚙️ Stage 4: Continuous Deployment via GitHub Actions

1. **Add GitHub Actions Workflow**

   * Create `.github/workflows/deploy.yml`

2. **Add Kubernetes Manifests**

   * `k8s/deployment.yaml`
   * `k8s/service.yaml`

   These will be used by GitHub Actions to update your GKE deployment automatically.

---

## ✅ Verification

Once the GitHub Actions pipeline runs successfully:

* Docker image will be built and pushed to Artifact Registry.
* Kubernetes deployment will be updated with the new image.
* The API will be accessible via the external IP from GKE.

Example test:

```bash
curl -X POST "http://<EXTERNAL_IP>:80/predict" \
-H "Content-Type: application/json" \
-d "{\"sepal_length\":5.1, \"sepal_width\":3.5, \"petal_length\":1.4, \"petal_width\":0.2}"
```

---

## 🧠 Notes & Best Practices

* Always expose the FastAPI app on `0.0.0.0` inside the container.
* Ensure `containerPort` in deployment matches your `targetPort` in service.
* Store your GCP credentials JSON securely as a GitHub secret.
* Use region-specific registry paths (e.g., `us-central1-docker.pkg.dev`).

---

## 📦 Outputs

* **Artifact Registry Image:**
  `us-central1-docker.pkg.dev/mlops-ga-474200/iris-repo/iris-api:latest`
* **Kubernetes Deployment:** `iris-deployment`
* **Kubernetes Service:** `iris-service`
* **Public Endpoint:** `http://<EXTERNAL_IP>:80/predict`

---
