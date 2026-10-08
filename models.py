# Importar a instancia do banco 'db' criada no arquivo database.py
from database import db


# Definir a classe que ira realizar todo o mapeamento da minha tabela
class Categoria(db.Model):
    # Define o nome da minha tabela
    __tablename__ = 'categoria'

    # Define os campos da minha tabela
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    descricao = db.Column(db.String(200), nullable=False)
    registro = db.relationship('Registro', backref='categoria', lazy=True)



# Definir a classe que ira realizar todo o mapeamento da minha tabela
class Registro(db.Model):
    
    # Define o nome da minha tabela
    __tablename__ = 'registro'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    info = db.Column(db.String(200), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='Pendente')

    imagem = db.Column(db.String(255), nullable=True, default='padrao.png')
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
