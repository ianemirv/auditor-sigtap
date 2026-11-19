import secrets

from app.controllers.application import Application
from bottle import Bottle, route, run, request, static_file
from bottle import redirect, template, response, abort


app = Bottle()
ctl = Application()


#-----------------------------------------------------------------------------
# Login: funções de apoio
#
# Depois do login, o servidor grava no navegador um cookie com o id do usuário.
# O cookie é ASSINADO com a chave secreta: se alguém trocar o id na mão,
# a assinatura não bate e o Bottle ignora o cookie.

# Chave nova a cada vez que o servidor liga (reiniciar o servidor desloga todos)
CHAVE_SECRETA = secrets.token_hex(32)


def usuario_logado():
    """Lê o cookie e devolve o usuário logado, ou None se ninguém entrou."""
    usuario_id = request.get_cookie('usuario_id', secret=CHAVE_SECRETA)
    if usuario_id is None:
        return None
    return ctl.buscar_usuario(int(usuario_id))


def exigir_login():
    """Sem login, manda para /login. Com login, devolve o usuário."""
    usuario = usuario_logado()
    if usuario is None:
        redirect('/login')
    return usuario


def exigir_permissao_catalogo():
    usuario = exigir_login()
    if not usuario.pode_editar_catalogo():
        abort(403)   # 403 = proibido: está logado, mas não tem permissão
    return usuario


def exigir_permissao_usuarios():
    usuario = exigir_login()
    if not usuario.pode_gerenciar_usuarios():
        abort(403)
    return usuario


#-----------------------------------------------------------------------------
# Rotas:

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')

@app.route('/helper')
def helper(info= None):
    return ctl.render('helper')

@app.error(403)
def erro_403(erro):
    return ctl.render('acesso_negado', usuario_logado())


#-----------------------------------------------------------------------------
# Suas rotas aqui:

@app.route('/', method='GET')
def action_index():
    return ctl.render('index', usuario_logado())


# Login e logout --------------------------------------------------------------

@app.route('/login', method='GET')
def action_login():
    if usuario_logado() is not None:
        redirect('/painel')
    return ctl.render('login', None)

@app.route('/login', method='POST')
def action_login_entrar():
    dados = request.forms.decode()
    usuario = ctl.autenticar(dados.get('login', ''), dados.get('senha', ''))
    if usuario is None:
        return ctl.render('login', None, 'Login ou senha incorretos.')
    response.set_cookie('usuario_id', str(usuario.id), secret=CHAVE_SECRETA,
                        path='/', httponly=True, samesite='lax', max_age=2 * 60 * 60)
    redirect('/painel')

@app.route('/logout', method='GET')
def action_logout():
    response.delete_cookie('usuario_id', path='/')
    redirect('/login')


# Painel (acesso restrito) ----------------------------------------------------

@app.route('/painel', method='GET')
def action_painel():
    usuario = exigir_login()
    return ctl.render('painel', usuario)


# Atendimentos (CRUD) - qualquer usuário logado --------------------------------

@app.route('/atendimentos', method='GET')
def action_atendimentos():
    usuario = exigir_login()
    return ctl.render('atendimentos', usuario)

@app.route('/atendimentos/novo', method='GET')
def action_atendimento_novo():
    usuario = exigir_login()
    return ctl.render('atendimento_novo', usuario)

@app.route('/atendimentos', method='POST')
def action_atendimento_criar():
    usuario = exigir_login()
    dados = request.forms.decode()          # decode() mantém os acentos certos
    texto = dados.get('texto', '')
    faturados = dados.getall('faturados')   # getall: todas as caixas marcadas
    if texto.strip() == '':
        redirect('/atendimentos/novo')
    novo_id = ctl.criar_atendimento(texto, faturados, usuario)
    redirect('/atendimentos/' + str(novo_id))

@app.route('/atendimentos/<id:int>', method='GET')
def action_atendimento_detalhe(id):
    usuario = exigir_login()
    return ctl.render('atendimento_detalhe', usuario, id)

@app.route('/atendimentos/<id:int>/editar', method='GET')
def action_atendimento_editar(id):
    usuario = exigir_login()
    return ctl.render('atendimento_editar', usuario, id)

