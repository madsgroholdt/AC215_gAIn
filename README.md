# AC215 - gAIn

**Team Members**
Vincent Hock, Tomas Arevalo, Jake Carmine Pappo, Mads Groeholdt

**Group Name**
gAIn - The future of health and fitness

**Project**
With the gAIn application, we seek to fill an existing gap in the health and fitness industry by providing users with an affordable, knowledgeable, and context-aware AI-enabled personal trainer. Our trainer seeks to replace expensive, thin-stretched personal trainers and fitness coaches, and provides an easier solution for those seeking to educate themselves compared to relying on the internet's scathered, unverified information. The main functionality of the app is a chat interface with the intelligent assistant, where users can ask their coach for advice, training plans, and more. The coach improves on other LLM's in the area of health and fitness by both being fine-tuned on quality-checked expert resources, as well as having access to each user's historical activity and fitness data powered by an AI-agent.


# Milestone 5
In this milestone, we deploy the fully-functional gAIn app to a Kubernetes cluster.

## Prerequisites & Setup

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


## Deployment Instructions

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

## Usage Details

See a video detailing usage [here](https://drive.google.com/file/d/1BOflX-POulPiBh85qdvH2Ypw8ETv6Bmm/view?usp=sharing!)!
## Known Issues & Limitations

### Multiple Users

Currently, the gAIn application does not support individual accounts for each user.
There are no profiles or login functionality, and it could therefore not be deployed to the general public yet.
We would need to enable this to ensure data privacy and security, as well as ensure that personalization is possible
for all new users.

### LLM Mathematics Logic

LLMs are notoriously bad at handling arithmetic. We would like to turn the gAIn LLM into an agent that uses
mathematical functions (ie. sum(), divide(), etc.) to operate on data across multiple days and weeks. This would remove many errors that come from asking for aggregated data, and would allow for a more wholistic view of a user's profile.

### Strava Connectivity
While we tried to minimize the number of clicks the user needs to make to connect their Strava account to gAIn, there is a 20-30 delay after authorizing permissions. This occurs due to rest of the Strava Data Pipeline (the fetching, preprocessing, and uploading of the Strava data) having to finish before the user is redirected back to the homepage. Ideally this would happen concurrently to smoothen the user interaction with gAIn. Additionally, while the current button pulls all the existing Strava data, there is no way to pull new data, without unlinking and then relinking your Strava account. Ideally, we would add another button that allows you to pull only new data, and not all existing data.

### Limited API Integrations
Currently we have only created the ability for a user to connect to their Strava account, but ideally we would like for them to be able to connect to any health and fitness app they have. This includes apps such as Whoop, FitBit, AppleHealthKit, and many others.
