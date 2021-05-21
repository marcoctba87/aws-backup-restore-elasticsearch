import boto3
import requests
from requests_aws4auth import AWS4Auth

host = '' ##Endpoint do ElasticSearch a ser realizado Snapshot, finalize com um /
region = '' ## Região
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

# Take snapshot

path = '_snapshot/<DIR-PONTO-DE-MONTAGEM>/<NOME-SNAP-A-SER-CRIADO>' ## Diretorio configurado no script "ElasticSearch_Change_Repo.py" e no do snap a ser criado"
url = host + path

r = requests.put(url, auth=awsauth)

print(r.text)

