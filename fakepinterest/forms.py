#Criar os formulários do nosso site
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from fakepinterest.models import Usuario

class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Fazer login")

    def validate_email(self, email): #Criando um método para validação do e-mail criar na classe acima
        usuario = Usuario.query.filter_by(email=email.data).first() #Procurando se o e-mail já existe no banco de dados
        if not usuario: #Se o e-mail já existe:
            raise ValidationError("Não existe nenhum cadastro para este e-mail. Crie uma conta")

class FormCriarConta(FlaskForm): #Criando um método para criar conta
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    username = StringField("Nome de usuário", validators=[DataRequired()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField("Senha", validators=[DataRequired(), EqualTo("senha")])
    botao_confirmacao = SubmitField("Criar Conta")

    def validate_email(self, email): #Criando um método para validação do e-mail criar na classe acima
        usuario = Usuario.query.filter_by(email=email.data).first() #Procurando se o e-mail já existe no banco de dados
        if usuario: #Se o e-mail já existe:
            raise ValidationError("E-mail já cadastrado,faça loguin para continuar")

class FormFoto(FlaskForm): #Criando uma classe para enviar/salvar fotos no perfil
    foto = FileField("Foto", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Enviar")
