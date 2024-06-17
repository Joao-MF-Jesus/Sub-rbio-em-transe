from tkinter import *
from tkinter import ttk
import tkinter.messagebox as tkmb
import mysql.connector
from mysql.connector import connect, Error
from datetime import datetime
import tkinter as tk
from PIL import Image, ImageTk
w = Tk()
w.title("Subúrbio em Transe ")
largura = 800
altura = 500
largura_screen = w.winfo_screenwidth()
altura_screen = w.winfo_screenheight()
posx = largura_screen/2 - largura/2
posy = altura_screen/2 - altura/2
w.geometry('%dx%d+%d+%d' % (largura, altura, posx, posy))
w.minsize(width=800, height=600)
w.resizable(False, False)
w['bg'] = "black"

conexao = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="root"
                )
'''
cursor = conexao.cursor()
cursor.execute('drop database usuario')'''

def criar_banco_auto():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="usuario"
        )
    except Error as e:
        if "Unknown database" in str(e):
            # Se o erro indica que o banco de dados é desconhecido, crie-o
            try:
                conexao = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="root"
                )
                cursor = conexao.cursor()
                cursor.execute("CREATE DATABASE usuario")
                mostrar_aviso("Banco de dados 'usuario' criado!")
            except Error as e:
                mostrar_aviso(f"Erro ao criar o banco de dados 'usuario': {str(e)}")
            finally:
                if conexao.is_connected():
                    conexao.close()
                    cursor.close()
        else:
            mostrar_aviso(f"Erro ao conectar ao banco de dados 'usuario': {str(e)}")
    finally:
        if conexao.is_connected():
            conexao.close()

