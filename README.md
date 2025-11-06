# Sistema de Coleta e Processamento de Dados v2.0

## 📋 Descrição

Sistema profissional de coleta, processamento e armazenamento de dados de APIs públicas. Arquitetura modular com separação de responsabilidades e containerização via Docker.

## 🏗️ Arquitetura

```
case_python/
│
├── app/                    # Aplicação principal
│   ├── __init__.py
│   ├── main.py            # Ponto de entrada
│   └── scheduler.py       # Gerenciamento de horários
│
├── config/                 # Configurações
│   ├── __init__.py
│   └── settings.py        # Configurações centralizadas
│
├── services/              # Camada de serviços
│   ├── __init__.py
│   ├── api_client.py     # Cliente HTTP para APIs
│   ├── data_processor.py # Processamento de dados
│   └── file_handler.py   # Manipulação de arquivos
│
├── utils/                 # Utilitários
│   ├── __init__.py
│   ├── logger.py         # Sistema de logs
│   └── validators.py     # Validações de dados
│
├── data/                  # Dados de saída (gitignored)
│
├── Dockerfile            # Containerização
├── docker-compose.yml    # Orquestração
├── requirements.txt      # Dependências Python
└── README.md            # Este arquivo
```

## 🎯 Funcionalidades

- ✅ Coleta de dados da API JSONPlaceholder (users)
- ✅ Validação robusta de dados
- ✅ Processamento e filtragem inteligente
- ✅ Exportação para Excel (.xlsx)
- ✅ Geração de resumo estatístico (JSON)
- ✅ Sistema de logs detalhado
- ✅ Controle de horário de execução
- ✅ Containerização com Docker

## 🔧 Requisitos

### Opção 1: Execução Local

- Python 3.11+
- pip

### Opção 2: Execução com Docker

- Docker 20.10+
- Docker Compose 2.0+

## 📦 Instalação e Execução

### Método 1: Execução Local

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Executar aplicação
python app/main.py
```

### Método 2: Docker (Recomendado)

```bash
# 1. Build da imagem
docker-compose build

# 2. Executar container
docker-compose up app

# 3. Para modo desenvolvimento
docker-compose --profile dev up app-dev
```

### Método 3: Docker direto

```bash
# Build
docker build -t data-collector:2.0 .

# Run
docker run -v $(pwd)/data:/app/data data-collector:2.0
```

## ⚙️ Configuração

### Variáveis de Ambiente

| Variável    | Descrição            | Padrão              | Valores                                |
| ----------- | -------------------- | ------------------- | -------------------------------------- |
| `APP_ENV`   | Ambiente de execução | `production`        | `development`, `staging`, `production` |
| `LOG_LEVEL` | Nível de log         | `INFO`              | `DEBUG`, `INFO`, `WARNING`, `ERROR`    |
| `TZ`        | Timezone             | `America/Sao_Paulo` | Qualquer timezone válido               |

### Exemplo de uso:

```bash
# Linux/Mac
export APP_ENV=development
export LOG_LEVEL=DEBUG
python app/main.py

# Windows CMD
set APP_ENV=development
set LOG_LEVEL=DEBUG
python app/main.py

# Windows PowerShell
$env:APP_ENV="development"
$env:LOG_LEVEL="DEBUG"
python app/main.py
```

## 📊 Saída de Dados

### Arquivo Excel (`data/dados_processados.xlsx`)

Contém os dados processados com colunas:

- `id`: ID do usuário
- `name`: Nome completo
- `username`: Nome de usuário
- `email`: Email
- `phone`: Telefone
- `website`: Website
- `data_processamento`: Timestamp do processamento
- `ambiente`: Ambiente de execução
- `validado`: Flag de validação

### Resumo JSON (`data/summary.json`)

Estatísticas do processamento:

- Total de registros
- Colunas processadas
- Registros válidos
- Data/hora do processamento
- Ambiente

## 🐛 Desafio de Debugging

Este código contém **bugs intencionais** para teste de habilidades de debugging:

### 🎯 Bugs a Encontrar:

1. **Bug Crítico**: Impede a execução em ambiente de produção
2. **Bugs Ocultos**: Causam falhas em casos específicos
3. **Bugs Sutis**: Difíceis de detectar, aparecem apenas em condições especiais

### 📝 Tarefa:

1. Execute a aplicação
2. Identifique todos os bugs
3. Corrija cada um
4. Documente:
   - O que era o bug
   - Como identificou
   - Como corrigiu
   - Como testou a correção

## 🔍 Dicas de Debugging

- Analise as variáveis de ambiente
- Verifique validações de dados
- Observe logs com atenção
- Teste com diferentes ambientes (development vs production)
- Analise o código de validação de dados
- Verifique dependências no `requirements.txt`

## 📚 API Utilizada

**JSONPlaceholder** - API REST fake para testes

- Base URL: `https://jsonplaceholder.typicode.com`
- Endpoint: `/users`
- Retorna: 10 usuários fictícios
- Docs: https://jsonplaceholder.typicode.com/

## 🧪 Testes

```bash
# Executar em modo debug
LOG_LEVEL=DEBUG python app/main.py

# Executar em modo desenvolvimento (ignora horário)
APP_ENV=development python app/main.py

# Ver logs detalhados no Docker
docker-compose logs -f app
```

## 📖 Estrutura de Logs

```
2025-10-07 14:00:00 - app.main - INFO - Iniciado em: 2025-10-07 14:00:00
2025-10-07 14:00:00 - app.scheduler - INFO - ✓ Horário permitido: 14:00
2025-10-07 14:00:01 - services.api_client - INFO - Buscando dados da API
...
```

## ⏰ Horário de Execução

Por padrão, o sistema executa apenas às **14:00**.

Para testar em outro horário, defina `APP_ENV=development` ou modifique `HORARIO_EXECUCAO` no `config/settings.py`.

## 🤝 Contribuindo

Este é um projeto de avaliação técnica. Para melhorias:

1. Identifique e corrija bugs
2. Documente mudanças
3. Mantenha a arquitetura modular
4. Adicione testes se necessário

## 📄 Licença

Projeto educacional para avaliação técnica.

---

**Versão:** 2.0.0  
**Atualizado:** 2025-10-07  
**Contato:** Sistema de Avaliação Técnica

Boa sorte no debugging! 🚀🐛
