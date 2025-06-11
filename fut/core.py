# Arquivo: fut/core.py
import os
import json
import shutil
from datetime import datetime

from .loader import load_test_file
from .executor import execute_validation
from .comparator import compare_results

def run_test(yaml_file_path: str) -> dict:
    """
    Executa um único caso de teste, salva o resultado no histórico e retorna um
    dicionário com os detalhes da execução.
    """
    test_data = load_test_file(yaml_file_path)
    if not test_data:
        raise ValueError(f"Falha ao carregar ou o arquivo de teste '{yaml_file_path}' está vazio.")

    instance_path = test_data.get("instance_path")
    if not instance_path:
        raise ValueError(f"O campo 'instance_path' não foi encontrado no arquivo de teste '{yaml_file_path}'.")
        
    local_resources = test_data.get("context", {}).get("resources", [])
    validation_output = execute_validation(instance_path, local_resource_paths=local_resources)

    expected_results = test_data.get("expected_results", {})
    comparison_success = compare_results(validation_output, expected_results)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    test_id = test_data.get("test_id", "teste_desconhecido")
    
    if not os.path.exists("historico_relatorios"):
        os.makedirs("historico_relatorios")
        
    history_dir = os.path.join("historico_relatorios", f"{timestamp}_{test_id}")
    os.makedirs(history_dir, exist_ok=True)

    try:
        shutil.copyfile(validation_output['output_file'], os.path.join(history_dir, "output.json"))
        shutil.copyfile(yaml_file_path, os.path.join(history_dir, "test_case.yml"))

        summary = {
            "test_id": test_id,
            "description": test_data.get("description"),
            "comparison_success": comparison_success,
            "timestamp": timestamp
        }
        with open(os.path.join(history_dir, "summary.json"), 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=4)
    except Exception as e:
        print(f"AVISO: Falha ao salvar artefatos do histórico: {e}")

    result = {
        "test_id": test_data.get("test_id"),
        "description": test_data.get("description"),
        "instance_path": instance_path,
        "comparison_success": comparison_success,
        "validation_output": validation_output,
        "expected_results": expected_results,
        "history_dir": history_dir
    }
    
    return result
