import os
import json
import shutil
from datetime import datetime

def run_test(yaml_file_path:str)-> dict:
    # ... (lógica existente de carregar, executar, comparar) ...

    # --- LÓGICA DE HISTÓRICO ---
    # Cria um nome de pasta único com data e hora
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    test_id = test_data.get("test_id", "teste_desconhecido")
    history_dir = os.path.join("historico_relatorios", f"{timestamp}_{test_id}")
    os.makedirs(history_dir, exist_ok=True)

    # Salva o resultado da comparação, o output do validador, etc.
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

    # ... (retorna o dicionário de resultado como antes) ...
    # Adiciona o caminho do histórico ao resultado para uso na interface
    result["history_dir"] = history_dir 
    return result