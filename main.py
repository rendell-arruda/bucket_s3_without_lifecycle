import threading
import concurrent.futures
from boto3 import Session
from datetime import datetime

#Garantindo uma escrita thread-safe no arquivo de saída
file_lock = threading.Lock()

# Lista dos perfis (nomes das credenciais configuradas no ~/.aws/credentials)
AWS_PROFILES = ["secundaria", "default"]
data_atual = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

def get_buckets_without_lifecycle(profile, output_file):
    """
    Em um ambiente Lambda real, você geralmente usaria roles e não perfis estáticos.
    Para testar localmente com perfis, use boto3.Session(profile_name=profile_name).
    Para implantação em Lambda, a role associada à função Lambda deve ter permissão para assumir roles nas contas que você quer acessar.
    """

    #Garantindo as credenciais corretas para o perfil  
    session = Session(profile_name=profile)
    s3 = session.client('s3') 

    try:
        response = s3.list_buckets()
        buckets = response.get('Buckets', [])
        print(f"Total de buckets encontrados no perfil {profile}: {len(buckets)}")

        #Gera a lista de buckets sem lifecycle
        buckets_without_lifecycle = []
        
        for bucket in buckets:
            bucket_name = bucket['Name']
            try:
                # Tenta buscar a configuração de lifecycle do bucket
                s3.get_bucket_lifecycle_configuration(Bucket=bucket_name)
                
            except s3.exceptions.ClientError as e:
                # Se o bucket **não tiver** lifecycle, o erro será NoSuchLifecycleConfiguration
                if e.response['Error']['Code'] == 'NoSuchLifecycleConfiguration':
                    print(bucket_name)  
                    buckets_without_lifecycle.append(bucket_name)       # Depois do primeiro, os próximos recebem vírgula antes

        # Agora, escreve os resultados no arquivo de forma thread-safe
        with file_lock:
            with open(output_file, "a") as file:
                file.write(f"Conta: {profile}\n")
                if buckets_without_lifecycle:
                    file.write(", ".join(buckets_without_lifecycle))
                else:
                    file.write("Nenhum bucket sem lifecycle")
                file.write("\n\n")
                
    except Exception as e:
        # Em caso de erro ao listar os buckets da conta, mostra mensagem no terminal
        print(f"Erro ao processar perfil {profile}: {e}")
        with file_lock:
            with open(output_file, 'a') as file:
                file.write(f"Conta: {profile}\n")
                file.write(f"ERRO: {e}\n\n")

def main():
    print(f"Iniciando verificação em {len(AWS_PROFILES)} perfis...")

    max_workers = 5  

    nome_arquivo = f"report/buckets_sem_lifecycle_{data_atual}.csv"
    
    # Usando ThreadPoolExecutor para paralelizar chamadas de API (I/O bound) e executa em paralelo. 'as_completed' retorna os resultados à medida que ficam prontos.
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_profile = {
            executor.submit(get_buckets_without_lifecycle, profile,nome_arquivo): profile for profile in AWS_PROFILES
        }
        
        for future in concurrent.futures.as_completed(future_to_profile):
            profile = future_to_profile[future]
            try:
                future.result()
                print(f"Resultado para {profile} concluido")
            except Exception as exc:
                print(f"'{profile}' gerou uma exceção: {exc}")
    
    print(f"Verificação concluída. Resultados salvos em '{nome_arquivo}'.")

if __name__ == "__main__":
    main()
