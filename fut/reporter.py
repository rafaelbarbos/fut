def generate_report(results, report_type="txt"):
    if report_type == "txt":
        with open("relatorio.txt", "w", encoding="utf-8") as f:
            f.write("==== FHIR VALIDATION REPORT ====\n")
            f.write(results["stdout"])
            f.write("\n==== FIM DO RELATÓRIO ====\n")
    elif report_type == "json":
        import json
        with open("relatorio.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4)
