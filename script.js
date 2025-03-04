// Dados de usuários (simplificado)
const usuarios = {
  "usuario1": "senha1",
  "usuario2": "senha2"
};

// Dados de horários (armazenados no localStorage)
let horarios = JSON.parse(localStorage.getItem("horarios")) || [];

// Valores por hora (não será mais usado, mas mantido para referência)
const VALORES_POR_HORA = {
  "Elétrica": 103.00,
  "Hidraulica": 97.00,
  "Manutenção Civil": 97.50
};

// Função de login
function login() {
  const username = document.getElementById("username").value;
  if (usuarios[username]) {
    document.getElementById("login").style.display = "none";
    document.getElementById("app").style.display = "block";
    carregarRegistros();
  } else {
    alert("Usuário inválido!");
  }
}

// Registrar entrada
function registrarEntrada() {
  const tipoTrabalho = document.getElementById("tipoTrabalho").value;
  const horario = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }); // Remove os segundos
  horarios.push({ tipo: "Entrada", horario, tipoTrabalho });
  localStorage.setItem("horarios", JSON.stringify(horarios));
  carregarRegistros();
}

// Registrar saída
function registrarSaida() {
  const tipoTrabalho = document.getElementById("tipoTrabalho").value;
  const horario = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }); // Remove os segundos
  horarios.push({ tipo: "Saída", horario, tipoTrabalho });
  localStorage.setItem("horarios", JSON.stringify(horarios));
  carregarRegistros();
  calcularTotal();
}

// Carregar registros na tela
function carregarRegistros() {
  const lista = document.getElementById("registros");
  lista.innerHTML = horarios.map(h => `<li>${h.tipo} (${h.tipoTrabalho}): ${h.horario}</li>`).join("");
}

// Calcular total de horas (sem segundos e sem valor total)
function calcularTotal() {
  const entradas = horarios.filter(h => h.tipo === "Entrada");
  const saidas = horarios.filter(h => h.tipo === "Saída");

  let totalMinutos = 0;

  for (let i = 0; i < entradas.length; i++) {
    const entrada = new Date(`1970-01-01T${entradas[i].horario}:00`);
    const saida = new Date(`1970-01-01T${saidas[i].horario}:00`);
    const diferenca = saida - entrada;
    const minutos = diferenca / 60000; // Converter milissegundos para minutos
    totalMinutos += minutos;
  }

  const horas = Math.floor(totalMinutos / 60);
  const minutos = Math.floor(totalMinutos % 60);

  document.getElementById("total").innerHTML = `
    Horas trabalhadas: ${horas}h${minutos}min
  `;
}
