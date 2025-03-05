from flask import Flask, jsonify, render_template
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Configuração do Google Sheets
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDENTIALS_FILE = "credentials.json"  # Certifique-se de ter o arquivo correto
SPREADSHEET_NAME = "Quiz_chico"

def get_questions():
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPE)
    client = gspread.authorize(creds)
    sheet = client.open(SPREADSHEET_NAME).sheet1  # Primeira aba da planilha
    data = sheet.get_all_values()  # Obtém todas as células

    if len(data) < 2:
        return []  # Se não houver perguntas, retorna uma lista vazia

    questions = []
    for row in data[1:]:  # Ignora o cabeçalho (primeira linha)
        if len(row) >= 4:  # Garante que tenha pelo menos 4 colunas (pergunta + 3 respostas)
            pergunta = row[0]
            respostas = [row[1], row[2], row[3]]  # Resposta correta + erradas
            random.shuffle(respostas)  # Embaralha as respostas
            questions.append({
                "pergunta": pergunta,
                "opcoes": respostas,
                "resposta_correta": row[1]  # Mantém a referência da resposta correta
            })

    return questions

@app.route("/question")
def question():
    questions = get_questions()
    if not questions:
        return jsonify({"erro": "Nenhuma pergunta disponível"})

    question = random.choice(questions)
    return jsonify({
        "pergunta": question["pergunta"],
        "opcoes": question["opcoes"],
        "resposta_correta": question["resposta_correta"]
    })

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
    