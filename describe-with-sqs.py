import boto3

# Configuração da sessão
session = boto3.Session(profile_name='default')
s3 = session.client('s3')
sqs = session.client('sqs')

# Nome da fila do SQS
SQS_QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/266549158321/buckets-without-lifecycle"

def get_buckets_without_lifecycle():
    buckets_without_lifecycle = []
    try:
        # Lista todos os buckets
        response = s3.list_buckets()
        buckets = response.get('Buckets', [])
        
        for bucket in buckets:
            bucket_name = bucket['Name']
            try:
                # Verifica a política de lifecycle do bucket
                s3.get_bucket_lifecycle_configuration(Bucket=bucket_name)
            except s3.exceptions.ClientError as e:
                if e.response['Error']['Code'] == 'NoSuchLifecycleConfiguration':
                    buckets_without_lifecycle.append(bucket_name)
    except Exception as e:
        print(f"Erro ao listar buckets: {e}")
    
    return buckets_without_lifecycle

def send_buckets_to_sqs(buckets):
    for bucket in buckets:
        try:
            response = sqs.send_message(
                QueueUrl=SQS_QUEUE_URL,
                MessageBody=bucket
            )
            print(f"Enviado para SQS: {bucket} - MessageId: {response['MessageId']}")
        except Exception as e:
            print(f"Erro ao enviar {bucket} para SQS: {e}")

if __name__ == '__main__':
    buckets = get_buckets_without_lifecycle()
    if buckets:
        print("Buckets sem política de lifecycle:")
        for bucket in buckets:
            print(f"- {bucket}")
        send_buckets_to_sqs(buckets)
    else:
        print("Todos os buckets têm política de lifecycle configurada.")
