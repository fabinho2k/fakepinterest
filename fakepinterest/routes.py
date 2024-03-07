#Criando o arquivo para as rotas/links da pagina

from flask import Flask, render_template, url_for, redirect
from fakepinterest import app, database, bcrypt
from fakepinterest.models import Usuario, Foto
from flask_login import login_required, login_user, logout_user, current_user
from fakepinterest.forms import FormLogin, FormCriarConta, FormFoto
import os
from werkzeug.utils import secure_filename


@app.route('/', methods=["GET", "POST"]) #Criando o link da pagina inicial, permitindo pegar informaçõe(GET) e enviar (POST) do html
def homepage():
    formlogin = FormLogin()
    if formlogin.validate_on_submit(): #Se os campos de login forem válidos:
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first() #Procurando no banco de dados, usuário com email passado para login
        if usuario and  bcrypt.check_password_hash(usuario.senha, formlogin.senha.data): #Se existe esse usuário e a senha está correta:
            login_user(usuario) #Faça login deste usuário
            return redirect(url_for("perfil", id_usuario=usuario.id))  # Após estar logado, o usuário será redirecionado a página do perfil

    return render_template('homepage.html', form=formlogin) #Retornando o frontend editado no template html

@app.route("/criarconta", methods=["GET", "POST"])
def criar_conta():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit():

        senha = bcrypt.generate_password_hash(form_criarconta.senha.data) #Usando o bcrypt para criptografar a senha do usuário

        #Para pegarmos informações como no atributo abaixo. Usamamos na ordem: Formulário:from_criarconta o campo: username A informação do campo: campo.data
        usuario = Usuario(username=form_criarconta.username.data,
                          email=form_criarconta.email.data,
                          senha=senha)

        database.session.add(usuario) #Adicionando o usuário no banco de dados
        database.session.commit() #Dando um commit para salvar as modificações no banco de dados

        login_user(usuario, remember=True) #Após criar a conta, fazendo o login do usuário no sistema

        return redirect(url_for("perfil", id_usuario=usuario.id)) #Após estar logado, o usuário será redirecionado a página do perfil

    return render_template("criarconta.html", form=form_criarconta)


@app.route("/perfil/<id_usuario>", methods=["GET", "POST"]) #Criando o link do perfil de cada usuário
@login_required  #Usuário é obrigado estar logado para usar esse método
def perfil(id_usuario):
    # Se o usuário estiver vendo seu próprio perfil:
    if int(id_usuario) == int(current_user.id):
        form_foto = FormFoto()
        if form_foto.validate_on_submit(): #Se estiver tudo certo com a foto enviada:
            arquivo = form_foto.foto.data #Salvando o arquivo
            nome_seguro = secure_filename(arquivo.filename) #Renomeando o arquivo de uma forma para não ter caractéres que possam dar erro
            #Salvando o arquivo na pasta fotos_post
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)), #Pegando o caminho absoluto onde está o arquivo file. No caso o este arquivo(routes) +
                                app.config["UPLOAD_FOLDER"], nome_seguro)#Caminho onde está sendo upada a foto + o nome do arquivo
            arquivo.save(caminho)

            #Registrando esse arquivo no banco de dados
            foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()


        return render_template('perfil.html', usuario=current_user, form=form_foto) #Retornando o frontend editado no template html
    else:
        usuario =  Usuario.query.get(int(id_usuario)) #O usuário está no perfil de outra pessoa
        return render_template('perfil.html', usuario=usuario, form=None) #Retornando o frontend editado no template html


@app.route("/logout")  #Criando o link de logout
@login_required #Obrigatório estar logado em alguma conta para acessar essa pagina
def logout(): #Criando o método de deslogar o usário.
    logout_user() #Deslogando o usuário
    return redirect(url_for("homepage"))

@app.route("/feed") #Criando o feed para que seja exibida todas as fotos de todos usuários
@login_required
def feed():
    fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()
    return render_template("feed.html", fotos=fotos)