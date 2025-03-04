const usuarios = { admin: "1234", diego: "senha123" }; // Exemplo de usuários
let registros = JSON.parse(localStorage.getItem('registros')) || [];

// Função para lidar com a tecla Enter
function handleEnter(e) {
  if (e.key === 'Enter') login();
}

// Função de login
function login() {
  const user = document.getElementById('username').value;
  const pass = document.getElementById('password').value;

  if (usuarios[user] === pass) {
    document.getElementById('login').style.display = 'none';
    document.getElementById('app').style.display = 'block';
    carregarRegistros();
  } else {
    alert('Usuário ou senha inválidos!');
  }
}

// Função para registrar entrada
function registrarEntrada() {
  const tipo = document.getElementById('tipoTrabalho').value;
  if (!tipo) return alerta('Selecione o tipo de trabalho.');

  if (verificaEntradaSemSaida(tipo)) {
    return alerta(`Já existe entrada para ${tipo} sem saída.`);
  }

  const horario = new Date().toLocaleString('pt-BR');
  registros.push({ tipo, horario, acao: 'Entrada' });
  salvarEAtualizar();
}

// Função para registrar saída
function registrarSaida() {
  const tipo = document.getElementById('tipoTrabalho').value;
  if (!tipo) return alerta('Selecione o tipo de trabalho.');

  if (!verificaUltimaEntrada(tipo)) {
    return alerta(`Nenhuma entrada encontrada para ${tipo}.`);
  }

  const horario = new Date().toLocaleString('pt-BR');
  registros.push({ tipo, horario, acao: 'Saída' });
  salvarEAtualizar();
}

// Verifica se há uma entrada sem saída para o tipo de trabalho
function verificaEntradaSemSaida(tipo) {
  const entradas = registros.filter(r => r.tipo === tipo && r.acao === 'Entrada');
  const saidas = registros.filter(r => r.tipo === tipo && r.acao === 'Saída');
  return entradas.length > saidas.length;
}

// Verifica se há uma entrada pendente para o tipo de trabalho
function verificaUltimaEntrada(tipo) {
  const entradas = registros.filter(r => r.tipo === tipo && r.acao === 'Entrada');
  const saidas = registros.filter(r => r.tipo === tipo && r.acao === 'Saída');
  return entradas.length > saidas.length;
}

// Salva os registros no localStorage e atualiza a interface
function salvarEAtualizar() {
  localStorage.setItem('registros', JSON.stringify(registros));
  carregarRegistros();
}

// Carrega os registros na interface
function carregarRegistros() {
  const ul = document.getElementById('registros');
  ul.innerHTML = '';

  registros.forEach(r => {
    const li = document.createElement('li');
    li.textContent = `${r.tipo} - ${r.acao} - ${r.horario}`;
    ul.appendChild(li);
  });

  calcularTotalDia();
}

// Calcula o total de horas trabalhadas no dia
function calcularTotalDia() {
  let minutosTotais = 0;

  ['Elétrica', 'Hidraulica', 'ManutencaoCivil'].forEach(tipo => {
    const entradas = registros.filter(r => r.tipo === tipo && r.acao === 'Entrada');
    const saidas = registros.filter(r => r.tipo === tipo && r.acao === 'Saída');

    entradas.forEach((entrada, index) => {
      if (saidas[index]) {
        const inicio = new Date(entrada.horario);
        const fim = new Date(saidas[index].horario);
        minutosTotais += (fim - inicio) / 60000;
      }
    });
  });

  const horas = Math.floor(minutosTotais / 60);
  const minutos = Math.floor(minutosTotais % 60);
  document.getElementById('totalDia').textContent = `${horas}h${minutos}min`;
}

// Gera um PDF com os registros
function gerarPDF() {
  const doc = new jsPDF();
  doc.setFontSize(16);
  doc.text('Registros de Ponto', 10, 10);
  doc.setFontSize(12);

  registros.forEach((r, i) => {
    doc.text(`${r.tipo} - ${r.acao} - ${r.horario}`, 10, 20 + (i * 10));
  });

  doc.save('RegistroPonto.pdf');
}

// Exibe uma mensagem de aviso
function alerta(msg) {
  const aviso = document.getElementById('aviso');
  aviso.textContent = msg;
  aviso.style.display = 'block';
  setTimeout(() => aviso.style.display = 'none', 4000);
}
