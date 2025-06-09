# Arquivo: fut/comparator.py

import json

def load_operation_outcome(output_filepath):
    """Carrega o arquivo JSON do OperationOutcome."""
    try:
        with open(output_filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"[ERRO-COMPARADOR] Não foi possível carregar ou ler o arquivo '{output_filepath}': {e}")
        return None

def check_issues(expected_issues: list, actual_issues: list, issue_type: str) -> bool:
    """
    Verifica se as issues (erros, avisos) esperadas correspondem às reais.
    """
    # 1. Compara a quantidade de issues
    if len(expected_issues) != len(actual_issues):
        print(f"[FALHA-COMPARAÇÃO] Quantidade de '{issue_type}' não bate. Esperado: {len(expected_issues)}, Real: {len(actual_issues)}")
        return False

    # 2. Se não há issues esperadas e nem reais, está tudo certo.
    if not expected_issues and not actual_issues:
        return True

    # 3. Compara o conteúdo de cada issue esperada
    for expected in expected_issues:
        expected_text = expected.get('description_contains', '')
        if not any(expected_text in actual.get('details', {}).get('text', '') for actual in actual_issues):
            print(f"[FALHA-COMPARAÇÃO] '{issue_type}' esperado não encontrado: '{expected_text}'")
            return False
            
    return True

def compare_results(actual_output: dict, expected_output: dict) -> bool:
    """
    Compara o OperationOutcome real com os resultados esperados do YAML.
    'actual_output' é o dicionário retornado pelo executor.py.
    'expected_output' é o dicionário 'expected_results' do YAML.
    """
    op_outcome = load_operation_outcome(actual_output.get('output_file'))
    if not op_outcome:
        return False

    actual_issues = op_outcome.get('issue', [])
    
    # Separa as issues reais por severidade
    actual_errors = [issue for issue in actual_issues if issue.get('severity') == 'error']
    actual_warnings = [issue for issue in actual_issues if issue.get('severity') == 'warning']

    # Pega as listas de erros e avisos esperados do YAML
    expected_errors = expected_output.get('errors', [])
    expected_warnings = expected_output.get('warnings', [])

    # Compara erros e avisos
    errors_ok = check_issues(expected_errors, actual_errors, 'erros')
    warnings_ok = check_issues(expected_warnings, actual_warnings, 'avisos')

    if errors_ok and warnings_ok:
        print("[SUCESSO-COMPARAÇÃO] O resultado da validação corresponde ao esperado.")
        return True
    else:
        return False