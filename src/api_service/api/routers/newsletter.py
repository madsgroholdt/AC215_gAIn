import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from typing import Optional
import glob
import json
import traceback

# Define Router
router = APIRouter()

# Newsletters should be downloaded from a GCS bucket
# (ML Task generates and saves into a bucket)
# We will assume the Newsletters have already been downloaded
# into "news-letters" folder locally
data_folder = "newsletters"


@router.get("/")
async def get_newsletters(limit: Optional[int] = None):
    """Get all newsletters, optionally limited to a specific number"""
    newsletters = []
    data_files = glob.glob(os.path.join(data_folder, "*.json"))
    for filepath in data_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                news_data = json.load(f)
                newsletters.append(news_data)
        except Exception as e:
            print(f"Error loading newsletter from {filepath}: {str(e)}")
            traceback.print_exc()

    # Sort by dts
    newsletters.sort(key=lambda x: x.get('dts', 0), reverse=True)
    if limit:
        return newsletters[:limit]

    return newsletters


@router.get("/{newsletter_title}")
async def get_newsletter(newsletter_title: str):
    """Get a specific ID"""
    filepath = os.path.join(data_folder, f"{newsletter_title}.json")
    with open(filepath, 'r', encoding='utf-8') as f:
        newsletter = json.load(f)
    if not newsletter:
        raise HTTPException(status_code=404, detail="Newsletter not found")
    return newsletter


@router.get("/image/{image_name}")
async def get_newsletter_image(image_name: str):
    content_type = "application/octet-stream"
    image_path = os.path.join(data_folder, "assets", image_name)
    print(image_path)
    return FileResponse(
        path=image_path,
        media_type=content_type
    )
