# Introdução

Este procedimento é destinado a realização de backup e restore de um cluster de Elasticsearch na AWS.

## Pré requisitos

> Baixar uma copia dos scripts desse repositório em sua maquina local:
   
>Usuário com permissão de admin, ou usuário com a adição da seguinte política:

        
    {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "iam:PassRole",
             "Resource": "arn:aws:iam::<ID-DA-CONTA-AWS>:role/<ARN-DA-ROLE-CRIADA-PASSO-1.2>"
        },
        {
            "Effect": "Allow",
            "Action": [
                "es:ESHttpPut",
                "es:ESHttpGet",
                "es:ESHttpPost"
            ],
            "Resource": "arn:aws:es:<REGIAO-DO-CLUSTER>:<ID-DA-CONTA-AWS>:domain/<NOME_CLUSTER_ELASTIC>/*"
        }
    ]
    }
    
>Obter a Secret Key e Access Key do usuário utilizado, e configurar no terminal conforme o exemplo abaixo:

    export AWS_ACCESS_KEY_ID="SUA_ACCESS_KEY"
    export AWS_SECRET_ACCESS_KEY="SUA_SECRET_KEY"


## Procedimentos


> ### 1. Backup Manual em um Bucket S3 <br />

>1.1 Criar um bucket S3 na mesma conta e região onde está o elasticsearch a ser realizado o backup, com um nome como por exemplo:<br>
    
    my-elk.elasticsearch.snapshot

>1.2 Criar uma role no IAM com a seguinte política (substitua <NOME-BUCKET> pelo nome do bucket criado no passo anterior):


    {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "s3:ListBucket"
            ],
            "Effect": "Allow",
            "Resource": [
                "arn:aws:s3:::<NOME-BUCKET>"
            ]
        },
        {
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject"
            ],
            "Effect": "Allow",
            "Resource": [
                "arn:aws:s3:::<NOME-BUCKET>/*"
            ]
        }
    ]
    }

>1.3 Configure a relação de confiança da role com a seguinte política:

    {
    "Version": "2012-10-17",
    "Statement": [
        {
        "Effect": "Allow",
        "Principal": {
            "Service": "es.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
        }
    ]
    }

>1.4 Configurar no scripts "ElasticSearch_Change_Repo.py" o valor para as seguintes variáveis:
    
    - host (Endpoint do Elasticsearch)
    - region (Região do Elasticsearch)
    - path (Substitua <DIR-PONTO-DE-MONTAGEM> por um nome de diretorio que sera criado como ponto de montagem).
      Deverá ficar conforme o exemplo: path = '_snapshot/meu-backup'
    - payload (Configurar os valores criados nos passos anteriores em <NOME-BUCKET>, <REGIAO-BUCKET> e <ARN-ROLE-BACKUP>)

>1.5 Realizar a execução do script "ElasticSearch_Change_Repo.py":


    python3 ElasticSearch_Change_Repo.py

>### 2. Realizar o backup manualmente

>2.1 No script "ElasticSearch_Take_Snapshot.py" configure os valores das seguintes variáveis:

    - host (Endpoint do Elasticsearch)
    - region (Região do Elasticsearch)
    - path (Substitua <DIR-PONTO-DE-MONTAGEM> pelo nome criado no passo 1.4 na variavel "path" e <NOME-SNAP-A-SER-CRIADO> pelo nome que deseja criar).
      Deverá ficar conforme o exemplo: path = '_snapshot/meu-backup/meu-snap-08-04-2021'

>2.2 Realizar a execução do script "ElasticSearch_Take_Snapshot.py":

    python3 ElasticSearch_Take_Snapshot.py


>###3. Listar o(s) backup realizado(s)
 
>3.1 No script "ElasticSearch_List_Backups.py" configure os valores das seguintes variáveis:

    - host (Endpoint do Elasticsearch)
    - region (Região do Elasticsearch)
    - path (Substitua <DIR-PONTO-DE-MONTAGEM> pelo nome criado no passo 1.4 na variavel "path").
      Deverá ficar conforme o exemplo: path = '_snapshot/meu-backup/_all?pretty'

>3.2 Realizar a execução do script "ElasticSearch_List_Backups.py":

     python3 ElasticSearch_List_Backups.py
 
>3.3 Serão exibidos os backup realizados no formato json onde nome do backup será o campo :

    "snapshot": "meu-snap-08-04-2021"

>###4. Restauração de Backup
    
><span style="color:red">Importante:</span> Caso o controle de acesso refinado estiver ativo no cluster, deverá ser configurado o ARN do usuário utilizado para a restauração:
    
    Logar no kibana com o usuário admin, Clicar em Security >> Role Mappings:
    Selecionar a role "all_access" clicar em "Manage Mappings" e no campo "Users" adicionar a ARN do usuário IAM que deverá ter acesso:
    
>4.1 Listar os snapshot executando o script do passo 3 e guardar o nome do backup a ser restaurado

>4.2 No script "ElasticSearch_Restore_Snapshot.py" configure os valores das seguintes variáveis:

    - host (Endpoint do Elasticsearch)
    - region (Região do Elasticsearch)
    - path (Substitua <DIR-PONTO-DE-MONTAGEM> pelo nome criado no passo 1.4 na variavel "path" e <NOME-DO-BACKUP> pelo nome do snap a ser restaurado).
      Deverá ficar conforme o exemplo: path = '_snapshot/meu-backup/meu-snap-08-04-2021/_restore'
 
>4.3 Realizar a execução do script "ElasticSearch_Restore_Snapshot.py":

    python3 ElasticSearch_Restore_Snapshot.py
