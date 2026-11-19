# Cria os usuários de teste do sistema.
# Rodar uma vez, na raiz do projeto:  python criar_usuarios.py
# Se o usuário já existir, ele não é criado de novo.

from app.models.repositorio import RepositorioUsuarios
from app.models.usuario import novo_usuario


USUARIOS_DE_TESTE = [
    # nome, login, senha, tipo
    ('Ian', 'admin', 'admin123', 'administrador'),
    ('Marina Lopes', 'marina', 'marina123', 'codificador'),
]

repositorio = RepositorioUsuarios()

for nome, login, senha, tipo in USUARIOS_DE_TESTE:
    if repositorio.buscar_por_login(login) is not None:
        print('Já existe:', login)
    else:
        usuario = novo_usuario(repositorio.proximo_id(), nome, login, senha, tipo)
        repositorio.adicionar(usuario)
        print('Criado:', login, '(' + tipo + ')')

print()
print('Abra app/controllers/db/usuarios.json: nenhuma senha aparece em texto.')
