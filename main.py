import boto3

profiles= ["sandbox", "default"]

def get_buckets_without_lifecycle(session):
    s3 = session.client('s3')
    # buckets_without_lifecycle = []

    try:
        # Lista todos os buckets
        response = s3.list_buckets()
        buckets = response.get('Buckets', [])
        print(f"Total de buckets encontrados: {len(buckets)}")
        
        for bucket in buckets:
            bucket_name = bucket['Name']
            try:
                # Verifica a política de lifecycle do bucket
                s3.get_bucket_lifecycle_configuration(Bucket=bucket_name)
            except s3.exceptions.ClientError as e:
                # Adiciona o bucket à lista se não houver política de lifecycle
                if e.response['Error']['Code'] == 'NoSuchLifecycleConfiguration':
                    print(bucket_name, end=',')
                    # buckets_without_lifecycle.append(bucket_name)
    except Exception as e:
        print(f"Erro ao listar buckets: {e}")

    # return buckets_without_lifecycle

for profile in profiles:
    print("\n")
    print(f"Verificando perfil: {profile}")
    session = boto3.Session(profile_name=profile)
    buckets = get_buckets_without_lifecycle(session)
    
    # if buckets:
    #     print("Buckets sem política de lifecycle:")
    #     for bucket in buckets:
    #         print(f"- {bucket}")
    # else:
    #     print("Todos os buckets têm política de lifecycle configurada.")
    
    
# if __name__ == '__main__':
#     get_buckets_without_lifecycle()