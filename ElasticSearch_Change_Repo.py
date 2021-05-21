import boto3
import requests
from requests_aws4auth import AWS4Auth

host = '' ##Endpoint do NOVO ElasticSearch, finalize com um /
region = '' ## Região
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

# Register repository
path = '_snapshot/<DIR-PONTO-DE-MONTAGEM>' ## Substitua após o "/"" pelo nome do dir que deseja criar como ponto de montagem
url = host + path

payload = {
  "type": "s3",
  "settings": {
    "bucket": "<NOME-BUCKET>",
    "region": "<REGIAO-BUCKET>",
    "role_arn": "<ARN-ROLE-BACKUP>"
  }
}

headers = {"Content-Type": "application/json"}

r = requests.put(url, auth=awsauth, json=payload, headers=headers)

print(r.status_code)
print(r.text)
