### gAIn Milestone 4 Organization

Below is an overview of the gAIn source code repository.

```
├── README.md
├── reports
│   ├── Planning and Components.pdf
│   └── Milestone 1.pdf
|   └── Milestone 3.pdf
└── src
│   ├── api_service
│   │   ├── api
│   │   │   ├── routers
│   │   │   │   └── llm_rag_chat.py
│   │   │   └── utils
│   │   │   │   ├── chat_utils.py
│   │   │   │   ├── llm_rag_utils.py
│   │   │   └── service.py
│   │   ├── Dockerfile
│   │   ├── Pipfile
│   │   ├── Pipfile.lock
│   │   ├── docker-entrypoint.sh
│   │   ├── docker-shell.sh
│   ├── data_preprocessing
│   │   ├── Dockerfile
│   │   ├── Pipfile
│   │   ├── Pipfile.lock
│   │   ├── docker-shell.sh
│   │   ├── env.dev
│   │   ├── cli.py
│   │   ├── redirect.py
│   │   ├── strava_api.py
│   │   ├── csv_to_txt.py
│   │   ├── README.md
│   ├── data_scraping
│   │   ├── Dockerfile
│   │   ├── Pipfile
│   │   ├── Pipfile.lock
│   │   ├── docker-shell.sh
│   │   ├── find_urls.py
│   │   ├── scrape.py
│   │   ├── send_to_bucket.py
│   │   └── README.md
│   ├── dataset_creator
│   │   ├── Dockerfile
│   │   ├── Pipfile
│   │   ├── Pipfile.lock
│   │   ├── env.dev
│   │   ├── docker-shell.sh
│   │   ├── cli.py
│   │   └── README.md
│   ├── model_finetuner
│   │   ├── Dockerfile
│   │   ├── Pipfile
│   │   ├── Pipfile.lock
│   │   ├── env.dev
│   │   ├── docker-shell.sh
│   │   ├── cli.py
│   │   └── README.md
│   ├── docker-compose.yml
│   ├── frontend_react
│   ├── models
│   │   ├── Dockerfile
│   │   ├── docker-shell.sh
│   │   ├── infer_model.py
│   │   ├── model_rag.py
│   │   └── train_model.py
│   ├── vector_db
│   │   ├── Dockerfile
│   │   ├── Pipfile
│   │   ├── Pipfile.lock
│   │   ├── cli.py
│   │   ├── docker-compose.yml
│   │   ├── docker-entrypoint.sh
│   │   ├── docker-shell.sh
│   │   └── semantic_splitter.py
├── test_runner
│   ├── Dockerfile
│   ├── Pipfile
│   ├── Pipfile.lock
│   └── README.md
└── tests
    ├── integration_tests
    │   └── test_data_preprocessing.py
    └── test_semantic_splitter.py
```

# AC215 - gAIn

**Team Members**
Vincent Hock, Tomas Arevalo, Jake Carmine Pappo, Mads Groeholdt

**Group Name**
gAIn - The future of health and fitness

**Project**
With the gAIn application, we seek to fill an existing gap in the health and fitness industry by providing users with an affordable, knowledgeable, and context-aware AI-enabled personal trainer. Our trainer seeks to replace expensive, thin-stretched personal trainers and fitness coaches, and provides an easier solution for those seeking to educate themselves compared to relying on the internet's scathered, unverified information. The main functionality of the app is a chat interface with the intelligent assistant, where users can ask their coach for advice, training plans, and more. The coach improves on other LLM's in the area of health and fitness by both being fine-tuned on quality-checked expert resources, as well as having access to each user's historical activity and fitness data powered by an AI-agent.

---

### Milestone 4

In this milestone, we have the components for the backend (i.e., our LLM-RAG model), the back-end API service, and the front-end web app. Also included are components from previous milestones, such as data storage and versioning.

After building a robust ML Pipeline in our previous milestone, we have now built a backend api service and frontend app. This will be our user-facing application that ties together the various components built in previous milestones.

