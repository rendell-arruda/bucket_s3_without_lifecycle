import boto3

profiles = ["sandbox", "default"]

def get_buckets_without_lifecycle(session, profile, output_file):
    s3 = session.client('s3')
    try:
        response = s3.list_buckets()
        buckets = response.get('Buckets', [])
        print(f"Total de buckets encontrados no perfil {profile}: {len(buckets)}")

        output_file.write(f"Perfil: {profile}\n")

        primeiro = True
        encontrou = False

        for bucket in buckets:
            bucket_name = bucket['Name']
            try:
                s3.get_bucket_lifecycle_configuration(Bucket=bucket_name)
            except s3.exceptions.ClientError as e:
                if e.response['Error']['Code'] == 'NoSuchLifecycleConfiguration':
                    print(bucket_name)
                    encontrou = True
                    if not primeiro:
                        output_file.write(",")
                    output_file.write(bucket_name)
                    primeiro = False

        if not encontrou:
            output_file.write("Nenhum bucket sem lifecycle")

        output_file.write("\n\n")  # Separador entre perfis

    except Exception as e:
        print(f"Erro ao processar perfil {profile}: {e}")

with open("buckets_sem_lifecycle.csv", "w") as output_file:
    for profile in profiles:
        print(f"\nVerificando perfil: {profile}")
        session = boto3.Session(profile_name=profile)
        get_buckets_without_lifecycle(session, profile, output_file)