import os
import csv
from unittest.mock import MagicMock, patch
from src.api_service.api.data_preprocessing.csv_to_txt import (
    get_csv_txt_paths,
    get_first_last_name,
    csv_to_txt,
    create_activities_txt,
    upload_to_gcp
)


def test_get_csv_txt_paths():
    with patch("os.path.exists", return_value=True):
        csv_path, txt_path = get_csv_txt_paths()
        assert csv_path == '/api/data_preprocessing/csv_data/'
        assert txt_path == '/api/data_preprocessing/txt_data/'

    with patch("os.path.exists", return_value=False):
        csv_path, txt_path = get_csv_txt_paths()
        assert csv_path == '/csv_data/'
        assert txt_path == '/txt_data/'


# Test get_first_last_name
def test_get_first_last_name():
    first_name, last_name = get_first_last_name("John_Doe_metrics.csv")
    assert first_name == "John"
    assert last_name == "Doe"


# Test csv_to_txt
def test_csv_to_txt(tmp_path):
    input_csv = tmp_path / "input.csv"
    output_txt = tmp_path / "output.txt"

    # Create a mock CSV file
    data = {
        "date": ["2024-12-01"],
        "distance (meters)": [5000],
        "moving time (seconds)": [1200]
    }

    input_csv = "output.csv"
    with open(input_csv, mode="w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(data.keys())
        writer.writerows(zip(*data.values()))
        csv_to_txt(input_csv, output_txt, "John_Doe_metrics.csv")

    # Verify the output file is created and has content
    assert output_txt.exists()
    with open(output_txt, "r") as f:
        content = f.read()
        assert "December 01st 2024, John Doe had the following" in content
        assert "Distance (meters) was 5000 meters" in content
        assert "Moving Time (seconds) was 1200 seconds" in content

    # Delete the created CSV file
    txt_path = ("src/api_service/api/data_preprocessing/txt_data/"
                "John_Doe_strava_data.txt")

    if os.path.exists(txt_path):
        os.remove(txt_path)
        print(f"Deleted test TXT file: {txt_path}")


# Test create_activities_txt
@patch("os.listdir", return_value=["John_Doe_activities.csv"])
@patch("os.getcwd", return_value="/mocked/path")
@patch("api_service.api.data_preprocessing.csv_to_txt.csv_to_txt")
@patch("api_service.api.data_preprocessing.csv_to_txt.get_csv_txt_paths",
       return_value=("/csv_data/", "/txt_data/"))
def test_create_activities_txt(mock_get_paths,
                               mock_csv_to_txt,
                               mock_getcwd,
                               mock_listdir):
    create_activities_txt()
    mock_csv_to_txt.assert_called_once_with(
        "/mocked/path/csv_data/John_Doe_activities.csv",
        "/mocked/path/txt_data/John_Doe_activities.txt",
        "John_Doe_activities.csv"
    )


# Test upload_to_gcp
@patch("os.listdir", return_value=["John_Doe_activities.csv"])
@patch("os.getcwd", return_value="/mocked/path")
@patch("api_service.api.data_preprocessing.csv_to_txt.get_csv_txt_paths",
       return_value=("/csv_data/", "/txt_data/"))
@patch("google.cloud.storage.Client")
@patch("google.oauth2.service_account.Credentials.from_service_account_file")
def test_upload_to_gcp(mock_credentials,
                       mock_storage_client,
                       mock_get_paths,
                       mock_getcwd,
                       mock_listdir):
    mock_bucket = MagicMock()
    mock_blob = MagicMock()
    mock_storage_client.return_value.bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob

    upload_to_gcp("test-bucket", "/csv_data/", "output-folder")

    mock_blob.upload_from_filename.assert_called_once_with(
        "/mocked/path/csv_data/John_Doe_activities.csv"
    )
    mock_bucket.blob.assert_called_once_with(
        "output-folder/John_Doe/John_Doe_activities.csv"
    )
