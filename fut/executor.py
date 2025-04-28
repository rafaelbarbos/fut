import subprocess
import os
from fut.loader import load_test_file

def execute_validation(yml_path):
    print(f"[Executor] Validando {yml_path}...")

    # 1. Carregar o teste YAML
    test_data = load_test_file(yml_path)

    # 2. Descobrir qual arquivo JSON deve ser validado
    instance_path = test_data.get('instance_path')

    if not instance_path:
        # Regra: procurar nome do .yml + '.json'
        instance_path = yml_path.replace('.yml', '.json')
        if not os.path.exists(instance_path):
            # Ou procurar pelo test_id
            test_id = test_data.get('test_id')
            instance_path = f"{test_id}.json"
            if not os.path.exists(instance_path):
                raise FileNotFoundError(f"Instância não encontrada para o teste {yml_path}.")

    # 3. Rodar o validator_cli
    output_file = "output.json"
    result = subprocess.run(
        ["java", "-jar", "validator_cli/validator_cli.jar", "-version", "4.0.1", "-output", output_file, instance_path],
        capture_output=True,
        text=True
    )

    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode,
        "output_file": output_file,  # novo: pra depois ler o resultado
        "test_data": test_data        # já devolve os dados do teste
    }
