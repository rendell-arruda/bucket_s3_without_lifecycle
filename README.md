# Verificador de Políticas de Lifecycle em Buckets S3

Este script em Python verifica quais buckets do Amazon S3 não possuem uma política de lifecycle configurada. É útil para equipes de **FinOps** e **DevOps** que buscam otimizar custos de armazenamento na AWS.

## 🚀 Funcionalidades

- Lista todos os buckets em uma conta AWS.
- Verifica se cada bucket possui uma política de lifecycle configurada.
- Retorna uma lista de buckets sem política de lifecycle.

## 🛠️ Pré-requisitos

1. **Python 3.7 ou superior**.
2. Instale o AWS CLI e configure um perfil com credenciais:
   ```bash
   aws configure --profile sandbox
   ```
3. Instale a biblioteca **boto3**:
   ```bash
   pip install boto3
   ```

## 📋 Configuração

1. Configure um perfil AWS no seu ambiente usando o **AWS CLI**.
2. Substitua o nome do perfil no código:
   ```python
   session = boto3.Session(profile_name='sandbox')
   ```

## 🖥️ Como usar

1. Clone este repositório:
   ```bash
   git clone https://github.com/rendell-arruda/bucket_s3_without_lifecycle
   cd s3-lifecycle-checker
   ```
2. Execute o script:
   ```bash
   python main.py
   ```

3. O script exibirá:
   - A lista de buckets sem política de lifecycle configurada.
   - Uma mensagem indicando que todos os buckets possuem política, caso aplicável.

## 🔑 Permissões necessárias

A conta AWS usada deve possuir as seguintes permissões:
- `s3:ListAllMyBuckets` – Para listar os buckets.
- `s3:GetBucketLifecycleConfiguration` – Para verificar a política de lifecycle de cada bucket.

## 📝 Exemplo de Saída

```plaintext
Buckets sem política de lifecycle:
- meu-bucket-1
- meu-bucket-2
```

Se todos os buckets estiverem configurados:
```plaintext
Todos os buckets têm política de lifecycle configurada.
```

## 📂 Estrutura do Projeto

```plaintext
.
├── main.py  # Código principal para verificar os buckets
├── README.md              # Documentação do projeto
```

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar PRs.

## 📜 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

## 💡 Autor

Desenvolvido por [Rendell Arruda](https://github.com/rendell-arruda).

---

**Dica:** Sempre valide o código em um ambiente de teste antes de aplicá-lo na produção.