### pip install Flask
### pip install mysql.connector

from flask import Flask, request, jsonify
import mysql.connector
import random

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'database-project.cayd3qorxcai.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = '145acf1435'
app.config['MYSQL_DB'] = 'PROJETOSCRUM'

db = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

app = Flask(__name__)

#Rota padrão da aplicação
@app.route('/')
def hello_world():
    return '<h1> Olá, Mundo! <h1>'


#Rota para fazer o cadastro dos usuários de forma geral
@app.route('/cadastro', methods=['POST'])
def cadastro():

    # Recebendo os parâmetros do frontend
    # Parâmetros devem ser lido utilizando request.form
    
    email_usuario = request.form['email']
    password_usuario = request.form['password']
    nome_usuario = request.form['nome']
    tipo_usuario = request.form['tipo_usuario']
    

    # Inicializando parâmetros do banco de dados e passando para tabela usuario (padrão)
    # Comandos para inserção no banco de dados
    mycursor = db.cursor()
    sql_command_for_database = "INSERT INTO usuario (nome, email, senha, tipo_usuario) VALUES (%s, %s, %s, %s);"
    values_for_database = (nome_usuario, email_usuario, password_usuario, tipo_usuario)
    try:
        mycursor.execute(sql_command_for_database, values_for_database)
    except:
        return jsonify({'cadastro': 'error'})
    db.commit()

    # Inicializando parâmetros do banco de dados e passando para tabela
    # de professor ou aluno.
    # Comandos para inserção no banco de dados
    mycursor = db.cursor()
    values_for_database = (nome_usuario, email_usuario, password_usuario)
    
    if(tipo_usuario == 'professor'):
        sql_command_for_database = "INSERT INTO professor (nome, email, senha) VALUES (%s, %s, %s);"
    elif(tipo_usuario == 'aluno'):
        sql_command_for_database = "INSERT INTO aluno (Nome, Email, Senha) VALUES (%s, %s, %s);"

    try:
        mycursor.execute(sql_command_for_database, values_for_database)
    except:
        return jsonify({'cadastro': 'error'})    
            
    db.commit()
    return jsonify({'cadastro': 'Cadastrado com sucesso!'})
    

@app.route('/login', methods=['POST'])
def login():

    # Recebendo email e senha do usuário
    email = request.form['email']
    password = request.form['password']
    
    # Inicialiazação dos parâmetros para o banco de dados
    mycursor = db.cursor()

    # Procura no banco de dados um usuário com o email que foi passado
    sql_command = "SELECT Email, Senha FROM usuario Where Email = %s;"
    value = (email,)
    mycursor.execute(sql_command, value)
    email_res = mycursor.fetchone()

    # Verefica se o retorno não foi nulo e se a senha inserida é igual a cadastrada
    if email_res is not None:
        senha_encontrada = email_res[1] #posicao da coluna da tabela do banco de dado
        if senha_encontrada == password:

            print("Logado com sucesso")
            sql_command = "SELECT Tipo_usuario from usuario WHERE Email = %s;"
            value = (email,)
            mycursor.execute(sql_command, value)
            tipo_user = mycursor.fetchone()

            return jsonify({'acesso': 'OK', 'Tipo_aluno': tipo_user[0], 'email': email})
        else:
            print("Senha incorreta")
    else:
        print("Email nao encontrado")

    return jsonify({'acesso': 'false', 'Tipo_aluno': 'Null'})



@app.route('/Registrar_materia', methods=['POST'])
def Registrar_materia():
    Nome_materia = request.form['Nome_materia']
    Nome_professor = request.form['Nome_professor']
    Ementa = request.form['Ementa']
    #Gerar o codigo da materia pelo back (prefixo 23 (2023))
    codigo = random.randint(230000, 239999)
    #Insere na tabela Materia
    mycursor = db.cursor()
    sql_command_for_database = "INSERT INTO Materia (Codigo, Nome, Ementa) VALUES (%s, %s, %s);"
    values_for_database = (codigo, Nome_materia, Ementa)
    mycursor.execute(sql_command_for_database, values_for_database)

    #Insere na tabela Materia x Professor
    sql_command_for_database = "INSERT INTO Materia_Professor (Nome_Professor, Nome_Materia) VALUES (%s, %s);"
    values_for_database = (Nome_professor, Nome_materia)
    mycursor.execute(sql_command_for_database, values_for_database)

    db.commit()

    return jsonify({'Status': 'Materia criada com sucesso!!!'})




