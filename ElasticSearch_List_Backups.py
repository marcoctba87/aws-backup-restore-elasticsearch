import boto3
import requests
from requests_aws4auth import AWS4Auth

host = '' ##Endpoint do NOVO ElasticSearch, finalize com um /
region = '' ## Região
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

# Repository
path = '_snapshot/<DIR-PONTO-DE-MONTAGEM>/_all?pretty'
url = host + path

headers = {"Content-Type": "application/json"}

r = requests.get(url, auth=awsauth, headers=headers)

print(r.status_code)
print(r.text)
