import os

from flask import Flask

from database import db
from routes import main_bp

# Instancia do servidor do Flask
app = Flask(__name__)


# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'chave_secreta_etec_ds1_2026'

# Configuração para receber os uploads
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')

# Configuração para limitar o tamanho máximo do arquivo de upload (5 MB)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

# Inicializa a instancia do banco de dados com a aplicação Flask
db.init_app(app)

# Registra o blueprint principal da aplicação
app.register_blueprint(main_bp)

# Cria automaticamente a pasta de upload caso não exista
with app.app_context():
    # Cria a pasta de upload caso não exista
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Cria as tabelas do banco de dados caso não existam
    db.create_all()


# Inicia o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
