Plano de Construção - FUT

    1. Definição e construção do documento de especificação de testes;
    1.1. Definição dos parâmetros;
    2. Tecnologia utilizada: Python. Será feita analise técnica referente às bibliotecas e ferramentas que
    serão utilizadas para os testes do FUT.
    3. Repartição da interface;
    4. Geração de relatórios;
    - Repositório: https://github.com/rafaelbarbos/fut
    - Os critérios de aceitação ainda serão definidos.
    - Comunicação via WhatsApp e Discord.

(FASE DE TESTES) COMO EXECUTAR
EXECUTE NO TERMINAL:
    1 - pip install -r requirements.txt

    2 - python main.py tests/patient-example.yml --report txt


ESTRUTURA ATUAL DO PROJETO
    fhirut/
    ├── fut/                        # Pacote principal do projeto
    │   ├── __init__.py
    │   ├── cli.py                  # Interface de linha de comando
    │   ├── loader.py               # Leitura e validação dos arquivos .yml
    │   ├── executor.py             # Execução do validator_cli
    │   ├── comparator.py           # Comparação entre output e resultados esperados
    │   ├── reporter.py             # Geração de relatórios
    │   └── utils.py                # Funções auxiliares
    ├── tests/
    │   └── patient-example.yml     # Exemplos de teste
    ├── validator_cli/              # JAR do validator e scripts relacionados
    │   └── validator_cli.jar
    ├── instances/                  # Instâncias FHIR de teste
    │   └── patient_example.json
    ├── valuesets/                 # ValueSets e outros artefatos
    │   └── my-valueset.json
    ├── instancias/                # Artefatos de conformidade adicionais
    ├── requirements.txt           # Dependências do projeto
    ├── README.md                  # Instruções de uso
    └── main.py                    # Arquivo principal para execução