import subprocess
import os

def execute_validation(yml_path):
    print(f"[Executor] Validando {yml_path}...")

    # Exemplo simples com subprocess (pode adaptar conforme os args do .jar)
    result = subprocess.run(
        ["java", "-jar", "validator_cli/validator_cli.jar", yml_path],
        capture_output=True,
        text=True
    )
    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode
    }
