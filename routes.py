import os

from flask import Blueprint, current_app, flash, redirect, render_template, request
from werkzeug.utils import secure_filename

from database import db
from models import Categoria, Registro

main_bp = Blueprint('main', __name__)

# definir as extensões que permitimos receber
EXTENSOES_PERMITIDAS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def arquivo_permitido(filename):
    """Verifica se a extensão do arquivo é permitida."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in EXTENSOES_PERMITIDAS
 
@main_bp.route("/")
def home():
    # Obter os parâmetros de busca e categoria da URL
    busca = request.args.get("busca", "").strip().lower()
    categoria_id = request.args.get("categoria_id", "")

    # Construir a query com base nos filtros fornecidos
    query = Registro.query
    if busca:
        # Filtrar registros pelo nome, ignorando maiúsculas e minúsculas
        query = query.filter(Registro.nome.ilike(f"%{busca}%"))
    # Filtrar registros pela categoria, se fornecida e válida
    if categoria_id and categoria_id.isdigit():
        query = query.filter(Registro.categoria_id == int(categoria_id))

    # Obter todos os registros filtrados
    registros = query.all()
    # Calcular o total de registros, faturamento e quantidade de registros concluídos
    total = len(registros)
    faturamento = sum(item.valor for item in registros)
    concluidos = sum(1 for item in registros if item.status == "Concluído")

    # Obter todas as categorias para exibir no filtro
    categorias = Categoria.query.all()
 
    return render_template(
        "index.html",
        cadastros=registros,
        total=total,
        faturamento=faturamento,
        concluidos=concluidos,
        busca=busca,
        categorias=categorias,
        categoria_selecionada=int(categoria_id) if categoria_id.isdigit() else None
    )
 
@main_bp.route("/cadastro")
def pagina_cadastro():
    categorias = Categoria.query.all()
    return render_template("cadastro.html", categorias=categorias)
 
@main_bp.route("/salvar", methods=["POST"])
def salvar_cadastro():
    nome = request.form.get("campo_nome", "").strip()
    info = request.form.get("campo_info", "").strip()
    valor_str = request.form.get("campo_valor", "0").strip()
    cat_id = request.form.get("campo_categoria")

    arquivo_foto = request.files.get("campo_imagem")
    if not nome or not info or not valor_str or not cat_id:
        flash("Todos os campos são obrigatórios.", "danger")
        return redirect("/cadastro")

    try:
        valor = float(valor_str)
        if valor < 0:
            raise ValueError("Valor não pode ser negativo.")
    except ValueError:
            flash("Valor deve ser maior que zero. Por favor, insira um número válido.", "warning")
            return redirect("/cadastro")

    nome_imagem_salva = "padrao.png"  # Nome padrão caso não haja upload de imagem
    if arquivo_foto and arquivo_foto.filename != "":
        if arquivo_permitido(arquivo_foto.filename):
            # remover caracteres especiais do nome do arquivo e salvar a imagem
            nome_seguro = secure_filename(arquivo_foto.filename)
            nome_imagem_salva = f"foto_{nome_seguro}"
            caminho_completo = os.path.join(current_app.config['UPLOAD_FOLDER'], nome_seguro)
            arquivo_foto.save(caminho_completo)
        else:
            flash("Extensão de arquivo não permitida. Use PNG, JPG, JPEG ou webp.", "danger")
            return redirect("/cadastro")

        novo_registro = Registro(
            nome=nome,
            info=info,
            valor=valor,
            categoria_id=int(cat_id),
            imagem=nome_imagem_salva,
        )
        db.session.add(novo_registro)
        db.session.commit()

        flash("Registro salvo com sucesso!", "successo")
        return redirect("/")

@main_bp.route("/excluir/<int:id>")
def excluir_registro(id):
    registro = Registro.query.get(id)
    if registro:
        if registro.imagem and registro.imagem != "padrao.png":
            caminho_foto = os.path.join(current_app.config['UPLOAD_FOLDER'], registro.imagem)
            if os.path.exists(caminho_foto):
                os.remove(caminho_foto)
        db.session.delete(registro)
        db.session.commit()
        flash("Registro excluído com sucesso!", "info")

    return redirect("/")
