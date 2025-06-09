# Arquivo: interface.py
import streamlit as st
import os
import glob
import json
from fut.core import run_test # Importa a função refatorada

# --- Funções de Apoio ---
def display_report(report_dir):
    """Função para mostrar um relatório de um diretório de histórico."""
    try:
        with open(os.path.join(report_dir, "summary.json"), 'r') as f:
            summary = json.load(f)
        with open(os.path.join(report_dir, "output.json"), 'r') as f:
            op_outcome = json.load(f)

        if summary["comparison_success"]:
            st.success(f"✅ Teste Aprovado (Executado em: {summary['timestamp']})")
        else:
            st.error(f"❌ Teste Reprovado (Executado em: {summary['timestamp']})")

        st.metric("ID do Teste", summary.get('test_id', 'N/A'))
        st.caption(summary.get('description', ''))
        
        with st.expander("Ver OperationOutcome completo"):
            st.json(op_outcome)
    except FileNotFoundError:
        st.error(f"Relatório incompleto ou corrompido em '{report_dir}'")

# --- Configuração da Página e Barra Lateral (Sidebar) ---
st.set_page_config(page_title="FHIRUT", layout="wide")

st.sidebar.title("FHIRUT  Workbench")
app_mode = st.sidebar.selectbox(
    "Selecione a Ação",
    ["Executar Teste", "Gerenciar Arquivos", "Histórico de Relatórios"]
)

# --- LÓGICA DE CADA PÁGINA ---

if app_mode == "Executar Teste":
    st.title("🔬 Executar um Novo Teste de Validação")
    uploaded_file = st.file_uploader("Selecione o arquivo de teste YAML", type=['yml', 'yaml'])

    if uploaded_file:
        # Salva o arquivo temporariamente para execução
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        if st.button("Executar Teste", type="primary"):
            with st.spinner("Executando validação..."):
                result = run_test(uploaded_file.name)
            
            # Mostra o relatório do teste que acabou de rodar
            display_report(result["history_dir"])


elif app_mode == "Gerenciar Arquivos":
    st.title("🗂️ Gerenciar Arquivos do Projeto")
    
    tab_tests, tab_instances, tab_profiles = st.tabs(["Casos de Teste", "Instâncias", "Perfis"])

    # Aba de Gerenciamento de Testes
    with tab_tests:
        st.subheader("Adicionar ou Excluir Casos de Teste (.yml)")
        # Adicionar
        new_test_file = st.file_uploader("Adicionar novo teste", type=['yml', 'yaml'], key="upload_test")
        if new_test_file:
            with open(os.path.join("tests", new_test_file.name), "wb") as f:
                f.write(new_test_file.getbuffer())
            st.success(f"Arquivo de teste '{new_test_file.name}' adicionado!")
        
        # Excluir
        test_files = [os.path.basename(f) for f in glob.glob("tests/*.yml")]
        file_to_delete = st.selectbox("Selecione um teste para excluir", options=test_files, index=None)
        if file_to_delete and st.button("Excluir Teste Selecionado", type="secondary"):
            os.remove(os.path.join("tests", file_to_delete))
            st.success(f"Arquivo '{file_to_delete}' excluído!")
            st.rerun() # Atualiza a página

    # (Lógica similar para as abas de Instâncias e Perfis)
    with tab_instances:
        st.subheader("Adicionar ou Excluir Instâncias (.json)")
        # ... implementação semelhante a de testes ...

    with tab_profiles:
        st.subheader("Adicionar ou Excluir Perfis (.json)")
        # ... implementação semelhante a de testes ...


elif app_mode == "Histórico de Relatórios":
    st.title("📜 Histórico e Relatórios de Execução")
    
    history_dirs = sorted([d for d in os.listdir("historico_relatorios") if os.path.isdir(os.path.join("historico_relatorios", d))], reverse=True)
    
    if not history_dirs:
        st.info("Nenhum relatório encontrado no histórico.")
    else:
        selected_report = st.selectbox("Selecione um relatório para visualizar", options=history_dirs)
        if selected_report:
            display_report(os.path.join("historico_relatorios", selected_report))