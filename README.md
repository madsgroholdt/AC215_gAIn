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
│   │   │   ├── data_preprocessing
│   │   │   │   ├── csv_data/
│   │   │   │   ├── txt_data/
│   │   │   │   ├── templates
│   │   │   │   │   └── index.html
│   │   │   │   ├── Dockerfile
│   │   │   │   ├── Pipfile
│   │   │   │   ├── Pipfile.lock
│   │   │   │   ├── docker-shell.sh
│   │   │   │   ├── docker-entrypoint.sh
│   │   │   │   ├── env.dev
│   │   │   │   ├── cli.py
│   │   │   │   ├── redirect.py
│   │   │   │   ├── strava_api.py
│   │   │   │   ├── csv_to_txt.py
│   │   │   │   ├── flask_app.py
│   │   │   │   └── README.md
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

### Milestone 5
In this milestone, we deploy the fully-functional gAIn app to a Kubernetes cluster.

### Prerequisites

1. **Secrets Folders:**
   - Ensure you have a `secrets` folder in the directory `AC215_gAIn/src`.
       - This folder should contain the file `llm-service-account.json`.
   - Ensure you have another `secrets` folder at the same level as `AC215_gAIn`.
       - This folder should contain the files `deployment.json` and `gcp-service.json`

2. **APIs**
   - Enable the following APIs in your GCP console:
       - Compute Engine API
       - Service Usage API
       - Cloud Resource Manager API
       - Google Container Registry API
       - Kubernetes Engine API

### Setup Instructions

1. Change your working directory to `AC215_gAIn/src/deployment`.

2. Start and enter the container by running:
   ```bash
   sh docker-shell.sh
   ```

3. If you need to push the images to Google Cloud (for the first time or to update them), run:
   ```bash
   ansible-playbook deploy-docker-images.yml -i inventory.yml
   ```
   - This will build and push the `gain-vector-db-cli`, `gain-api-service`, and `gain-frontend` images
   - *NOTE: This step is **not** required if your containers are already up-to-date and in your artifact registry*

4. Create and deploy the cluster by running:
   ```bash
   ansible-playbook deploy-k8s-cluster.yml -i inventory.yml --extra-vars cluster_state=present
   ```

5. View the app and explore gAIn by going to `http://<YOUR INGRESS IP>.sslip.io`
   - Copy `nginx_ingress_ip` from the terminal

---
