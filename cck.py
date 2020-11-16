import boto3
import requests
from urllib3.util import parse_url as urlparse
from datetime import date
import base64


CCK_BUCKET = "cck-list-zarizeni"
LIST_VERSION = "2020-11-16.csv"
TODAY = date.today().strftime("%Y-%m-%d")


def check_website(url):
    result = urlparse(url)
    if all([result.scheme, result.netloc, result.path]):
        response = requests.get(url)
        client = boto3.resource("s3")
        output = client.Object(CCK_BUCKET, f"archiv/{TODAY}/{base64.b64encode(url.encode()).decode('ascii')}.html")
        output.put(Body=response.text)
    else:
        print(f"Invalid url {url}")


def load_websites():
    client = boto3.client("s3")
    list_file = client.get_object(Bucket=CCK_BUCKET, Key=f"seznamy/{LIST_VERSION}")
    return [institution.split(";") for institution in list_file["Body"].read().decode("utf-8").split("\n")]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    websites = load_websites()
    for website, url in websites:
        print(f"Checking {website} ...")
        check_website(url)
