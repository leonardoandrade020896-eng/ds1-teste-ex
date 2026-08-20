from flask import Flask, render_template, request, redirect

# Instancia do servidor do Flask
app = Flask(__name__)
lista_de_cadastros = []

#Rota 1: Pagina inicial (home) calcular métricas, 
@app.route("/")
def home():
    
    # 1 capturar termo digitado no campo de busca GET
    busca = request.args.get("busca", "").strip().lower()
    
    #2 filtra a lista se houver busca digitada
    if busca:
        registro_filtrados = [item for item in lista_de_cadastros if busca in item["name"].lower()]
    else:
        registro_filtrados = lista_de_cadastros
        
    
    # 3 Calculo de métrica / indicadores (Cads Home)
    total_registro = len(lista_de_cadastros)
    total_faturamento = sum(item["valor"]for item in lista_de_cadastros)
    total_concluidos = sum(1 for item in lista_de_cadastros if item ["status"] == "Concluído")
    
    
    # 4 Enviar os indicadores para o index.html
    return render_template(
        "index.html",
        cadastro=registro_filtrados,
        total=total_registro,
        faturamento=total_faturamento,
        concluidos=total_concluidos,
    )


#  Rota 4: Alterar status
@app.route("/mudar-status/<int:indice>")
def mudar_status(indice):
    if 0 <= indice < len(lista_de_cadastros):
        # alterar o status entre "pendente"e "concluido"
        if lista_de_cadastros[indice]["status"] == "Pendente":
            lista_de_cadastros[indice]["status"] == "Concluído"
        else:
                lista_de_cadastros[indice]["status"] == "Pendente"

    return redirect("/")


# Rota 5: Excluir registro
@app.route("/excluir/<int:indice>")
def excluir_cadastro(indice):
    if 0<= indice <len(lista_de_cadastros):
        lista_de_cadastros.pop(indice)
    return redirect("/")


#Rota 2: Exibição da tela de cadastro Método (GET)
@app.route('/cadastro')
def pagina_cadastro():
    return render_template("cadastro.html")

#Rota 3:Processamento dos dados Método (POST)
@app.route('/salvar', methods=["POST"])
def salvar_cadastro():
        
    nome = request.form.get("campo_nome", "").strip()
    info = request.form.get("campo_info", "").strip()
    valor_str = request.form.get("campo_valor", "0").strip()
    
       # validaçao 1: tratar a conversão de valor numerico
    try:
        valor = float(valor_str)
        if valor <=0:
            raise ValueError
    except ValueError:
        return"<h3>Erro 400: O valor deve ser um valor maior que zero!<h3><br>< a href='/index'>Voltar ao formulario</a>", 400

    # validaçao 2: verifica se os campos obrigatorios vieram vazios
    if not nome or not info:
        return "<h3>Erro 400: Preencha todos os campos obrigatórios do formulario<h3><br><a href='/index'>Voltar ao formulário</a>", 400

    #Criação da estrutura de dados
    novo_registro = {
        "nome": nome,
        "info": info,
        "valor": valor,
        "status": "Pendente" #status sempre inicia como pendente
    }

    lista_de_cadastros.append(novo_registro)

    # redirecionar para a home (padrao post-redirect-get)
    return redirect("/")

    return render_template("resultado.html", campo_nome=nome, campo_info=info, campo_valor=valor)


if __name__ == '__main__':
    app.run(debug=True)