@app.route('/atendimentos/<id:int>/editar', method='POST')
def action_atendimento_salvar(id):
    exigir_login()
    dados = request.forms.decode()
    texto = dados.get('texto', '')
    faturados = dados.getall('faturados')
    if texto.strip() == '':
        redirect('/atendimentos/' + str(id) + '/editar')
    ctl.editar_atendimento(id, texto, faturados)
    redirect('/atendimentos/' + str(id))

@app.route('/atendimentos/<id:int>/excluir', method='POST')
def action_atendimento_excluir(id):
    exigir_login()
    ctl.excluir_atendimento(id)
    redirect('/atendimentos')


# Catálogo SIGTAP - todos veem, só o administrador edita ------------------------

@app.route('/procedimentos', method='GET')
def action_procedimentos():
    usuario = exigir_login()
    return ctl.render('procedimentos', usuario)

@app.route('/procedimentos/novo', method='GET')
def action_procedimento_novo():
    usuario = exigir_permissao_catalogo()
    return ctl.render('procedimento_novo', usuario)

@app.route('/procedimentos', method='POST')
def action_procedimento_criar():
    usuario = exigir_permissao_catalogo()
    dados = request.forms.decode()
    erro = ctl.criar_procedimento(dados.get('codigo', ''),
                                  dados.get('nome', ''),
                                  dados.get('palavras_chave', ''))
    if erro is not None:
        return ctl.render('procedimento_novo', usuario, erro)
    redirect('/procedimentos')

@app.route('/procedimentos/<codigo>/editar', method='GET')
def action_procedimento_editar(codigo):
    usuario = exigir_permissao_catalogo()
    return ctl.render('procedimento_editar', usuario, codigo)

@app.route('/procedimentos/<codigo>/editar', method='POST')
def action_procedimento_salvar(codigo):
    exigir_permissao_catalogo()
    dados = request.forms.decode()
    ctl.editar_procedimento(codigo, dados.get('nome', ''), dados.get('palavras_chave', ''))
    redirect('/procedimentos')

@app.route('/procedimentos/<codigo>/excluir', method='POST')
def action_procedimento_excluir(codigo):
    exigir_permissao_catalogo()
    ctl.excluir_procedimento(codigo)
    redirect('/procedimentos')


# Usuários (CRUD) - só o administrador ------------------------------------------

@app.route('/usuarios', method='GET')
def action_usuarios():
    usuario = exigir_permissao_usuarios()
    return ctl.render('usuarios', usuario)

@app.route('/usuarios/novo', method='GET')
def action_usuario_novo():
    usuario = exigir_permissao_usuarios()
    return ctl.render('usuario_novo', usuario)

@app.route('/usuarios', method='POST')
def action_usuario_criar():
    usuario = exigir_permissao_usuarios()
    dados = request.forms.decode()
    erro = ctl.cadastrar_usuario(dados.get('nome', ''), dados.get('login', ''),
                                 dados.get('tipo', ''), dados.get('senha', ''),
                                 dados.get('confirmar', ''))
    if erro is not None:
        return ctl.render('usuario_novo', usuario, erro)
    redirect('/usuarios')

@app.route('/usuarios/<id:int>/editar', method='GET')
def action_usuario_editar(id):
    usuario = exigir_permissao_usuarios()
    return ctl.render('usuario_editar', usuario, id)

@app.route('/usuarios/<id:int>/editar', method='POST')
def action_usuario_salvar(id):
    usuario = exigir_permissao_usuarios()
    dados = request.forms.decode()
    erro = ctl.editar_usuario(id, dados.get('nome', ''), dados.get('tipo', ''),
                              dados.get('senha', ''), dados.get('confirmar', ''),
                              usuario)
    if erro is not None:
        return ctl.render('usuario_editar', usuario, id, erro)
    redirect('/usuarios')

@app.route('/usuarios/<id:int>/excluir', method='POST')
def action_usuario_excluir(id):
    usuario = exigir_permissao_usuarios()
    erro = ctl.excluir_usuario(id, usuario)
    if erro is not None:
        return ctl.render('usuarios', usuario, erro)
    redirect('/usuarios')


#-----------------------------------------------------------------------------


if __name__ == '__main__':

    run(app, host='0.0.0.0', port=8080, debug=True)
