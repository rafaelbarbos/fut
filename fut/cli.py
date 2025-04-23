import argparse
from fut.executor import execute_validation
from fut.reporter import generate_report

def main():
    parser = argparse.ArgumentParser(description="FHIR Validator CLI")
    parser.add_argument("input_file", help="Arquivo .yml com os dados de teste")
    parser.add_argument("--report", help="Tipo de relatório (json, txt)", default="txt")
    args = parser.parse_args()

    print("[CLI] Iniciando validação...")

    results = execute_validation(args.input_file)
    generate_report(results, args.report)

if __name__ == "__main__":
    main()
