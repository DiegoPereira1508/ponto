from flask import Flask, request, jsonify
import sqlite3
import datetime
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)

# Configurações do banco de dados
DATABASE = 'registros.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS registros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                funcao TEXT NOT NULL,
                entrada TEXT NOT NULL,
                saida TEXT,
                valor TEXT
            )
        ''')
        db.commit()

@app.route('/registrar', methods=['POST'])
def registrar():
    data = request.json
    funcao = data.get('funcao')
    tipo = data.get('tipo')  # 'entrada' ou 'saida'

    if not funcao or not tipo:
        return jsonify({"status": "error", "message": "Dados incompletos"}), 400

    db = get_db()
    cursor = db.cursor()

    if tipo == 'entrada':
        entrada = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        cursor.execute('INSERT INTO registros (funcao, entrada) VALUES (?, ?)', (funcao, entrada))
        db.commit()
        return jsonify({"status": "success", "message": "Entrada registrada"}), 200

    elif tipo == 'saida':
        registro = cursor.execute('SELECT * FROM registros WHERE saida IS NULL ORDER BY id DESC LIMIT 1').fetchone()
        if not registro:
            return jsonify({"status": "error", "message": "Nenhuma entrada pendente"}), 400

        saida = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        entrada = datetime.datetime.strptime(registro['entrada'], "%Y-%m-%d %H:%M")
        saida_dt = datetime.datetime.strptime(saida, "%Y-%m-%d %H:%M")
        minutos_trabalhados = (saida_dt - entrada).seconds // 60
        valor_hora = 100  # Exemplo de valor por hora
        valor_trabalhado = (minutos_trabalhados / 60) * valor_hora

        cursor.execute('UPDATE registros SET saida = ?, valor = ? WHERE id = ?', (saida, f"R$ {valor_trabalhado:.2f}", registro['id']))
        db.commit()
        return jsonify({"status": "success", "message": "Saída registrada"}), 200

    return jsonify({"status": "error", "message": "Tipo inválido"}), 400

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
