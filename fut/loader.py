import yaml

def load_test_file(file_path):
    """
    Lê um arquivo .yml contendo as definições de teste.
    Retorna:
        dict: Um dicionário com os dados do teste, ou None se falhar.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # Garante que o loader não retorne None para arquivos vazios, 
            # retornando um dicionário vazio em vez disso.
            data = yaml.safe_load(f) or {}
        return data
    except Exception as e:
        # Se houver qualquer erro, ele será impresso no console do servidor
        # e a função retornará None, que o servidor sabe como tratar.
        print(f"Erro ao carregar o arquivo YAML '{file_path}': {e}")
        return None
