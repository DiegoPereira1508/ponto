// Dados de usuários (simplificado)
const usuarios = {
  "usuario1": "senha1",
  "usuario2": "senha2"
};

// Dados de horários (armazenados no localStorage)
let horarios = JSON.parse(localStorage.getItem("horarios")) || [];

// Valores por hora
const VALORES_POR_HORA = {
  "Elétrica": 103.00,
  "Manutenção Civil": 97.50,
  "Hidraulica": 97.00
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
  const horario = new Date().toLocaleTimeString();
  horarios.push({ tipo: "Entrada", horario });
  localStorage.setItem("horarios", JSON.stringify(horarios));
  carregarRegistros();
}

// Registrar saída
function registrarSaida() {
  const horario = new Date().toLocaleTimeString();
  horarios.push({ tipo: "Saída", horario });
  localStorage.setItem("horarios", JSON.stringify(horarios));
  carregarRegistros();
  calcularTotal();
}

// Carregar registros na tela
function carregarRegistros() {
  const lista = document.getElementById("registros");
  lista.innerHTML = horarios.map(h => `<li>${h.tipo}: ${h.horario}</li>`).join("");
}

// Calcular total de horas e valor
function calcularTotal() {
  const entradas = horarios.filter(h => h.tipo === "Entrada").map(h => new Date(`1970-01-01T${h.horario}`));
  const saidas = horarios.filter(h => h.tipo === "Saída").map(h => new Date(`1970-01-01T${h.horario}`));

  let totalMinutos = 0;
  for (let i = 0; i < entradas.length; i++) {
    const diferenca = saidas[i] - entradas[i];
    totalMinutos += diferenca / 60000; // Converter milissegundos para minutos
  }

  const horas = Math.floor(totalMinutos / 60);
  const minutos = Math.floor(totalMinutos % 60);
  const valor = (totalMinutos * (VALORES_POR_HORA["Elétrica"] / 60)).toFixed(2);

  document.getElementById("total").innerHTML = `
    Horas trabalhadas: ${horas}h${minutos}min<br>
    Valor a receber: R$ ${valor}
  `;
}