# Dentro de fut/executor.py
import subprocess
import os

# Modifique a assinatura da função para aceitar local_resource_paths
def execute_validation(instance_path, local_resource_paths=None):
    """
    Executa a validação para um arquivo de instância FHIR.

    Args:
        instance_path (str): Caminho para o arquivo de instância JSON
        local_resource_paths (list, optional): Lista de caminhos para arquivos de 
                                               recursos de conformidade locais (ex: perfis).
                                               Defaults to None.

    Returns:
        dict: Resultado da validação
    """
    print(f"[Executor] Validando {instance_path}...") #
    if local_resource_paths:
        print(f"[Executor] Utilizando recursos locais: {', '.join(local_resource_paths)}")

    # ... (lógica de correção de caminho e verificação de existência do arquivo) ...
    if not os.path.exists(instance_path): #
        raise FileNotFoundError(f"Arquivo não encontrado: {instance_path}") #

    output_file = "output.json" #

    # Monta o comando base
    command = [
        "java", "-jar", "validator_cli/validator_cli.jar", #
        "-version", "4.0.1", #
        "-output", output_file #
    ]

    # Adiciona os IGs/recursos locais ao comando
    if local_resource_paths:
        for resource_path in local_resource_paths:
            # Verifica se o recurso local existe antes de adicioná-lo
            if os.path.exists(resource_path):
                command.extend(["-ig", resource_path])
            else:
                print(f"[AVISO] Recurso local não encontrado e não será incluído: {resource_path}")

    # Adiciona o arquivo de instância a ser validado
    command.append(instance_path)

    print(f"[Executor] Executando comando: {' '.join(command)}")

    result = subprocess.run(
        command,
        capture_output=True, #
        text=True #
    )

    return { #
        "stdout": result.stdout, #
        "stderr": result.stderr, #
        "returncode": result.returncode, #
        "output_file": output_file, #
        "instance_path": instance_path #
    }