**Application Design**

Before we start implementing the app we built a detailed design document outlining the application’s architecture. We built a Solution Architecture and Technical Architecture to ensure all our components work together.

Here is our Solution Architecture:

<img src="images/solution-arch.png"  width="800">

Here is our Technical Architecture:

<img src="images/technical-arch.png"  width="800">

**Backend API**

We built a backend API service using FastAPI to expose model functionality to the frontend. We also added APIs that will help the front-end display some key information about the model and data. As seen below, this routes output from our back-end (e.g., LLM-generated text) to the user-facing front-end application.

<img src="images/api_list.png"  width="800">

**Frontend**

A user-friendly React app was built to allow users to interact with their personalized LLM-RAG model from the backend. In the app, the user can ask their AI personal trainer about anything health- and fitness-related, and they can also get specific insights and advice on their own personal data (e.g., from Strava). There is also a newsletters section that allows users to access and read primary source material, much of which contributes to the knowledge base for gAIn's fine-tuned LLM.

Here are some screenshots of our app:
<img src="images/gain_home.png"  width="800">

<img src="images/new_chat.png"  width="800">

<img src="images/gain_convo.png"  width="800">

## gAIn Application Setup Guide

Follow these steps to get the application up and running locally.

---

### Prerequisites

1. **Secrets Folder:**

   - Ensure you have a `secrets` folder in the directory `AC215_gAIn/src`.
   - This folder should contain the file `llm-service-account.json`.

2. **Directory Structure:**
   - Navigate to `AC215_gAIn/src` where you will find the following folders:
     - `vector_db`
     - `api_service`
     - `frontend_react`

---

### Setup Instructions

#### 1. Prepare the Vector Database

1. Change your working directory to the `vector_db` folder.

2. Start the container by running:

   ```bash
   sh docker-shell.sh

   ```

3. Inside the container, preprocess the user data by running:
   ```bash
   python cli.py --preprocess
   ```
   - This downloads the data from GCS, then chunks, embeds, and uploads it to ChromaDB
   - The default chunking method is `recursive-split`, but you can also try semantic splitting by adding `--chunk_type semantic-split`

#### 2. Start the Backend API Service

1. Open a **new terminal** and navigate to the `api_service` folder.

2. Start the docker container by running:

   ```bash
   sh docker-shell.sh

   ```

3. Inside the container, expose the backend API server:
   ```bash
   uvicorn_server
   ```

#### 3. Start the Frontend Web Application

1. Open another **new terminal** and navigate to the `frontend_react` folder.

2. Start the docker container by running:

   ```bash
   sh docker-shell.sh

   ```

3. (Optional) If this is your first time setting up the application, install the necessary dependencies:

   ```bash
   npm install

   ```

4. Start the local development server:
   ```bash
   npm run dev
   ```

---

### Accessing the Application

- Open your browser and navigate to:
  **[http://localhost:3000/](http://localhost:3000/)**

- Explore the features:
  1. **Home Page:** Learn about gAIn and its mission.
  2. **Newsletters Page:** Explore articles and blogs (content pending).
  3. **AI Chat Assistant:**
     - Chat with gAIn about health and fitness topics.
     - gAIn has access to Mads’s Strava data for personalized recommendations and insights.

## Pushing Dockerfile to Google Cloud Artifact Registry

Add the below `docker-push.sh` file to a folder that has the Dockerfile for the image you want to add to the project's artifact registry.

```sh
#!/bin/bash
set -e

PROJECT_ID="ac215-final-project"
REGION="us-central1"
REPO_NAME="gcf-artifacts"
IMAGE_NAME="image-name" # Put your image name here

# Tag the image for Artifact Registry
docker build -t $IMAGE_NAME .
docker tag $IMAGE_NAME $REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME

# Push the image to Artifact Registry
docker push $REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME
```

Then run `sh docker-push.sh` to build the image and add it to the registry.

---
