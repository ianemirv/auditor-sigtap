from app.controllers.application import Application
from bottle import Bottle, route, run, request, static_file
from bottle import redirect, template, response


app = Bottle()
ctl = Application()


#-----------------------------------------------------------------------------
# Rotas:

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')

@app.route('/helper')
def helper(info= None):
    return ctl.render('helper')


#-----------------------------------------------------------------------------
# Suas rotas aqui:

@app.route('/', method='GET')
def action_index():
    return ctl.render('index')


# Atendimentos (CRUD) ---------------------------------------------------------

@app.route('/atendimentos', method='GET')
def action_atendimentos():
    return ctl.render('atendimentos')

@app.route('/atendimentos/novo', method='GET')
def action_atendimento_novo():
    return ctl.render('atendimento_novo')

@app.route('/atendimentos', method='POST')
def action_atendimento_criar():
    dados = request.forms.decode()          # decode() mantém os acentos certos
    texto = dados.get('texto', '')
    faturados = dados.getall('faturados')   # getall: todas as caixas marcadas
    if texto.strip() == '':
        redirect('/atendimentos/novo')
    novo_id = ctl.criar_atendimento(texto, faturados)
    redirect('/atendimentos/' + str(novo_id))

@app.route('/atendimentos/<id:int>', method='GET')
def action_atendimento_detalhe(id):
    return ctl.render('atendimento_detalhe', id)

@app.route('/atendimentos/<id:int>/editar', method='GET')
def action_atendimento_editar(id):
    return ctl.render('atendimento_editar', id)

@app.route('/atendimentos/<id:int>/editar', method='POST')
def action_atendimento_salvar(id):
    dados = request.forms.decode()
    texto = dados.get('texto', '')
    faturados = dados.getall('faturados')
    if texto.strip() == '':
        redirect('/atendimentos/' + str(id) + '/editar')
    ctl.editar_atendimento(id, texto, faturados)
    redirect('/atendimentos/' + str(id))

@app.route('/atendimentos/<id:int>/excluir', method='POST')
def action_atendimento_excluir(id):
    ctl.excluir_atendimento(id)
    redirect('/atendimentos')


# Catálogo de procedimentos SIGTAP (CRUD) -------------------------------------

@app.route('/procedimentos', method='GET')
def action_procedimentos():
    return ctl.render('procedimentos')

@app.route('/procedimentos/novo', method='GET')
def action_procedimento_novo():
    return ctl.render('procedimento_novo')

@app.route('/procedimentos', method='POST')
def action_procedimento_criar():
    dados = request.forms.decode()
    erro = ctl.criar_procedimento(dados.get('codigo', ''),
                                  dados.get('nome', ''),
                                  dados.get('palavras_chave', ''))
    if erro is not None:
        return ctl.render('procedimento_novo', erro)
    redirect('/procedimentos')

@app.route('/procedimentos/<codigo>/editar', method='GET')
def action_procedimento_editar(codigo):
    return ctl.render('procedimento_editar', codigo)

@app.route('/procedimentos/<codigo>/editar', method='POST')
def action_procedimento_salvar(codigo):
    dados = request.forms.decode()
    ctl.editar_procedimento(codigo, dados.get('nome', ''), dados.get('palavras_chave', ''))
    redirect('/procedimentos')

@app.route('/procedimentos/<codigo>/excluir', method='POST')
def action_procedimento_excluir(codigo):
    ctl.excluir_procedimento(codigo)
    redirect('/procedimentos')


#-----------------------------------------------------------------------------


if __name__ == '__main__':

    run(app, host='0.0.0.0', port=8080, debug=True)
