import boto3
import requests
from requests_aws4auth import AWS4Auth

host = '' ##Endpoint do NOVO ElasticSearch, finalize com um /
region = '' ## Região
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

# Repository snapshot
path = '_snapshot/<DIR-PONTO-DE-MONTAGEM>/<NOME-DO-BACKUP>/_restore' ##Informe o nome do snapshot que deseja restaurar

url = host + path
payload = {"indices": "-.kibana*,-.opendistro_security"}

headers = {"Content-Type": "application/json"}

r = requests.post(url, auth=awsauth, json=payload, headers=headers)

print(r.status_code)
print(r.text)