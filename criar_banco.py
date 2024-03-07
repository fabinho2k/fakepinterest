from fakepinterest import database, app
from fakepinterest.models import Usuario, Foto

with app.app_context(): # Método obrigatório para criação do banco de dados
    database.create_all()