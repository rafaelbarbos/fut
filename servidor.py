# Arquivo: servidor.py
from flask import Flask, jsonify, request, render_template
import os
import glob
import json
import yaml
from fut.core import run_test
from fut.loader import load_test_file

app = Flask(__name__, template_folder='templates')

# --- Função de Segurança ---
def is_safe_path(path):
    """Verifica se o caminho do arquivo está dentro das pastas permitidas."""
    allowed_dirs = ['tests', 'instancias', 'perfis_locais']
    try:
        # Resolve o caminho real para evitar ataques de diretório (ex: ../../)
        real_path = os.path.realpath(path)
        # Verifica se o caminho real começa com o caminho de uma das pastas permitidas
        return any(real_path.startswith(os.path.realpath(d)) for d in allowed_dirs)
    except:
        return False

# --- Rotas da API ---

@app.route('/')
def index():
    """Serve a página HTML principal."""
    return render_template('index.html')

@app.route('/api/files')
def list_files():
    """Lista todos os arquivos relevantes do projeto."""
    tests = sorted([os.path.basename(f) for f in glob.glob("tests/*.yml")])
    instances = sorted([os.path.basename(f) for f in glob.glob("instancias/*.json")])
    profiles = sorted([os.path.basename(f) for f in glob.glob("perfis_locais/*.json")])
    return jsonify({'tests': tests, 'instances': instances, 'profiles': profiles})

@app.route('/api/file_content')
def get_file_content():
    """Lê e retorna o conteúdo de um arquivo de texto."""
    file_path = request.args.get('path')
    if not is_safe_path(file_path):
        return jsonify({"error": "Acesso negado"}), 403
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return jsonify({"content": content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/save_file', methods=['POST'])
def save_file():
    """Salva (cria ou atualiza) o conteúdo de um arquivo."""
    data = request.json
    file_path = data.get('path')
    content = data.get('content')
    if not is_safe_path(file_path):
        return jsonify({"error": "Acesso negado"}), 403
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return jsonify({"success": True, "message": f"Arquivo '{os.path.basename(file_path)}' salvo."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/delete_file', methods=['POST'])
def delete_file():
    """Deleta um arquivo."""
    data = request.json
    file_path = data.get('path')
    if not is_safe_path(file_path):
        return jsonify({"error": "Acesso negado"}), 403
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({"success": True, "message": f"Arquivo '{os.path.basename(file_path)}' deletado."})
        else:
            return jsonify({"error": "Arquivo não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/run_test', methods=['POST'])
def handle_run_test():
    """Executa um teste."""
    data = request.json
    test_path = data.get('path')
    if not is_safe_path(test_path):
        return jsonify({"error": "Acesso negado"}), 403
    try:
        result = run_test(test_path)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Falha na execução do teste: {e}"}), 500

@app.route('/api/test_detail')
def get_test_detail():
    """Retorna o conteúdo de um arquivo de teste YAML como JSON."""
    test_path = request.args.get('path')
    if not is_safe_path(test_path):
        return jsonify({"error": "Acesso negado"}), 403
    if not os.path.exists(test_path):
        return jsonify({"error": "Arquivo não encontrado"}), 404
    try:
        data = load_test_file(test_path)
        if data is None:
            return jsonify({"error": "Arquivo YAML está vazio ou mal formatado"}), 400
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/history')
def get_history():
    """Lista todos os relatórios salvos no histórico."""
    try:
        if not os.path.exists("historico_relatorios"): return jsonify([])
        history_dirs = sorted([d for d in os.listdir("historico_relatorios") if os.path.isdir(os.path.join("historico_relatorios", d))], reverse=True)
        return jsonify(history_dirs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/report')
def get_report():
    """Retorna os detalhes de um relatório específico do histórico."""
    report_dir_name = request.args.get('dir')
    report_dir = os.path.join("historico_relatorios", report_dir_name)
    try:
        with open(os.path.join(report_dir, "summary.json"), 'r', encoding='utf-8') as f:
            summary = json.load(f)
        with open(os.path.join(report_dir, "output.json"), 'r', encoding='utf-8') as f:
            op_outcome = json.load(f)
        return jsonify({"summary": summary, "operation_outcome": op_outcome})
    except Exception as e:
        return jsonify({"error": f"Erro ao carregar relatório: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)