def criar_tabela_usuario():
    try:
        conexao = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="usuario"
            )
        
        cursor = conexao.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario (
                 id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conexao.commit()
        cursor.close()
    except Error as e:
        mostrar_aviso(f"Erro ao criar a tabela 'usuario': {str(e)}")

def criar_tabela_voluntario():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="usuario"
        )
        
        cursor = conexao.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Voluntario (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL,
                telefone VARCHAR(15),
                endereco TEXT,
                data_nascimento DATE,
                sexo ENUM('Masculino', 'Feminino', 'Outro'),
                ata_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            )
        """)
        conexao.commit()
        cursor.close()
    except Error as e:
        mostrar_aviso(f"Erro ao criar a tabela 'Voluntario': {str(e)}")        
        

def abrir_n_j_b():
    n_j = Toplevel(w)
    n_j.title('Cadastro Voluntário')
    n_j.geometry('250x600')
    global nome_entry, email_entry, telefone_entry, data_nascimento_entry, endereco_entry, sexo_var


    nome_label = Label(n_j, text="Nome: ")
    nome_label.grid(row=1, column=0)
    nome_entry = Entry(n_j)
    nome_entry.grid(row=1, column=1)

    email_label = Label(n_j, text="Email:")
    email_label.grid(row=2, column=0)
    email_entry = Entry(n_j)
    email_entry.grid(row=2, column=1)

    telefone_label = Label(n_j, text="Telefone:")
    telefone_label.grid(row=3, column=0)
    telefone_entry = Entry(n_j)
    telefone_entry.grid(row=3, column=1)

    data_nascimento_label = Label(n_j, text="Data de nascimento:")
    data_nascimento_label.grid(row=4, column=0)
    data_nascimento_entry = Entry(n_j)
    data_nascimento_entry.grid(row=4, column=1)

    rua_label = Label(n_j, text="Endereço:")
    rua_label.grid(row=5, column=0)
    endereco_entry = Entry(n_j)
    endereco_entry.grid(row=5, column=1)
    
    sexo_label = Label(n_j, text="Sexo:")
    sexo_label.grid(row=12, column=0)
    masculino_rdb = Radiobutton(n_j, text="Masculino", variable=sexo_var, value=1)
    masculino_rdb.grid(row=12, column=0)
    feminino_rdb = Radiobutton(n_j, text="Feminino", variable=sexo_var, value=2)
    feminino_rdb.grid(row=12, column=1)

    voluntario_var = IntVar()
    temporario_rdb = Radiobutton(n_j, text="Temporário", variable=voluntario_var, value=1)
    temporario_rdb.grid(row=14, column=0)
    fixo_rdb = Radiobutton(n_j, text="Fixo", variable=voluntario_var, value=2)
    fixo_rdb.grid(row=14, column=1)
    bcb_B = Button(n_j, text="Cadastrar Voluntário", command=cadastrar_voluntario)
    bcb_B.grid(row=16, column=0)
    criar_tabela_voluntario()


def criar_tabela_doacao():
        try:
                conexao = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="root",
                        database="usuario"
                )

                cursor = conexao.cursor()
                cursor.execute("""
                        CREATE TABLE IF NOT EXISTS doacao (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                id_voluntario INT,
                                valor DECIMAL(10, 2) NOT NULL
                               
                        )
                """)
                conexao.commit()
                cursor.close()
        except Error as e:
                mostrar_aviso(f"Erro ao criar a tabela 'doacao': {str(e)}")

def cdb():
    criar_banco_auto()

def mostrar_aviso(mensagem):
    aviso = Tk()
    aviso.title("Aviso")
    label = Label(aviso, text=mensagem)
    label.pack(padx=10, pady=10)
    botao_ok = Button(aviso, text="OK", command=aviso.destroy)
    botao_ok.pack(pady=10)
    aviso.mainloop()

def sair():
    resl = tkmb.askquestion("Sair", "Tem certeza?")
    if resl == "yes":
        w.destroy()

exit_B = Button(w, text="Sair", command=sair)
exit_B.place(x=750, y=550)

# Define entry variables globally
#id_usuario_entry = None
nome_entry = None
email_entry = None
telefone_entry = None
data_nascimento_entry = None
endereco_entry = None
sexo_var = None


username_entry = None
password_entry = None
email_entry_u = None

valor_doacao_entry = None

def abrir_n_j_b():
    global nome_entry, email_entry, telefone_entry, data_nascimento_entry, endereco_entry, sexo_var
    n_j = Toplevel(w)
    n_j.title('Cadastro Voluntário')
    n_j.geometry('250x600')

    nome_label = Label(n_j, text="Nome: ")
    nome_label.grid(row=1, column=0)
    nome_entry = Entry(n_j)
    nome_entry.grid(row=1, column=1)

    email_label_v = Label(n_j, text="Email:")
    email_label_v.grid(row=2, column=0)
    email_entry = Entry(n_j)
    email_entry.grid(row=2, column=1)

    telefone_label = Label(n_j, text="Telefone:")
    telefone_label.grid(row=3, column=0)
    telefone_entry = Entry(n_j)
    telefone_entry.grid(row=3, column=1)

    data_nascimento_label = Label(n_j, text="Data de nascimento:")
    data_nascimento_label.grid(row=4, column=0)
    data_nascimento_entry = Entry(n_j)
    data_nascimento_entry.grid(row=4, column=1)

    rua_label = Label(n_j, text="Endereço:")
    rua_label.grid(row=5, column=0)
    endereco_entry = Entry(n_j)
    endereco_entry.grid(row=5, column=1)

    sexo_var = IntVar()
    sexo_label = Label(n_j, text="Sexo:")
    sexo_label.grid(row=6, column=0)
    masculino_rdb = Radiobutton(n_j, text="Masculino", variable=sexo_var, value=1)
    masculino_rdb.grid(row=6, column=1)
    feminino_rdb = Radiobutton(n_j, text="Feminino", variable=sexo_var, value=2)
    feminino_rdb.grid(row=7, column=0)



    bcb_B = Button(n_j, text="Cadastrar Voluntário", command=cadastrar_voluntario)
    bcb_B.grid(row=10, column=0)
    criar_tabela_voluntario()


def cadastrar_voluntario():
    nome = nome_entry.get()
    email = email_entry.get()
    telefone = telefone_entry.get()
    endereco = endereco_entry.get()
    data_nascimento_str = data_nascimento_entry.get()

    # Convertendo a data para o formato YYYY-MM-DD
    try:
        data_nascimento = datetime.strptime(data_nascimento_str, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError as e:
        mostrar_aviso(f"Data de nascimento inválida: {str(e)}")
        return

    # Mapeamento de IntVar para string
    sexo = "Masculino" if sexo_var.get() == 1 else "Feminino" if sexo_var.get() == 2 else "Outro"
    
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="usuario"
        )

        cursor = conexao.cursor()
        cursor.execute("""
            INSERT INTO voluntario (nome, email, telefone, endereco, data_nascimento, sexo)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nome, email, telefone, endereco, data_nascimento, sexo))
        conexao.commit()
        mostrar_aviso("Voluntário cadastrado com sucesso!")
        cursor.close()
    except Error as e:
        mostrar_aviso(f"Erro ao cadastrar voluntário: {str(e)}")
    finally:
        if conexao.is_connected():
            conexao.close()
    
