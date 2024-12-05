import argparse
import random
import string
from kfp import dsl
from kfp import compiler
import google.cloud.aiplatform as aip

GCP_PROJECT = "ac215-final-project"
GCS_BUCKET_NAME = "gain-ml-pipeline"
BUCKET_URI = f"gs: //{GCS_BUCKET_NAME}"
PIPELINE_ROOT = f"{BUCKET_URI}/pipeline_root/root"
GCS_SERVICE_ACCOUNT = "ml-pipeline@ac215-final-project.iam.gserviceaccount.com"
GCP_REGION = "us-central1"

ARTICLE_COLLECTOR_IMAGE = "us-central1-docker.pkg.dev/ac215-final-project/\
                            gcf-artifacts/article-collector"
ARTICLE_PROCESSOR_IMAGE = "us-central1-docker.pkg.dev/ac215-final-project/\
                            gcf-artifacts/article-processor"


def generate_uuid(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


def article_collector():
    print("article_collector()")

    # Define a Container Component
    @dsl.container_component
    def article_collector():
        container_spec = dsl.ContainerSpec(
            image=ARTICLE_COLLECTOR_IMAGE,
            command=[],
            args=[
                "cli.py",
                # "--urls",
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

    # Define a Container Component for data processor
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


def main(args=None):
    print("CLI Arguments:", args)

    if args.article_collector:
        article_collector()

    if args.article_processor:
        article_processor()


if __name__ == "__main__":
    # Generate the inputs arguments parser
    parser = argparse.ArgumentParser(description="Workflow CLI")

    parser.add_argument(
        "--article_collector",
        action="store_true",
        help="Run just the Article Collector",
    )

    parser.add_argument(
        "--article_processor",
        action="store_true",
        help="Run just the Article Processor",
    )

    args = parser.parse_args()

    main(args)
