import yaml

def load_test_file(file_path):
    """
    Lê um arquivo .yml contendo as definições de teste.

    Retorna:
        dict: Um dicionário com os dados do teste.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data
