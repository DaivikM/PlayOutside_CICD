# 🌤️ Play Outside Predictor

A machine learning-based web app that predicts whether you can play outside based on weather conditions. Built using **FastAPI** for backend APIs and **Streamlit** for the frontend UI. Integrated with **Docker**, **GitHub Actions**, and **Render** for CI/CD and deployment.

[View Deployment](https://play-ui-048l.onrender.com)

---

## 🚀 Project Overview

- **Model**: Decision Tree trained on weather data.
- **Backend**: FastAPI for prediction API (`/predict`)
- **Frontend**: Streamlit UI interacting with FastAPI API
- **CI/CD**: GitHub Actions to run tests and build Docker images
- **Deployment**: Dockerized containers pushed to Docker Hub and deployed to Render

---

## 🧪 Local Development & Testing

### 1. Clone the Repository

```bash
git clone https://github.com/DaivikM/PlayOutside_CICD.git
cd play-outside-PlayOutside_CICD
````

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Locally

#### Run API:

```bash
uvicorn api:app --reload
```

#### Run UI:

```bash
streamlit run ui.py
```

Or run both together:

```bash
python app.py
```

### 4. Run Tests

```bash
pytest tests/
```

Tests will:

* Check if model & encoders exist
* Verify predictions
* Ensure accuracy > 60%
* Validate error handling

---

## 🐳 Docker Setup

### 1. Build Images Locally

```bash
docker build -t daivikmohan/play-api -f Dockerfile.api .
docker build -t daivikmohan/play-ui -f Dockerfile.ui .
```

### 2. Run Using Docker Compose

```bash
docker-compose up
```

---

## 🔄 CI/CD with GitHub Actions

### `.github/workflows/cicd.yml`

* On push to `main`:

  1. Run tests
  2. If successful:

     * Build Docker images
     * Push to Docker Hub

Make sure to add these GitHub Secrets:

* `DOCKER_USERNAME`
* `DOCKER_PASSWORD`

---

## ☁️ Deployment on Render

### 1. Push Docker Images to Docker Hub

Done automatically through CI/CD pipeline.

### 2. Create Render Services

* **API**

  * Type: Web Service
  * Docker: Use your Docker Hub image (`play-api`)
  * Start Command: Render will auto-detect
  * Get the API URL, e.g., `https://play-api-xxxxx.onrender.com`

* **UI**

  * Type: Web Service
  * Docker: Use your Docker Hub image (`play-ui`)
  * Set API URL inside `ui.py`:

    ```python
    API_URL = "https://play-api-xxxxx.onrender.com/predict/"
    ```

---

## 🧠 Model Details

* Trained on weather dataset
* Label encoded all categorical features
* Saved model & encoders with `pickle`
* Accuracy & metrics logged in `metrics.json`

---

## 📈 Example Usage

```json
POST /predict
{
  "Outlook": "Sunny",
  "Temperature": "Cool",
  "Humidity": "Normal",
  "Windy": "Weak"
}
```

Returns:

```json
{
  "Prediction": "Yes"
}
```

---

## 🔒 Security

* No sensitive secrets are stored in code
* CI/CD builds and deploys only after successful tests

---

## 🙌 Acknowledgements

* Built using [FastAPI](https://fastapi.tiangolo.com/)
* UI with [Streamlit](https://streamlit.io/)
* CI/CD with [GitHub Actions](https://github.com/features/actions)
* Deployed on [Render](https://render.com)

---
