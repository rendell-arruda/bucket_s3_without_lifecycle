# 🛡️ Verificador de Políticas de Lifecycle em Buckets S3 – Multi-Conta

Este script em Python percorre múltiplas contas AWS (via perfis configurados no AWS CLI) e identifica quais buckets do Amazon S3 **não possuem política de lifecycle configurada**.  
Ideal para equipes de **FinOps** e **DevOps** que desejam otimizar custos de armazenamento na AWS.

---

## 🚀 Funcionalidades

- Itera sobre múltiplos perfis AWS configurados localmente.
- Lista todos os buckets S3 por conta.
- Verifica se cada bucket possui política de lifecycle configurada.
- Imprime o nome dos buckets sem lifecycle à medida que processa (evitando timeouts).
- Salva a saída em um arquivo `.csv` no formato CSV, com data e hora no nome.

---

## 🛠️ Pré-requisitos

1. **Python 3.7 ou superior**.
2. AWS CLI instalado e perfis configurados:
   ```bash
   aws configure --profile nome-do-perfil
   ```
3. Biblioteca `boto3` instalada:
   ```bash
   pip install boto3
   ```

---

## 📋 Configuração

1. Edite a lista de perfis AWS no script:
   ```python
   profiles = ["sandbox", "default", "conta-prod", "conta-dev"]
   ```

2. O script criará automaticamente um arquivo `.txt` com nome no formato:
   ```
   buckets_sem_lifecycle_YYYY-MM-DD_HH-MM-SS.txt
   ```

---

## 🖥️ Como usar

1. Clone este repositório:
   ```bash
   git clone https://github.com/rendell-arruda/bucket_s3_without_lifecycle
   cd bucket_s3_without_lifecycle
   ```

2. Execute o script:
   ```bash
   python main.py
   ```

3. O script:
   - Irá iterar por cada perfil AWS definido.
   - Imprimirá os buckets sem lifecycle conforme encontra.
   - Gerará um arquivo `.txt` contendo, para cada conta, os buckets sem lifecycle separados por vírgulas, no estilo CSV.

---

## 🔑 Permissões necessárias

A conta AWS usada em cada perfil precisa das seguintes permissões:

- `s3:ListAllMyBuckets` – Para listar todos os buckets da conta.
- `s3:GetBucketLifecycleConfiguration` – Para verificar se o bucket possui política de lifecycle.

---

## 📂 Estrutura do Projeto

```plaintext
.
├── main.py            # Script principal
├── README.md          # Este arquivo
├── buckets_sem_lifecycle_YYYY-MM-DD_HH-MM-SS.txt  # Saída gerada
```

---

## 📌 Exemplo de saída no arquivo `.csv`

```csv
Conta: sandbox
bucket-finops-logs, bucket-dados-temp, bucket-relatorios

Conta: default
bucket-dev, bucket-teste-api
```

---

## 🤝 Contribuições

Contribuições são bem-vindas!  
Sinta-se à vontade para abrir issues ou enviar pull requests com melhorias, correções ou sugestões.

---

## 📜 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

## 💡 Autor

Desenvolvido por [Rendell Arruda](https://github.com/rendell-arruda).  
FinOps Engineer | Automação para Cloud | Otimização de Custos em AWS

---

> 💡 *Dica:* sempre teste os scripts em ambientes de desenvolvimento antes de aplicá-los em produção.
