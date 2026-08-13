from flask import Flask, render_template, request

# Instancia do servidor do Flask
app = Flask(__name__)

#Rota 1: Pagina inicial
@app.route('/')
def home():
    return render_template("index.html")

#Rota 2: Exibição da tela de cadastro Método (GET)
@app.route('/cadastro')
def pagina_cadastro():
    return render_template("cadastro.html")

#Rota 3:Processamento dos dados Método (POST)
@app.route('/salvar', methods=["POST"])
def salvar_cadastro():
    nome_digitado = request.form.get("campo_nome")
    info_digitado = request.form.get("campo_info")

    return render_template("resultado.html", nome=nome_digitado, info=info_digitado)


if __name__ == '__main__':
    app.run(debug=True)
