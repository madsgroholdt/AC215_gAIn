from kfp import dsl


# Define a Container Component
@dsl.component(
    base_image="python:3.10", packages_to_install=["google-cloud-aiplatform"]
)
def model_deploy():
    print("Model Deployment")

    import google.cloud.aiplatform as aip

    # Get endpoint
    endpoint = aip.Endpoint(endpoint_name="1336804928747732992",
                            project="ac215-final-project",
                            location="us-central1")

    # Get most recently trained model
    model = aip.Model.list(filter="display_name=gain-finetuned")[0]

    # Deploy model to existing endpoint
    model.deploy(
        endpoint=endpoint,
        machine_type="n1-standard-4",  # Choose a machine type
        traffic_split={"0": 100},  # Route 100% of traffic to this model
        accelerator_count=0,
        min_replica_count=1,
        max_replica_count=1,
        sync=True,
    )
