# Arquivo: servidor.py
from flask import Flask, jsonify, request, render_template
import os
import glob
import json

# Importa as funções dos módulos do seu pacote 'fut'
from fut.core import run_test
from fut.loader import load_test_file # Importa a função de carregar arquivos YAML

# Inicializa a aplicação Flask
app = Flask(__name__, template_folder='templates')

# --- Rota Principal da Interface ---
@app.route('/')
def index():
    """Serve a página HTML principal da interface."""
    return render_template('index.html')

# --- API Endpoints ---

@app.route('/api/files')
def list_files():
    """Lista todos os arquivos relevantes do projeto."""
    tests = sorted([os.path.basename(f) for f in glob.glob("tests/*.yml")])
    instances = sorted([os.path.basename(f) for f in glob.glob("instancias/*.json")])
    profiles = sorted([os.path.basename(f) for f in glob.glob("perfis_locais/*.json")])
    
    return jsonify({
        'tests': tests,
        'instances': instances,
        'profiles': profiles
    })

@app.route('/api/test_detail')
def get_test_detail():
    """Retorna o conteúdo de um arquivo de teste YAML como JSON."""
    test_path = request.args.get('path')
    if not test_path or not os.path.exists(test_path):
        return jsonify({"error": "Arquivo não encontrado"}), 404
    
    try:
        # CORREÇÃO: Usa a função central 'load_test_file' para consistência
        data = load_test_file(test_path)
        if data is None:
            return jsonify({"error": "Arquivo YAML está vazio ou mal formatado"}), 400
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/run_test', methods=['POST'])
def handle_run_test():
    """Executa um teste e retorna o diretório do relatório."""
    data = request.json
    test_path = data.get('path')
    
    if not test_path or not os.path.exists(test_path):
        return jsonify({"error": "Caminho do teste inválido"}), 400
        
    try:
        result = run_test(test_path)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Falha na execução do teste: {e}"}), 500

@app.route('/api/history')
def get_history():
    """Lista todos os relatórios salvos no histórico."""
    try:
        if not os.path.exists("historico_relatorios"):
            return jsonify([])
            
        history_dirs = sorted(
            [d for d in os.listdir("historico_relatorios") if os.path.isdir(os.path.join("historico_relatorios", d))],
            reverse=True
        )
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
        
        return jsonify({
            "summary": summary,
            "operation_outcome": op_outcome
        })
    except Exception as e:
        return jsonify({"error": f"Erro ao carregar relatório: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
