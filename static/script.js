// Arquivo: static/script.js

document.addEventListener('DOMContentLoaded', () => {
    
    const mainContent = document.getElementById('main-content');
    const modal = document.getElementById('editor-modal');
    const modalTitle = document.getElementById('modal-title');
    const modalTextarea = document.getElementById('modal-textarea');
    const modalSaveBtn = document.getElementById('modal-save-btn');
    const modalCancelBtn = document.getElementById('modal-cancel-btn');

    // --- LÓGICA DO MODAL DE EDIÇÃO ---
    function openModal(title, content, saveCallback) {
        modalTitle.textContent = title;
        modalTextarea.value = content;
        modal.classList.remove('hidden');
        
        const newSaveBtn = modalSaveBtn.cloneNode(true); // Recria o botão para evitar listeners duplicados
        modalSaveBtn.parentNode.replaceChild(newSaveBtn, modalSaveBtn);
        
        newSaveBtn.addEventListener('click', () => {
            saveCallback(modalTextarea.value);
            closeModal();
        });
    }

    function closeModal() {
        modal.classList.add('hidden');
    }
    modalCancelBtn.addEventListener('click', closeModal);

    // --- RENDERIZADORES DE TELA ---
    function showView(viewName) {
        document.querySelectorAll('nav a').forEach(el => el.classList.remove('active'));
        const activeLink = document.querySelector(`nav a[data-view='${viewName}']`);
        if(activeLink) activeLink.classList.add('active');

        if (viewName === 'dashboard') renderDashboard();
        else if (viewName === 'management') renderManagementView();
        else if (viewName === 'history') renderHistory();
    }

    // --- RENDERIZADOR DO PAINEL ---
    async function renderDashboard() {
        mainContent.innerHTML = `<h2 class="text-3xl font-bold text-white mb-6">Painel de Execução</h2>`;
        try {
            const response = await fetch('/api/files');
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const data = await response.json();
            let testOptions = data.tests.map(test => `<option value="tests/${test}">${test}</option>`).join('');
            
            mainContent.innerHTML += `
                <div class="card p-6 rounded-xl shadow-lg">
                    <h3 class="font-semibold text-lg mb-4">1. Selecione um Caso de Teste</h3>
                    <select id="test-selector" class="w-full p-2 rounded bg-gray-800 border border-gray-600 focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
                        <option value="">-- Selecione --</option>
                        ${testOptions}
                    </select>
                    <div id="test-details" class="mt-4 text-sm p-4 bg-gray-800 rounded-lg min-h-[80px]"></div>
                    <button id="run-test-btn" class="btn-primary text-white font-bold py-2 px-4 rounded-lg mt-4 w-full transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2" disabled>
                        <i class="ph-bold ph-play"></i>
                        <span>Executar Teste Selecionado</span>
                    </button>
                </div>
                <div id="result-area" class="mt-6"></div>
            `;
            attachDashboardListeners();
        } catch (error) {
            mainContent.innerHTML += `<div class="card p-4 text-red-400">Erro ao carregar arquivos de teste.</div>`;
            console.error(error);
        }
    }

    // --- RENDERIZADOR DO GERENCIADOR DE ARQUIVOS ---
    async function renderManagementView() {
        mainContent.innerHTML = `<h2 class="text-3xl font-bold text-white mb-6">Gerenciar Arquivos</h2>
            <div id="tabs" class="flex border-b border-gray-700">
                <button data-tab="tests" data-folder="tests" class="tab-btn px-4 py-2 text-lg font-semibold border-b-2 border-transparent">Testes (.yml)</button>
                <button data-tab="instances" data-folder="instancias" class="tab-btn px-4 py-2 text-lg font-semibold border-b-2 border-transparent">Instâncias (.json)</button>
                <button data-tab="profiles" data-folder="perfis_locais" class="tab-btn px-4 py-2 text-lg font-semibold border-b-2 border-transparent">Perfis (.json)</button>
            </div>
            <div id="tab-content" class="py-6"><div class="flex justify-center pt-8"><div class="loader"></div></div></div>
        `;

        const renderTabContent = async (tabName, folder) => {
            const tabContent = document.getElementById('tab-content');
            tabContent.innerHTML = `<div class="flex justify-center pt-8"><div class="loader"></div></div>`;
            try {
                const response = await fetch('/api/files');
                const data = await response.json();
                const files = data[tabName] || []; // CORREÇÃO APLICADA AQUI
                tabContent.innerHTML = `
                    <button class="btn-primary text-white font-bold py-2 px-4 rounded-lg mb-4 flex items-center gap-2" data-action="create" data-folder="${folder}">
                        <i class="ph-bold ph-plus-circle"></i> Novo Arquivo
                    </button>
                    <div class="space-y-3">
                        ${files.length > 0 ? files.map(file => `
                            <div class="card p-3 rounded-lg flex justify-between items-center">
                                <span class="font-mono flex items-center gap-2"><i class="ph-bold ph-file"></i>${file}</span>
                                <div>
                                    <button class="text-blue-400 hover:underline mr-4" data-action="edit" data-path="${folder}/${file}">Ver/Editar</button>
                                    <button class="text-red-400 hover:underline" data-action="delete" data-path="${folder}/${file}">Excluir</button>
                                </div>
                            </div>
                        `).join('') : '<p class="text-gray-400">Nenhum arquivo nesta categoria.</p>'}
                    </div>`;
            } catch (error) {
                tabContent.innerHTML = `<p class="text-red-400">Erro ao carregar arquivos.</p>`;
            }
        };
        
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                // CORREÇÃO: Mapeia o data-tab para a chave correta da API
                const tabKeyMap = { tests: 'tests', instancias: 'instances', perfis_locais: 'profiles' };
                const tabId = e.target.getAttribute('data-tab');
                const tabName = tabKeyMap[tabId];
                const folder = e.target.getAttribute('data-folder');

                document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('text-blue-500', 'border-blue-500'));
                e.target.classList.add('text-blue-500', 'border-blue-500');
                renderTabContent(tabName, folder);
            });
        });
        document.querySelector('.tab-btn[data-tab="tests"]').click();
    }
    
    // --- RENDERIZADOR DO HISTÓRICO ---
    async function renderHistory() {
        mainContent.innerHTML = `<h2 class="text-3xl font-bold text-white mb-6">Histórico de Relatórios</h2><div id="history-container"><div class="flex justify-center pt-8"><div class="loader"></div></div></div>`;
        try {
            const response = await fetch('/api/history');
            const historyList = await response.json();
            const container = document.getElementById('history-container');
            if (historyList.length === 0) {
                container.innerHTML = `<p>Nenhum relatório encontrado no histórico.</p>`;
                return;
            }
            let historyItems = '';
            for (const dirName of historyList) {
                const reportData = await fetch(`/api/report?dir=${dirName}`);
                if (!reportData.ok) continue;
                const report = await reportData.json();
                const successClass = report.summary.comparison_success ? 'border-green-500' : 'border-red-500';
                const icon = report.summary.comparison_success ? '<i class="ph-fill ph-check-circle text-green-400 text-2xl"></i>' : '<i class="ph-fill ph-x-circle text-red-400 text-2xl"></i>';
                historyItems += `
                    <details class="card rounded-lg border-l-4 ${successClass} overflow-hidden">
                        <summary class="p-4 cursor-pointer flex justify-between items-center">
                             <div class="flex items-center gap-4">
                                ${icon}
                                <div>
                                    <p class="font-bold">${report.summary.test_id}</p>
                                    <p class="text-sm text-gray-400">${report.summary.timestamp}</p>
                                </div>
                            </div>
                            <span class="text-sm text-blue-400 hover:underline">Ver Detalhes</span>
                        </summary>
                        <div class="p-4 bg-gray-800 border-t border-gray-600 details-content" data-dirname="${dirName}"></div>
                    </details>`;
            }
            container.innerHTML = `<div class="space-y-4">${historyItems}</div>`;
        } catch (error) {
            document.getElementById('history-container').innerHTML = `<div class="card p-4 text-red-400">Erro ao carregar o histórico.</div>`;
            console.error(error);
        }
    }
    
    // --- RENDERIZADOR DO RELATÓRIO ---
    function renderReport(container, report, title) {
        const successClass = report.summary.comparison_success ? 'text-green-400' : 'text-red-400';
        const successText = report.summary.comparison_success ? 'Teste Aprovado' : 'Teste Reprovado';
        let issuesHTML = '<p class="text-sm text-gray-400">Nenhuma issue encontrada.</p>';
        if(report.operation_outcome && report.operation_outcome.issue && report.operation_outcome.issue.length > 0) {
            issuesHTML = report.operation_outcome.issue.map(issue => `
                <div class="p-3 my-2 rounded-lg bg-gray-900">
                    <p class="font-mono text-sm"><strong class="capitalize ${issue.severity === 'error' ? 'text-red-400' : 'text-yellow-400'}">${issue.severity}:</strong> ${issue.details.text}</p>
                    <p class="text-xs text-gray-500 mt-1">Local: ${issue.expression ? issue.expression.join(', ') : 'N/A'}</p>
                </div>
            `).join('');
        }
        container.innerHTML = `
            <div class="card p-6 rounded-xl">
                ${title ? `<h3 class="font-semibold text-lg mb-4">${title}</h3>` : ''}
                <div class="p-4 rounded-lg ${report.summary.comparison_success ? 'bg-green-900/50' : 'bg-red-900/50'}">
                    <p class="font-bold text-lg ${successClass}">${successText}</p>
                    <p class="text-sm">${report.summary.description || 'Sem descrição.'}</p>
                </div>
                <div class="mt-4">
                    <h4 class="font-semibold mb-2">Detalhes da Validação (Issues):</h4>
                    ${issuesHTML}
                </div>
            </div>`;
    }

    // --- LISTENERS (GERENCIADORES DE EVENTOS) ---
    function attachDashboardListeners() {
        const selector = document.getElementById('test-selector');
        const detailsDiv = document.getElementById('test-details');
        const runBtn = document.getElementById('run-test-btn');

        if (!selector || !detailsDiv || !runBtn) return;

        selector.addEventListener('change', async (e) => {
            const testPath = e.target.value;
            detailsDiv.innerHTML = '';
            runBtn.disabled = true;
            if (!testPath) return;

            try {
                const response = await fetch(`/api/test_detail?path=${testPath}`);
                const data = await response.json();
                if (!response.ok) throw new Error(data.error || 'Falha ao buscar detalhes.');
                
                detailsDiv.innerHTML = `
                    <p><strong>Descrição:</strong> ${data.description || 'N/A'}</p>
                    <p class="mt-2"><strong>Instância:</strong> <code class="bg-gray-900 px-2 py-1 rounded">${data.instance_path || 'N/A'}</code></p>
                `;
                runBtn.disabled = false;
            } catch (error) {
                detailsDiv.innerHTML = `<p class="text-red-400">Erro ao carregar detalhes: ${error.message}</p>`;
            }
        });

        runBtn.addEventListener('click', async () => {
            const testPath = selector.value;
            if (!testPath) return;
            const resultArea = document.getElementById('result-area');
            resultArea.innerHTML = `<div class="card p-6 rounded-xl mt-6"><div class="flex items-center gap-4"><div class="loader"></div><p>Executando validação...</p></div></div>`;
            try {
                const response = await fetch('/api/run_test', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ path: testPath })
                });
                const result = await response.json();
                if (result.error) throw new Error(result.error);
                const reportData = await fetch(`/api/report?dir=${result.history_dir.split('/').pop().split('\\').pop()}`);
                const report = await reportData.json();
                renderReport(resultArea, report, "Resultado da Execução");
            } catch(error) {
                 resultArea.innerHTML = `<div class="card p-4 text-red-400">Erro ao executar o teste: ${error.message}</div>`;
            }
        });
    }

    mainContent.addEventListener('click', async (e) => {
        const button = e.target.closest('button[data-action]');
        if (button) {
            const action = button.getAttribute('data-action');
            const path = button.getAttribute('data-path');
            const folder = button.getAttribute('data-folder');
            
            if (action === 'edit') {
                const response = await fetch(`/api/file_content?path=${path}`);
                const data = await response.json();
                openModal(`Editando: ${path}`, data.content || '', async (newContent) => {
                    await fetch('/api/save_file', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({path, content: newContent}) });
                    document.querySelector('.tab-btn.text-blue-500')?.click();
                });
            } else if (action === 'create') {
                const fileName = prompt(`Digite o nome do novo arquivo (ex: meu-teste.yml):`);
                if (fileName) {
                    const newPath = `${folder}/${fileName}`;
                    openModal(`Criando: ${newPath}`, '', async (newContent) => {
                         await fetch('/api/save_file', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({path: newPath, content: newContent}) });
                         document.querySelector('.tab-btn.text-blue-500')?.click();
                    });
                }
            } else if (action === 'delete') {
                if (confirm(`Tem certeza que deseja excluir o arquivo '${path}'?`)) {
                    await fetch('/api/delete_file', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({path}) });
                    document.querySelector('.tab-btn.text-blue-500')?.click();
                }
            }
        }
    });

    mainContent.addEventListener('toggle', async (e) => {
        if (e.target.tagName === 'DETAILS') {
            const detailsContent = e.target.querySelector('.details-content');
            if (detailsContent && e.target.open && !detailsContent.innerHTML) {
                const dirName = detailsContent.dataset.dirname;
                detailsContent.innerHTML = `<div class="flex items-center gap-4"><div class="loader"></div> <p>Carregando detalhes...</p></div>`;
                const reportData = await fetch(`/api/report?dir=${dirName}`);
                const report = await reportData.json();
                renderReport(detailsContent, report, "");
            }
        }
    }, true);

    document.querySelectorAll('nav a').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            showView(e.currentTarget.getAttribute('data-view'));
        });
    });

    showView('dashboard');
});
