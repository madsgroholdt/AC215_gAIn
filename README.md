## gAIn Milestone 4

```
Below is an overview of the gAIn source code repository.
```

#### gAIn Milestone 4 Organization

```
├── Readme.md
├── reports
│   ├── CheesyAppMidterm.pdf
│   └── Milestone 1.pdf
|   └── Milestone 3.pdf
└── src
    ├── api-service
    ├── datapipeline
    │   ├── Dockerfile
    │   ├── Pipfile
    │   ├── Pipfile.lock
    │   ├── dataloader.py
    │   ├── docker-shell.sh
    │   ├── preprocess_cv.py
    │   └── preprocess_rag.py
    ├── docker-compose.yml
    ├── frontend
    ├── models
    │   ├── Dockerfile
    │   ├── docker-shell.sh
    │   ├── infer_model.py
    │   ├── model_rag.py
    │   └── train_model.py
    └── workflow
```

# AC215 - Milestone3 - Cheesy App

**Team Members**
Vincent Hock, Tomas Arevalo, Jake **Carmine** Pappo, Mads Groeholdt

**Group Name**
gAIn - The future of health and fitness

**Project**
With the gAIn application, we seek to fill an existing gap in the health and fitness industry by providing users with an affordable, knowledgeable, and context-aware AI-enabled personal trainer. Our trainer seeks to replace expensive, thin-stretched personal trainers and fitness coaches, and provides an easier solution for those seeking to educate themselves compared to relying on the internet's scathered, unverified information. The main functionality of the app is a chat interface with the intelligent assistant, where users can ask their coach for advice, training plans, and more. The coach improves on other LLM's in the area of health and fitness by both being fine-tuned on quality-checked expert resources, as well as having access to each user's historical activity and fitness data powered by an AI-agent.

---

### Milestone4 - THIS NEEDS TO BE EDITED

In this milestone, we have the components for frontend, API service, also components from previous milestones for data management, including versioning, as well as the computer vision and language models.

After completions of building a robust ML Pipeline in our previous milestone we have built a backend api service and frontend app. This will be our user-facing application that ties together the various components built in previous milestones.

**Application Design**

Before we start implementing the app we built a detailed design document outlining the application’s architecture. We built a Solution Architecture and Technical Architecture to ensure all our components work together.

Here is our Solution Architecture:

<img src="images/solution-arch.png"  width="800">

Here is our Technical Architecture:

<img src="images/technical-arch.png"  width="800">

**Backend API**

We built backend api service using fast API to expose model functionality to the frontend. We also added apis that will help the frontend display some key information about the model and data.

<img src="images/api-list.png"  width="800">

**Frontend**

A user friendly React app was built to identify various species of mushrooms in the wild using computer vision models from the backend. Using the app a user can take a picture of a mushroom and upload it. The app will send the image to the backend api to get prediction results on weather the mushroom is poisonous or not.

Here are some screenshots of our app:

`Add screenshots here`

## Running Dockerfile

Instructions for running the Dockerfile can be added here.
To run Dockerfile - `Instructions here`

**Notebooks/Reports**
This folder contains code that is not part of container - for e.g: Application mockup, EDA, any 🔍 🕵️‍♀️ 🕵️‍♂️ crucial insights, reports or visualizations.

---

You may adjust this template as appropriate for your project.
