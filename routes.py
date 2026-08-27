from flask import Blueprint, render_template, request, redirect
from database import db
from models import Registro

# Criar o modulo principal das rotas
main_bp = Blueprint('main', __name__)

# Rota 1: Pagina Inicial
@main_bp.route("/")
def home():
    # Captura toda palavra digitada no campo busca
    busca = request.args.get("busca", "").strip().lower()

    if busca:
        registros = Registro.query.filter(Registro.nome.ilike(f"%{busca}")).all()
    else:
        registros = Registro.query.all()

    total_registros = len(registros)
    total_faturamento = sum(item.valor for item in registros)
    total_concluidos = sum(1 for item in registros if item.status == "Concluido")

    # Renderizar o index.html passando os objetos vindo do banco
    return render_template(
        "index.html",
        cadastros=registros,
        total=total_registros,
        faturamento=total_faturamento,
        concluidos=total_concluidos,
        busca=busca
    )

# Rota 2: Tela de formulario
@main_bp.route("/cadastro")
def pagina_cadastro():
    return render_template("cadastro.html")

# Rota 3: Inserção de registro
@main_bp.route("/salvar", methods=["POST"])
def salvar_cadastro():
    # Captura e trata os valores passados nos imputs
    nome = request.form.get("campo_nome", "").strip().lower()
    info = request.form.get("campo_info", "").strip().lower()
    valor_str = request.form.get("campo_valor", "0").strip()


    # validação do campo numerico no servidor
    try:
        valor = float(valor_str)
        if valor <= 0:
            raise ValueError()
    except ValueError:
        return "<h3>Erro 400: O Valor deve ser maior que zero</h3><a href='/cadastro'>Voltar</a>", 400
    
    # Validação dos campos obrigatorios
    if not nome or not info:
        return "<h3>Erro 400: Preencher todos os campos</h3><a href='/cadastro'>Voltar</a>", 400
    
    novo_registro = Registro(nome=nome, info=info, valor=valor)
    db.session.add(novo_registro) # Adiciona a sessão da tabela
    db.session.commit() # Inserindo a sessão 
    
    return redirect("/")

# Rota 4: Alteração do status
@main_bp.route("/mudar-status/<int:id>")
def mudar_status(id):
    registro = Registro.query.get(id)
    
    # Se o ID for encontrado, alterar o status e salvar no banco
    if registro:
        if registro.status == "Pendente":
            registro.status = "Concluido"

        else:
            registro.status = "Pendente"
        
        db.session.commit()

    return redirect("/")

# Rota 5: Exclusão de registro
@main_bp.route("/excluir/<int:id>")
def excluir_cadastro(id):
    registro = Registro.query.get(id)
    
    if registro:
        db.session.delete(registro)
        db.session.commit()
    return redirect("/")