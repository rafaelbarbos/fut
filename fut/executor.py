import subprocess
import os

def execute_validation(instance_path):
    """
    Executa a validação para um arquivo de instância FHIR.
    
    Args:
        instance_path (str): Caminho para o arquivo de instância JSON
        
    Returns:
        dict: Resultado da validação
    """
    print(f"[Executor] Validando {instance_path}...")
    
    # Verificar se o caminho contém "instances" e corrigir para "instancias" se necessário
    if "instances/" in instance_path:
        corrected_path = instance_path.replace("instances/", "instancias/")
        if os.path.exists(corrected_path):
            print(f"[AVISO] Caminho corrigido de {instance_path} para {corrected_path}")
            instance_path = corrected_path
    
    # Verificar se o arquivo existe
    if not os.path.exists(instance_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {instance_path}")
    
    # Rodar o validator_cli
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
        "output_file": output_file,
        "instance_path": instance_path  # Inclui o caminho no resultado
    }