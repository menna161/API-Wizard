import requests


def on_gcp():
    'Detect whether the current running environment is on GCP.'
    try:
        response = requests.get(GCP_METADATA_URL, headers=GCP_METADATA_HEADER, timeout=5)
        return (response.status_code == 200)
    except requests.exceptions.RequestException:
        return False