@app.route('/return_aluno', methods=['POST'])
def return_aluno():

    email = request.form['email']
    #email = "janedoe@gmail.com" teste de execução

    # Inicialização do cursor
    mycursor = db.cursor()
    # Comando e valores para consultar o banco de dados
    sql_command_for_database = "SELECT * FROM aluno WHERE Email = %s;"
    values_for_database = (email,)

    # Tenta executar o camando no banco de dados para fazer a consulta
    try:
        mycursor.execute(sql_command_for_database, values_for_database)
    except:
        return jsonify({'return_aluno': 'error'})

    aluno_data = mycursor.fetchone()

    # parâmetros separados pra retornar para o backend
    aluno_RA = aluno_data[0]
    aluno_nome = aluno_data[1]
    aluno_email = aluno_data[2]

    return jsonify({'aluno_RA': aluno_RA, 'aluno_nome': aluno_nome, 'aluno_email': aluno_email})


@app.route('/Materia_Aluno', methods=['POST'])
def Materia_Aluno():

    Nome_Aluno = request.form['Nome']
    Nome_Materia = request.form['Materia']

    #Nome_Aluno = 'Rafael Sato'
    #Nome_Materia = 'calculo'

    # Inicialização do cursor
    mycursor = db.cursor()
    # Comando e valores para consultar o banco de dados
    sql_command_for_database = "INSERT INTO Materia_Aluno (Nome_Aluno, Nome_Materia) VALUES (%s, %s);"
    values_for_database = (Nome_Aluno, Nome_Materia)

    # Tenta executar o camando no banco de dados para fazer a consulta
    try:
        mycursor.execute(sql_command_for_database, values_for_database)
    except:
        return jsonify({'Materia_Aluno': 'error'})

    db.commit()

    return jsonify({'status':'O aluno foi inscrito com sucesso na materia'})


@app.route('/return_professor', methods=['POST'])
def return_professor():

    Email = request.form['Email']

    #Email = "professor@gmail.com"

    # Inicialização do cursor
    mycursor = db.cursor()
    # Comando e valores para consultar o banco de dados
    sql_command_for_database = "SELECT * FROM professor WHERE Email = %s;"
    values_for_database = (Email,)

    # Tenta executar o camando no banco de dados para fazer a consulta
    try:
        mycursor.execute(sql_command_for_database, values_for_database)
    except:
        return jsonify({'return_professor': 'error'})

    professor_data = mycursor.fetchone()

    # parâmetros separados pra retornar para o backend
    professor_RP = professor_data[0]
    professor_nome = professor_data[1]
    professor_email = professor_data[2]

    return jsonify({'professor_RP': professor_RP, 'professor_nome': professor_nome, 'professor_email': professor_email})


@app.route('/return_materias', methods=['POST'])
def return_materias():

    mycursor = db.cursor()
    sql_command_for_database = "SELECT * FROM Materia"

    mycursor.execute(sql_command_for_database)

    materias_data = mycursor.fetchall()
    size = len(materias_data)

    data = []

    for i in range(size):
        materias = {
        'codigo_materias': str(materias_data[i][0]),
        'nome_materias': materias_data[i][1],
        'ementa_materias': materias_data[i][2]
        }
        data.append(materias)

    return jsonify(data)


@app.route('/render_test', methods=['GET'])
def render_test():

    email = "janedoe@gmail.com"

    # Inicialização do cursor
    mycursor = db.cursor()
    # Comando e valores para consultar o banco de dados
    sql_command_for_database = "SELECT * FROM aluno WHERE Email = %s;"
    values_for_database = (email,)

    # Tenta executar o camando no banco de dados para fazer a consulta
    try:
        mycursor.execute(sql_command_for_database, values_for_database)
    except:
        return jsonify({'return_aluno': 'error'})

    aluno_data = mycursor.fetchone()

    # parâmetros separados pra retornar para o backend
    aluno_RA = aluno_data[0]
    aluno_nome = aluno_data[1]
    aluno_email = aluno_data[2]

    return jsonify({'aluno_RA': aluno_RA, 'aluno_nome': aluno_nome, 'aluno_email': aluno_email})

if __name__ == '__main__':
    app.run()