import json
import boto3 # Importando a biblioteca boto3 para trabalhar com os serviços da AWS
import os # Para recuperar variáveis de ambiente
import uuid # Para gerar um identificador único

dynamodb_resource = boto3.resource("dynamodb")

table_name = os.environ['TABLE_NAME'] # Nomeda Tabela do DynamoDB
table = dynamodb_resource.Table(table_name)

def lambda_handler(event, context):
    
    try:
        response = table.scan()
        items = response.get('Items', [])
        print(items)
        return {
            "statusCode": 200,
            'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps({
                "message": "Dados recuperados com sucesso",
                "data": items
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
                "message": "Erro ao recuperar os dados"
            }),    
        }