# Importar a instancia do banco 'db' criada no arquivo database.py
from database import db

# Definir a classe que ira realizar todo o mapeamento da minha tabela
class Registro(db.Model):
    
    # Define o nome da minha tabela
    __tablename__ = 'registro'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    info = db.Column(db.String(200), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    status = db.column(db.String(20), default='Pendente')
