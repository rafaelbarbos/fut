import argparse
from fut.loader import load_test_file
from fut.executor import execute_validation
from fut.comparator import compare_results
from fut.reporter import generate_report

def main():
    parser = argparse.ArgumentParser(description="Validador FHIR CLI")
    parser.add_argument("test_file", help="Arquivo YAML com os testes")
    parser.add_argument("--report", choices=["txt", "json"], default="txt", help="Formato do relatório")
    args = parser.parse_args()

    # 1. Carrega dados do arquivo YAML
    test_data = load_test_file(args.test_file)
    print("[INFO] Teste carregado:", test_data.get("test_id", "ID não encontrado"))
    print("[INFO] Descrição:", test_data.get("description", "Sem descrição"))

    # 2. Executa o validator_cli
    instance_path = test_data.get("instance_path")
    output = execute_validation(instance_path)
    print("[INFO] Resultado real:", output)

    # 3. Compara com o esperado
    expected = test_data.get("expected_results", {})
    success = compare_results(output, expected)
    print("[INFO] Comparação:", "OK" if success else "FALHOU")

    # 4. Gera relatório
    generate_report(output, report_type=args.report)

if __name__ == "__main__":
    main()