def abrir_n_j_f():
    n_j_f = Toplevel(w)
    n_j_f.title('Cadastro')
    n_j_f.geometry('250x600')
    global username_entry, password_entry, email_entry
    username_label = Label(n_j_f, text="Nome:")
    username_label.grid(row=1, column=0)
    username_entry = Entry(n_j_f)
    username_entry.grid(row=1, column=1)
    password_label = Label(n_j_f, text="Senha:")
    password_label.grid(row=2, column=0)
    password_entry = Entry(n_j_f, show="*")
    password_entry.grid(row=2, column=1)
    email_label = Label(n_j_f, text="Email:")  # Corrigido de email_entry para email_label
    email_label.grid(row=3, column=0)
    email_entry = Entry(n_j_f)  # Definindo email_entry corretamente
    email_entry.grid(row=3, column=1)
    bcb_f = Button(n_j_f, text="Cadastrar", command=cadastrar_usuario)
    bcb_f.grid(row=4, column=0)
    criar_tabela_usuario()

def abrir_n_j_p():
    global valor_doacao_entry

    n_j_p = Toplevel(w)
    n_j_p.title('Efetuar Doação')
    n_j_p.geometry('250x600')

    valor_doacao_label = Label(n_j_p, text="Valor da doação:")
    valor_doacao_label.grid(row=1, column=0)
    valor_doacao_entry = Entry(n_j_p)
    valor_doacao_entry.grid(row=1, column=1)
 
    bcb_p = Button(n_j_p, text="Cadastrar doacao", command=cadastrar_doacao)
    bcb_p.grid(row=4, column=0)
    criar_tabela_doacao()
    

def cadastrar_usuario():
    username = username_entry.get()
    password = password_entry.get()
    email = email_entry.get()
    print(f"Cadastrando usuário: {username}, {email}")
    if not username or not password or not email:
        mostrar_aviso("Por favor, preencha todos os campos.")
    else:
        try:
            conexao = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="usuario"
            )
            cursor = conexao.cursor()
            cursor.execute("INSERT INTO usuario (username, password, email) VALUES ( %s, %s, %s)", (username, password, email))
            conexao.commit()
            cursor.close()
            mostrar_aviso("Usuário cadastrado com sucesso!")
        except Error as e:
            mostrar_aviso(f"Erro ao cadastrar a usuário: {str(e)}")
def ver_usuario():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="usuario"
        )
        cursor = conexao.cursor()
        query = "SELECT * FROM `usuario`"
        cursor.execute(query)
        resultados = cursor.fetchall()
        cursor.close()
        conexao.close()

        jan_res = Tk()
        jan_res.title("Resultados da Consulta")

        # Criar uma área de texto para exibir os resultados
        tex_res = Text(jan_res)
        tex_res.pack()

        # Exibir os resultados na área de texto
        for resultado in resultados:
            tex_res.insert(END, resultado)
            tex_res.insert(END, "\n")

        jan_res.mainloop()

    except mysql.connector.Error as err:
        print(f"Erro ao consultar o banco de dados: {err}")
        
