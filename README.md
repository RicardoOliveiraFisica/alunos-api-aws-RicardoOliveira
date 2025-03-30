# alunos-api-aws

Este projeto contém o código-fonte e arquivos de suporte para uma aplicação serverless que pode ser implantada com o SAM CLI. Ele inclui os seguintes arquivos e pastas:

- `categorize` - Código para a função Lambda que categoriza imagens.
- `generateContent` - Código para a função Lambda que gera conteúdo usando o Bedrock.
- `presignedUrl` - Código para a função Lambda que gera URLs pré-assinadas para upload de arquivos no S3.
- `events` - Eventos de invocação que podem ser usados para invocar a função.
- `template.yaml` - Um template que define os recursos AWS da aplicação.
- `README.md` - Documentação do projeto.
- `TODO.md` - Lista de tarefas a serem realizadas.

## Estrutura do Projeto

### Categorize

A função Lambda em `categorize/app.py` é responsável por detectar labels em imagens enviadas para um bucket S3 usando o Amazon Rekognition. As labels detectadas são enviadas para uma fila SQS.

### Generate Content

A função Lambda em `generateContent/app.py` é responsável por gerar conteúdo usando o Bedrock com base nas labels detectadas e enviadas para a fila SQS e registra-las na base de dados do DynamoBD.

### Presigned URL

A função Lambda em `presignedUrl/app.py` é responsável por gerar URLs pré-assinadas para upload de arquivos no S3.

### Get All Products

A função Lambda em `getAllProducts/app.py` é responsável por buscar todos os produtos registrados na base de dados do DynamoBD e devolve-las no path `/products`.

### Get Product By Id

A função Lambda em `getProductById/app.py` é responsável por buscar pelo Id o produto registrado na base de dados do DynamoBD e devolve-las no path `/products/{id}`.

## Recursos AWS

Os recursos AWS são definidos no arquivo `template.yaml`. Este arquivo inclui definições para:

- Bucket S3 para upload de imagens.
- Funções Lambda para categorizar imagens, gerar conteúdo e criar URLs pré-assinadas.
- Fila SQS para comunicação entre as funções Lambda.

## Implantação

Para implantar a aplicação pela primeira vez, execute os seguintes comandos no seu terminal:

```bash
sam build --use-container
sam deploy --guided
```

## Testes

Os testes são definidos na pasta tests deste projeto. Use o PIP para instalar as dependências de teste e executar os testes.

```bash
pip install -r tests/requirements.txt --user
# Teste unitário
python -m pytest tests/unit -v
# Teste de integração, requerendo a implantação do stack primeiro.
# Crie a variável de ambiente AWS_SAM_STACK_NAME com o nome do stack que estamos testando
AWS_SAM_STACK_NAME="alunos-api-aws" python -m pytest tests/integration -v
```

## Limpeza

Para deletar a aplicação de exemplo que você criou, use o AWS CLI. Supondo que você usou o nome do seu projeto para o nome do stack, você pode executar o seguinte comando:

```bash
sam delete --stack-name "alunos-api-aws"
```

## Recursos

Veja o guia do desenvolvedor AWS SAM para uma introdução à especificação SAM, ao SAM CLI e aos conceitos de aplicação serverless.

Você também pode usar o AWS Serverless Application Repository para implantar Apps prontos para uso que vão além dos exemplos de hello world e aprender como os autores desenvolveram suas aplicações: AWS Serverless Application Repository main page

# Links Uteis

- `Site S3 Uploader`: https://d19xrahy2u07nb.cloudfront.net/
- `Projeto`: https://github.com/matheus-mprado/alunos-api-aws
- `PerguntAI`: https://d3qbhhrr5ebjj9.cloudfront.net/course?c=801c639e-ff59-4e85-92b7-b1472c1680ed

## Prompt Site S3 Uploader

Considere ser um engenheiro de software senior que conhece de aws, crie uma página web com react e vite, que ao inserir um link de uma API do aws gateway, e inserir um arquivo, ee vai fazer o trabalho de solicitar uma URL pré assinada do s3 com permissão de put para a chamada do api gateway, e no retorno da url pré assinada, faça o envio do arquivo selecionado via PUT para a URL pré assinada.

Crie de forma minimalista, e seguindo uma UI e UX agradavel, utilizando tons de cinza e melhores práticas de desenvolvimento.

separe em componentes se necessário.

## Configuração do CORS do Bucket S3

```json
[
  {
    "AllowedHeaders": ["*"],
    "AllowedMethods": ["GET", "PUT", "POST", "DELETE", "HEAD"],
    "AllowedOrigins": ["*"],
    "ExposeHeaders": [],
    "MaxAgeSeconds": 3600
  }
]
```
