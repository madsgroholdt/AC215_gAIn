import os
import argparse
import random
import string
from kfp import dsl
from kfp import compiler
import google.cloud.aiplatform as aip
from model_deployment import model_deploy

GCP_PROJECT = os.environ["GCP_PROJECT"]
GCS_BUCKET_NAME = os.environ["GCS_BUCKET_NAME"]
GCS_SERVICE_ACCOUNT = os.environ["GCS_SERVICE_ACCOUNT"]
GCP_REGION = os.environ["GCP_REGION"]
BUCKET_URI = "gs:" + f"//{GCS_BUCKET_NAME}"
PIPELINE_ROOT = f"{BUCKET_URI}/pipeline_root/root"

IMAGE_HUB = f"us-central1-docker.pkg.dev/{GCP_PROJECT}/gcf-artifacts"
ARTICLE_COLLECTOR_IMAGE = f"{IMAGE_HUB}/article-collector"
ARTICLE_PROCESSOR_IMAGE = f"{IMAGE_HUB}/article-processor"
MODEL_FINETUNING_IMAGE = f"{IMAGE_HUB}/model-finetuning"


def generate_uuid(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


def article_collector(num_articles):
    print("article_collector()")

    # Define a Container Component
    @dsl.container_component
    def article_collector():
        container_spec = dsl.ContainerSpec(
            image=ARTICLE_COLLECTOR_IMAGE,
            command=[],
            args=[
                "cli.py",
                f"--urls {num_articles}",
                "--scrape",
            ],
        )
        return container_spec

    # Define a Pipeline
    @dsl.pipeline
    def article_collector_pipeline():
        article_collector()

    # Build yaml file for pipeline
    compiler.Compiler().compile(
        article_collector_pipeline, package_path="article_collector.yaml"
    )

    # Submit job to Vertex AI
    aip.init(project=GCP_PROJECT, staging_bucket=BUCKET_URI)

    job_id = generate_uuid()
    DISPLAY_NAME = "gain-article-collector-" + job_id
    job = aip.PipelineJob(
        display_name=DISPLAY_NAME,
        template_path="article_collector.yaml",
        pipeline_root=PIPELINE_ROOT,
        enable_caching=False,
    )

    job.run(service_account=GCS_SERVICE_ACCOUNT)


def article_processor():
    print("article_processor()")

    # Define a Container Component
    @dsl.container_component
    def article_processor():
        container_spec = dsl.ContainerSpec(
            image=ARTICLE_PROCESSOR_IMAGE,
            command=[],
            args=[
                "cli.py",
                "--generate",
                "--prepare",
                "--upload",
            ],
        )
        return container_spec

    # Define a Pipeline
    @dsl.pipeline
    def article_processor_pipeline():
        article_processor()

    # Build yaml file for pipeline
    compiler.Compiler().compile(
        article_processor_pipeline, package_path="article_processor.yaml"
    )

    # Submit job to Vertex AI
    aip.init(project=GCP_PROJECT, staging_bucket=BUCKET_URI)

    job_id = generate_uuid()
    DISPLAY_NAME = "gain-article-processor-" + job_id
    job = aip.PipelineJob(
        display_name=DISPLAY_NAME,
        template_path="article_processor.yaml",
        pipeline_root=PIPELINE_ROOT,
        enable_caching=False,
    )

    job.run(service_account=GCS_SERVICE_ACCOUNT)


def model_finetuning():
    print("model_finetuning()")

    # Define a Container Component for data processor
    @dsl.container_component
    def model_finetuning():
        container_spec = dsl.ContainerSpec(
            image=MODEL_FINETUNING_IMAGE,
            command=[],
            args=[
                "cli.py",
                "--train",
            ],
        )
        return container_spec

    # Define a Pipeline
    @dsl.pipeline
    def model_finetuning_pipeline():
        model_finetuning()

    # Build yaml file for pipeline
    compiler.Compiler().compile(
        model_finetuning_pipeline, package_path="model_finetuning.yaml"
    )

    # Submit job to Vertex AI
    aip.init(project=GCP_PROJECT, staging_bucket=BUCKET_URI)

    job_id = generate_uuid()
    DISPLAY_NAME = "gain-model-finetuning-" + job_id
    job = aip.PipelineJob(
        display_name=DISPLAY_NAME,
        template_path="model_finetuning.yaml",
        pipeline_root=PIPELINE_ROOT,
        enable_caching=False,
    )

    job.run(service_account=GCS_SERVICE_ACCOUNT)


def model_deploying():
    print("model_deploy()")

    # Define a Pipeline
    @dsl.pipeline
    def model_deploy_pipeline():
        model_deploy()

    # Build yaml file for pipeline
    compiler.Compiler().compile(
        model_deploy_pipeline, package_path="model_deploy.yaml"
    )

    # Submit job to Vertex AI
    aip.init(project=GCP_PROJECT, staging_bucket=BUCKET_URI)

    job_id = generate_uuid()
    DISPLAY_NAME = "gain-model-deploy-" + job_id
    job = aip.PipelineJob(
        display_name=DISPLAY_NAME,
        template_path="model_deploy.yaml",
        pipeline_root=PIPELINE_ROOT,
        enable_caching=False,
    )

    job.run(service_account=GCS_SERVICE_ACCOUNT)


def pipeline(num_articles):
    print("pipeline()")

    # Define a Container Component
    @dsl.container_component
    def article_collector():
        container_spec = dsl.ContainerSpec(
            image=ARTICLE_COLLECTOR_IMAGE,
            command=[],
            args=[
                "cli.py",
                f"--urls {num_articles}",
                "--scrape",
            ],
        )
        return container_spec

    # Define a Container Component for article processor
    @dsl.container_component
    def article_processor():
        container_spec = dsl.ContainerSpec(
            image=ARTICLE_PROCESSOR_IMAGE,
            command=[],
            args=[
                "cli.py",
                "--generate",
                "--prepare",
                "--upload",
            ],
        )
        return container_spec

    # Define a Container Component for model finetuning
    @dsl.container_component
    def model_finetuning():
        container_spec = dsl.ContainerSpec(
            image=MODEL_FINETUNING_IMAGE,
            command=[],
            args=[
                "cli.py",
                "--train",
            ],
        )
        return container_spec

    # Define a Pipeline
    @dsl.pipeline
    def ml_pipeline():
        # Data Collector
        article_collector_task = (
            article_collector()
            .set_display_name("Article Collector")
        )

        # Data Processor
        article_processor_task = (
            article_processor()
            .set_display_name("Article Processor")
            .after(article_collector_task)
        )

        # Model Finetuning
        model_finetuning_task = (
            model_finetuning()
            .set_display_name("Model Finetuning")
            .after(article_processor_task)
        )

        # Model Deployment
        model_deploy_task = (
            model_deploy()
            .set_display_name("Model Deploy")
            .after(model_finetuning_task)
        )

        _ = model_deploy_task

    # Build yaml file for pipeline
    compiler.Compiler().compile(ml_pipeline, package_path="pipeline.yaml")

    # Submit job to Vertex AI
    aip.init(project=GCP_PROJECT, staging_bucket=BUCKET_URI)

    job_id = generate_uuid()
    DISPLAY_NAME = "gain-pipeline-" + job_id
    job = aip.PipelineJob(
        display_name=DISPLAY_NAME,
        template_path="pipeline.yaml",
        pipeline_root=PIPELINE_ROOT,
        enable_caching=False,
    )

    job.run(service_account=GCS_SERVICE_ACCOUNT)


def main(args=None):
    print("CLI Arguments:", args)

    if args.article_collector:
        article_collector(args.article_collector)

    if args.article_processor:
        article_processor()

    if args.model_finetuning:
        model_finetuning()

    if args.model_deploy:
        model_deploying()

    if args.pipeline:
        pipeline(args.pipeline)


if __name__ == "__main__":
    # Generate the inputs arguments parser
    parser = argparse.ArgumentParser(description="Workflow CLI")

    parser.add_argument(
        "--article_collector",
        type=int,
        help="Run just the Article Collector",
    )

    parser.add_argument(
        "--article_processor",
        action="store_true",
        help="Run just the Article Processor",
    )

    parser.add_argument(
        "--model_finetuning",
        action="store_true",
        help="Run just the Model Finetuning",
    )

    parser.add_argument(
        "--model_deploy",
        action="store_true",
        help="Run just model deployment",
    )

    parser.add_argument(
        "--pipeline",
        type=int,
        help="Run full Gain ML Pipeline",
    )

    args = parser.parse_args()

    main(args)