def cadastrar_voluntario():
    nome = nome_entry.get()
    email = email_entry.get()
    telefone = telefone_entry.get()
    endereco = endereco_entry.get()
    data_nascimento = data_nascimento_entry.get()
   

    # Mapeamento de IntVar para string
    sexo = "Masculino" if sexo_var.get() == 1 else "Feminino" if sexo_var.get() == 2 else "Outro"
    
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="usuario"
        )

        cursor = conexao.cursor()
        cursor.execute("""
            INSERT INTO voluntario (nome, email, telefone, endereco, data_nascimento, sexo)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nome, email, telefone, endereco, data_nascimento, sexo))
        conexao.commit()
        mostrar_aviso("Voluntário cadastrado com sucesso!")
        cursor.close()
    except Error as e:
        mostrar_aviso(f"Erro ao cadastrar voluntário: {str(e)}")
    finally:
        if conexao.is_connected():
            conexao.close()
def ver_voluntario():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="usuario"
        )
        cursor = conexao.cursor()
        query = "SELECT * FROM `voluntario`"
        cursor.execute(query)
        resultados = cursor.fetchall()
        cursor.close()
        conexao.close()

        jan_res = Tk()
        jan_res.title("Resultados da Consulta")

        # Criar uma área de texto para exibir os resultados
        tex_res = Text(jan_res)
        tex_res.pack()

        # Exibir os resultados na área de texto
        for resultado in resultados:
            tex_res.insert(END, resultado)
            tex_res.insert(END, "\n")

        jan_res.mainloop()

    except mysql.connector.Error as err:
        print(f"Erro ao consultar o banco de dados: {err}")

def cadastrar_doacao():
    valor = valor_doacao_entry.get()

    if not valor:
        mostrar_aviso("Por favor, preencha todos os campos.")
    else:
        try:
            conexao = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="usuario"
            )

            cursor = conexao.cursor()
            cursor.execute("INSERT INTO doacao (id, valor, data_doacao) VALUES (NULL, %s, NOW())", (valor,))
            conexao.commit()
            cursor.close()
            conexao.close()
            mostrar_aviso("Doação cadastrada com sucesso!")
        except Error as e:
            mostrar_aviso(f"Erro ao cadastrar a doação: {str(e)}")
            if conexao.is_connected():
                conexao.close()
def ver_doacao():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="usuario"
        )
        cursor = conexao.cursor()
        query = "SELECT * FROM `doacao`"
        cursor.execute(query)
        resultados = cursor.fetchall()
        cursor.close()
        conexao.close()

        jan_res = Tk()
        jan_res.title("Resultados da Consulta")

        tex_res = Text(jan_res)
        tex_res.pack()

        # Exibir os resultados na área de texto
        for resultado in resultados:
            tex_res.insert(END, resultado)
            tex_res.insert(END, "\n")

        jan_res.mainloop()

    except mysql.connector.Error as err:
        print(f"Erro ao consultar o banco de dados: {err}")
        
def remover_doacao_por_id(id_doacao):
        try:
                conexao = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="root",
                        database="usuario"
                )

                if conexao.is_connected():
                        cursor = conexao.cursor()

                        cursor.execute("SELECT * FROM doacao WHERE id = %s", (id_doacao,))
                        doacao = cursor.fetchone()

                        if doacao:
                                cursor.execute("DELETE FROM doacao WHERE id = %s", (id_doacao,))
                                conexao.commit()
                                mostrar_aviso(f"doacao com ID {id_doacao} removido com sucesso!")
                        else:
                                mostrar_aviso(f"doacao com ID {id_doacao} não encontrado.")

                        cursor.close()

        except Error as e:
                mostrar_aviso(f"Erro ao remover o doacao: {str(e)}")

        finally:
                if conexao.is_connected():
                        conexao.close()

def remover_usuario_por_id(id_usuario):
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="usuario"
        )

        if conexao.is_connected():
            cursor = conexao.cursor()

            cursor.execute("SELECT * FROM usuario WHERE id = %s", (id_usuario,))
            usuario = cursor.fetchone()

            if usuario:
                cursor.execute("DELETE FROM usuario WHERE id = %s", (id_usuario,))
                conexao.commit()
                mostrar_aviso(f"Usuário com ID {id_usuario} removida com sucesso!")
            else:
                mostrar_aviso(f"Usuário com ID {id_usuario} não encontrada.")
            
            cursor.close()

    except Error as e:
        mostrar_aviso(f"Erro ao remover a Usuário: {str(e)}")

    finally:
        if conexao.is_connected():
            conexao.close()
            
def remover_voluntario_por_id(id_voluntario):
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="usuario"
        )

        if conexao.is_connected():
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM voluntario WHERE id = %s", (id_voluntario,))
            voluntario = cursor.fetchone()

            if voluntario:
                cursor.execute("DELETE FROM voluntario WHERE id = %s", (id_voluntario,))
                conexao.commit()
                mostrar_aviso(f"Voluntário com ID {id_voluntario} removido com sucesso!")
            else:
                mostrar_aviso(f"Voluntário com ID {id_voluntario} não encontrado.")
            
            cursor.close()

    except Error as e:
        mostrar_aviso(f"Erro ao remover o Voluntário: {str(e)}")

    finally:
        if conexao.is_connected():
            conexao.close()

def remover_doacao_window():
    window = Toplevel(w)
    window.title("Remover doacao por ID")
    window.geometry('300x300')

    def remover_doacao():
        id_doacao = entry_id_doacao.get()
        if id_doacao:
            remover_doacao_por_id(int(id_doacao))
        else:
            mostrar_aviso("Por favor, insira o ID do doacao.")
            
    label_id_doacao = Label(window, text="ID do doacao:")
    label_id_doacao.pack(pady=10)
    entry_id_doacao = Entry(window, width=10)
    entry_id_doacao.pack(pady=10)

    b_remover_doacao = Button(window, text="Remover doacao", width=15, height=2, command=remover_doacao)
    b_remover_doacao.pack(pady=10)

def remover_usuario_window():
    window = Toplevel(w)
    window.title("Remover Voluntário por ID")
    window.geometry('300x300')

    def remover_usuario():
        id_usuario = entry_id_usuario.get()
        
        if id_usuario:
            remover_usuario_por_id(int(id_usuario))
        else:
            mostrar_aviso("Por favor, insira o ID do Voluntário.")

    label_id_usuario = Label(window, text="ID do Voluntário:")
    label_id_usuario.pack(pady=10)
    entry_id_usuario = Entry(window, width=10)
    entry_id_usuario.pack(pady=10)

    b_remover_usuario = Button(window, text="Remover Voluntário", width=15, height=2, command=remover_usuario)
    b_remover_usuario.pack(pady=10)
    
def remover_voluntario_window():
    window = Toplevel(w)
    window.title("Remover Voluntário por ID")
    window.geometry('300x300')

    def remover_voluntario():
        id_voluntario = entry_id_voluntario.get()
        if id_voluntario:
            remover_voluntario_por_id(int(id_voluntario))
        else:
            mostrar_aviso("Por favor, insira o ID do Voluntário.")

    label_id_voluntario = Label(window, text="ID do Voluntário:")
    label_id_voluntario.pack(pady=10)
    entry_id_voluntario = Entry(window, width=10)
    entry_id_voluntario.pack(pady=10)

    b_remover_voluntario = Button(window, text="Remover Voluntário", width=20, height=2, command=remover_voluntario)
    b_remover_voluntario.pack(pady=10)
    
'''def atualizar_voluntario_por_id(
    novo_nome,
    novo_email,    
    id_voluntario,
    novo_telefone,
    nova_data_nascimento,
    novo_endereco,
    
):
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="usuario"
        )

        if conexao.is_connected():
            cursor = conexao.cursor()

            # Atualize os dados do Voluntário com base no ID
            sql = """
                UPDATE voluntario SET
                    nome = %s,
                    email = %s,
                    telefone = %s,
                    data_nascimento = %s,
                    endereco = %s,                 
                WHERE id = %s
            """
            valores = (
                novo_nome,
                novo_telefone,
                novo_email,
                nova_data_nascimento,
                novo_endereco,
                
                id_voluntario
            )
            cursor.execute(sql, valores)

            conexao.commit()
            mostrar_aviso(f"Voluntário com ID {id_voluntario} atualizado com sucesso!")

            cursor.close()

    except Error as e:
        mostrar_aviso(f"Erro ao atualizar o Voluntário: {str(e)}")

    finally:
        if conexao.is_connected():
            conexao.close()

def atualizar_voluntario_window():
    window = Toplevel(w)
    window.title("Atualizar Voluntário por ID")
    window.geometry('400x700')

    def atualizar_voluntario():
        voluntario_id = entry_id_voluntario.get()
        novo_nome = entry_novo_nome.get()
        novo_email = entry_novo_email.get()
        novo_telefone = entry_novo_telefone.get()
        nova_data_nascimento = entry_nova_data_nascimento.get()  
        novo_endereco = entry_novo_endereco.get()
        

        if voluntario_id and novo_nome and novo_email and novo_telefone and nova_data_nascimento and novo_endereco :

            atualizar_voluntario_por_id(
                voluntario_id,
                novo_nome,
                novo_email,
                novo_telefone,
                nova_data_nascimento,
                novo_endereco,
                
            )  # Fecha a janela após a atualização
        else:
            mostrar_aviso("Por favor, preencha todos os campos obrigatórios.")
        
    label_voluntario_id = Label(window, text="ID do Voluntário:")
    label_voluntario_id.grid(row=0, column=0, pady=10)
    entry_id_voluntario = Entry(window, width=10)
    entry_id_voluntario.grid(row=0, column=1, pady=10)

    label_novo_nome = Label(window, text="Novo Nome:")
    label_novo_nome.grid(row=1, column=0, pady=10)
    entry_novo_nome = Entry(window, width=30)
    entry_novo_nome.grid(row=1, column=1, pady=10)

    label_novo_email = Label(window, text="Novo Email:")
    label_novo_email.grid(row=2, column=0, pady=10)
    entry_novo_email = Entry(window, width=30)
    entry_novo_email.grid(row=2, column=1, pady=10)

    label_novo_telefone = Label(window, text="Novo Telefone:")
    label_novo_telefone.grid(row=3, column=0, pady=10)
    entry_novo_telefone = Entry(window, width=30)
    entry_novo_telefone.grid(row=3, column=1, pady=10)

    label_nova_data_nascimento = Label(window, text="Nova Data de Nascimento:")
    label_nova_data_nascimento.grid(row=4, column=0, pady=10)
    entry_nova_data_nascimento = Entry(window, width=30)
    entry_nova_data_nascimento.grid(row=4, column=1, pady=10)

    label_novo_endereco = Label(window, text="Novo endereco:")
    label_novo_endereco.grid(row=5, column=0, pady=10)
    entry_novo_endereco = Entry(window, width=30)
    entry_novo_endereco.grid(row=5, column=1, pady=10)


    b_atualizar_voluntario = Button(window, text="Atualizar Voluntário", width=20, height=2, command=atualizar_voluntario)
    b_atualizar_voluntario.grid(row=13, column=0, columnspan=2, pady=10)'''

def atualizar_usuario_por_id(
    id_usuario,
    novo_username,
    novo_email,
    nova_password
):
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="usuario"
        )

        if conexao.is_connected():
            cursor = conexao.cursor()

            sql = """
                UPDATE usuario SET
                    username = %s,
                    email = %s,
                    password = %s
                WHERE id = %s
            """
            valores = (
                novo_username,
                novo_email,
                nova_password,
                id_usuario
            )
            cursor.execute(sql, valores)

            conexao.commit()
            mostrar_aviso(f"Usuário com ID {id_usuario} atualizada com sucesso!")

            cursor.close()

    except Error as e:
        mostrar_aviso(f"Erro ao atualizar a Usuário: {str(e)}")

    finally:
        if conexao.is_connected():
            conexao.close()


def atualizar_usuario_window():

    window = Toplevel(w)
    window.title("Atualizar Usuário por ID")

    def atualizar_usuario():
        id_usuario = entry_id_usuario.get()
        novo_username = entry_novo_username.get()
        novo_password = entry_novo_password.get()
        novo_email = label_nova_email.get()

        if id_usuario and novo_username and novo_password and novo_email:
            atualizar_usuario_por_id(
                int(id_usuario),
                novo_username,
                novo_password,
                novo_email
            )  # Fecha a janela após a atualização
        else:
            mostrar_aviso("Por favor, preencha todos os campos obrigatórios.")

    label_id_usuario = Label(window, text="ID do Usuário:")
    label_id_usuario.grid(row=0, column=0, pady=10)
    entry_id_usuario = Entry(window, width=10)
    entry_id_usuario.grid(row=0, column=1, pady=10)

    label_novo_username = Label(window, text="Nome:")
    label_novo_username.grid(row=1, column=0, pady=10)
    entry_novo_username = Entry(window, width=30)
    entry_novo_username.grid(row=1, column=1, pady=10)

    label_novo_password = Label(window, text="senha:")
    label_novo_password.grid(row=2, column=0, pady=10)
    entry_novo_password = Entry(window, width=30)
    entry_novo_password.grid(row=2, column=1, pady=10)

    label_nova_email = Label(window, text="email:")
    label_nova_email.grid(row=3, column=0, pady=10)
    label_nova_email = Entry(window, width=30)
    label_nova_email.grid(row=3, column=1, pady=10)

    b_atualizar_usuario = Button(window, text="Atualizar Usuário", width=20, height=2, command=atualizar_usuario)
    b_atualizar_usuario.grid(row=4, column=0, columnspan=2, pady=10)

x = Menu(w)

arqvMenu = Menu(w, tearoff=0)

arqvMenu.add_command(label='Criar Banco Usuário', command=cdb)
arqvMenu.add_command(label='Criar Tabela Usuário', command=criar_tabela_usuario)
arqvMenu.add_command(label='Criar Tabela Voluntário', command=criar_tabela_voluntario)
arqvMenu.add_command(label='Criar Tabela Doação', command=criar_tabela_doacao)

x.add_cascade(label='Banco de Dados', menu=arqvMenu)

cadsusuMenu = Menu(w, tearoff=0)

cadsusuMenu.add_command(label='Remover', command = remover_usuario_window)
cadsusuMenu.add_command(label='Editar', command = atualizar_usuario_window)
cadsusuMenu.add_command(label='Ver', command = ver_usuario)

x.add_cascade(label="Usuário", menu=cadsusuMenu)

cadsMenu = Menu(w, tearoff=0)

cadsMenu.add_command(label='Remover', command = remover_voluntario_window)
#cadsMenu.add_command(label='Editar', command=atualizar_voluntario_window)
cadsMenu.add_command(label='Ver', command = ver_voluntario)

x.add_cascade(label="Voluntário", menu=cadsMenu)

cadsMenu = Menu(w, tearoff=0)

cadsMenu.add_command(label='Remover', command = remover_doacao_window)
cadsMenu.add_command(label='Ver',command = ver_doacao)

x.add_cascade(label="Doação", menu=cadsMenu)

w.config(menu=x)


bf_B = Button(w, text="Cadastrar Usuário", width=40, height=3, command=abrir_n_j_f)
bf_B.place(x=250, y=150)

bb_B = Button(w, text="Cadastrar voluntario", width=40, height=3, command=abrir_n_j_b)
bb_B.place(x=250, y=250)

bp_B = Button(w, text="Cadastrar Doação", width=40, height=3, command=abrir_n_j_p)
bp_B.place(x=250, y=350)

w.mainloop()
