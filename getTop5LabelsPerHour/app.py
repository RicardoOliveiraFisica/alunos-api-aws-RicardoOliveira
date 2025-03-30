import boto3 # Importando a biblioteca boto3 para trabalhar com os serviços da AWS
import os # Para recuperar variáveis de ambiente
from datetime import datetime, timedelta, timezone
from collections import Counter
import json

dynamodb_resource = boto3.resource("dynamodb")

table_name = os.environ['TABLE_NAME'] # Nome da Tabela do DynamoDB
table = dynamodb_resource.Table(table_name)

def lambda_handler(event, context):
    try:
        ranking = get_top_5_labels_per_hour()
        return {
            "statusCode": 200,
            'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps({
                "message": "Ranking das Labels obtidas com sucesso",
                "data": ranking
            }),    
        }
    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps({
                "message": "Erro ao recuperar o ranking das labels",
            }),    
        }
    
def get_top_5_labels_per_hour():
    one_hour_ago = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()

    # Consulta registros criados na última hora para montar o ranking
    response = table.scan(
        FilterExpression="createdAt > :one_hour_ago",
        ExpressionAttributeValues={":one_hour_ago": one_hour_ago}
    )

    labels_found = []

    for item in response.get("Items", []):
        labels_found.extend(item.get("labels", []))

    if not labels_found:
        return "Nenhuma label inserida na ultima hora."        

    counter = Counter(labels_found)
    total_labels = sum(counter.values())
    percentages = {label: (count / total_labels) * 100 for label, count in counter.items()}
    top_5_labels = sorted(percentages.items(), key=lambda x: x[1], reverse=True)[:5]

    ranking = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "top_labels": [{"label": label, "percentage": round(perc, 2)} for label, perc in top_5_labels]
    }
    
    return ranking