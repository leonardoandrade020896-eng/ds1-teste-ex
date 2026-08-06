from flask import Flask

# Instancia do servidor do Flask
app = Flask(__name__)

#Rota 1: Pagina inicial
@app.route('/')
def home():
    return "<h1>Servidor Flask rodando</h1>" "<h1>Bem-vindo ao meu servidor Flask!</h1>"

#Rota 2: Sobre a aplicação
@app.route('/sobre')
def sobre():
    return "<h1>Sobre a função</h1>" "<p>Esta é uma simples aplicação Flask.</p>"

#Rota 3:Status da aplicação
@app.route('/status')
def status():
    return "<h1>Status da aplicação</h1>" "<p>O servidor Flask está rodando corretamente.</p>"

if __name__ == '__main__':
    app.run(debug=True)
