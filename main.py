import boto3  # Importa a biblioteca Boto3 para interagir com os serviços da AWS

# Lista dos perfis (nomes das credenciais configuradas no ~/.aws/credentials)
profiles = ["sandbox", "default"]

# Função que verifica buckets sem lifecycle para um determinado profile
def get_buckets_without_lifecycle(session, profile, output_file):
    s3 = session.client('s3')  # Cria um cliente S3 usando a sessão da conta atual

    try:
        # Lista todos os buckets da conta atual
        response = s3.list_buckets()
        buckets = response.get('Buckets', [])
        print(f"Total de buckets encontrados no perfil {profile}: {len(buckets)}")

        # Escreve o nome do perfil no arquivo de saída
        output_file.write(f"Perfil: {profile}\n")

        primeiro = True         # Variável para controlar se é o primeiro bucket (evita vírgula no início)
        encontrou = False       # Marca se encontrou algum bucket sem lifecycle

        # Loop por cada bucket da conta
        for bucket in buckets:
            bucket_name = bucket['Name']
            try:
                # Tenta buscar a configuração de lifecycle do bucket
                s3.get_bucket_lifecycle_configuration(Bucket=bucket_name)
            except s3.exceptions.ClientError as e:
                # Se o bucket **não tiver** lifecycle, o erro será NoSuchLifecycleConfiguration
                if e.response['Error']['Code'] == 'NoSuchLifecycleConfiguration':
                    print(bucket_name)       # Mostra o bucket no terminal
                    encontrou = True         # Sinaliza que encontrou bucket sem lifecycle

                    # Escreve vírgula antes dos próximos buckets (evita no primeiro)
                    if not primeiro:
                        output_file.write(",")
                    output_file.write(bucket_name)
                    primeiro = False         # Depois do primeiro, os próximos recebem vírgula antes

        # Se nenhum bucket sem lifecycle foi encontrado, escreve uma mensagem padrão
        if not encontrou:
            output_file.write("Nenhum bucket sem lifecycle")

        # Pula duas linhas no arquivo para separar os perfis
        output_file.write("\n\n")

    except Exception as e:
        # Em caso de erro ao listar os buckets da conta, mostra mensagem no terminal
        print(f"Erro ao processar perfil {profile}: {e}")

# Abre (ou cria) o arquivo de saída onde os resultados serão salvos
with open("buckets_sem_lifecycle.txt", "w") as output_file:
    for profile in profiles:
        print(f"\nVerificando perfil: {profile}")
        # Cria uma sessão boto3 para o profile atual
        session = boto3.Session(profile_name=profile)
        # Executa a função de verificação para esse profile
        get_buckets_without_lifecycle(session, profile, output_file)