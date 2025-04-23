def compare_results(actual_output: dict, expected_output: dict) -> bool:
    # Aqui você pode comparar por partes, como stdout ou returncode
    return (
        actual_output.get("returncode") == expected_output.get("returncode")
        and expected_output.get("error_contains", "") in actual_output.get("stderr", "")
    )
