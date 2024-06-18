from tkinter import *
from tkinter import ttk
import tkinter.messagebox as tkmb
import mysql.connector
from customtkinter import *
import customtkinter as ctk
from mysql.connector import connect, Error
from datetime import datetime
import tkinter as tk
from PIL import Image, ImageTk
w = Tk()
w.title("Subúrbio em Transe ")
w.wm_iconbitmap('images/suburbio.ico')
largura = 1000
altura = 800
largura_screen = w.winfo_screenwidth()
altura_screen = w.winfo_screenheight()
posx = largura_screen/2 - largura/2
posy = altura_screen/2 - altura/2
w.geometry('%dx%d+%d+%d' % (largura, altura, posx, posy))
w.minsize(width=1000, height=800)
w.resizable(False, False)
set_appearance_mode("light")

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

# FRONT --------------------------------------------------------------------------------------------------------------------------------

sidebar_frame = CTkFrame(master=w, fg_color="#050505",  width=200, height=650, corner_radius=0)
sidebar_frame.pack_propagate(0)
sidebar_frame.pack(fill="y", anchor="w", side="left")

logo_img_data = Image.open("images/suburbio_logo.png")
logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(180, 75.42))

CTkButton(master=sidebar_frame, command=lambda: controller.show_frame("pagina_inicial"), text="", fg_color="transparent", hover_color="#050505", image=logo_img).pack(pady=(38, 0), anchor="center")

cadastrar_img_data = Image.open("images/cadastrar.png")
cadastrar_img = CTkImage(dark_image=cadastrar_img_data, light_image=cadastrar_img_data)
CTkButton(master=sidebar_frame, command=lambda: controller.show_frame("cadastrar_voluntario_front"), image=cadastrar_img, text="Cadastrar Voluntário", fg_color="transparent", font=("Arial Bold", 14), hover_color="#3b3b3b", anchor="w", width=170, height=20).pack(ipady=5, pady=(38, 0))

remover_img_data = Image.open("images/remover.png")
remover_img = CTkImage(dark_image=remover_img_data, light_image=remover_img_data)
CTkButton(master=sidebar_frame, command=lambda: controller.show_frame("remover_voluntario_front"), image=remover_img, text="Remover Voluntário", fg_color="transparent", font=("Arial Bold", 14), hover_color="#3b3b3b", anchor="w", width=170, height=20).pack(ipady=5, pady=(15, 0))

ver_img_data = Image.open("images/ver.png")
ver_img = CTkImage(dark_image=ver_img_data, light_image=ver_img_data)
CTkButton(master=sidebar_frame, image=ver_img, command=ver_voluntario, text="Ver Voluntários", fg_color="transparent", font=("Arial Bold", 14), hover_color="#3b3b3b", anchor="w", width=170, height=20).pack(ipady=5, pady=(15, 0))

cadastrar_img_data2 = Image.open("images/cadastrar.png")
cadastrar_img2 = CTkImage(dark_image=cadastrar_img_data2, light_image=cadastrar_img_data2)
CTkButton(master=sidebar_frame, command=lambda: controller.show_frame("cadastrar_usuario_front"), image=cadastrar_img2, text="Cadastrar Usuário", fg_color="transparent", font=("Arial Bold", 14), hover_color="#3b3b3b", anchor="w", width=170, height=20).pack(ipady=5, pady=(15, 0))

atualizar_img_data2 = Image.open("images/atualizar.png")
atualizar_img2 = CTkImage(dark_image=atualizar_img_data2, light_image=atualizar_img_data2)
CTkButton(master=sidebar_frame, command=lambda: controller.show_frame("atualizar_usuario_front"),image=atualizar_img2, text="Atualizar Usuário", fg_color="transparent", font=("Arial Bold", 14), hover_color="#3b3b3b", anchor="w", width=170, height=20).pack(ipady=5, pady=(15, 0))

remover_img_data2 = Image.open("images/remover.png")
remover_img2 = CTkImage(dark_image=remover_img_data2, light_image=remover_img_data2)
CTkButton(master=sidebar_frame, command=lambda: controller.show_frame("remover_usuario_front"), image=remover_img2, text="Remover Usuário", fg_color="transparent", font=("Arial Bold", 14), hover_color="#3b3b3b", anchor="w", width=170, height=20).pack(ipady=5, pady=(15, 0))

ver_img_data2 = Image.open("images/ver.png")
ver_img2 = CTkImage(dark_image=ver_img_data2, light_image=ver_img_data2)
CTkButton(master=sidebar_frame, image=ver_img2, text="Ver Usuários", command=ver_usuario, fg_color="transparent", font=("Arial Bold", 14), hover_color="#3b3b3b", anchor="w", width=170, height=20).pack(ipady=5, pady=(15, 0))

doacao_img_data = Image.open("images/doacao.png")
doacao_img = CTkImage(dark_image=doacao_img_data, light_image=doacao_img_data)
CTkButton(master=sidebar_frame, command=lambda: controller.show_frame("cadastrar_doacao_front"), image=doacao_img, text="Cadastrar doação", fg_color="transparent", font=("Arial Bold", 14), hover_color="#3b3b3b", anchor="w", width=170, height=20).pack(ipady=5, pady=(15, 0))

remover_img_data3 = Image.open("images/delete.png")
remover_img3 = CTkImage(dark_image=remover_img_data3, light_image=remover_img_data3)
CTkButton(master=sidebar_frame, command=lambda: controller.show_frame("remover_doacao_front"), image=remover_img3, text="Remover doação", fg_color="transparent", font=("Arial Bold", 14), hover_color="#3b3b3b", anchor="w", width=170, height=20).pack(ipady=5, pady=(15, 0))

ver_img_data3 = Image.open("images/ver.png")
ver_img3 = CTkImage(dark_image=ver_img_data3, light_image=ver_img_data3)
CTkButton(master=sidebar_frame, image=ver_img3, text="Ver doações", command=ver_doacao, fg_color="transparent", font=("Arial Bold", 14), hover_color="#3b3b3b", anchor="w", width=170, height=20).pack(ipady=5, pady=(15, 0))

sair_img_data = Image.open("images/sair.png")
sair_img = CTkImage(dark_image=sair_img_data, light_image=sair_img_data)
CTkButton(master=sidebar_frame, command=sair, image=sair_img, text="Sair",fg_color="#3b3b3b", font=("Verdana Bold", 14), hover_color="#3b3b3b", anchor="w").pack(anchor="center", ipady=5, pady=(15, 0))

# FUNÇÕES ------------------------------------------------------------------------------------------------

pages_fm = CTkFrame(master=w, width=800, height=800, corner_radius=0)
pages_fm.pack_propagate(0)
pages_fm.pack(fill="y", anchor="w", side="right")

def pagina_inicial():
    pagina_inicial_fm = CTkFrame(master=pages_fm, width=550, height=570, fg_color='transparent')
    pagina_inicial_fm.place(relx=0.5, rely=0.5, anchor="center")

    pagina_inicial_data = Image.open("images/suburbio_logo2.png")
    pagina_inicial_img = CTkImage(dark_image=pagina_inicial_data, light_image=pagina_inicial_data, size=(500, 400))

    background_label = CTkLabel(master=pagina_inicial_fm, text="", image=pagina_inicial_img)
    background_label.place(relx=0.5, rely=0.5, anchor="center")

    botao_criar_banco = CTkButton(master=pagina_inicial_fm, text='Criar Banco Usuário', command=cdb, width=180, height=40, font=("Arial Bold", 17), hover_color="#3b3b3b", fg_color="#050505", text_color="#fff")
    botao_criar_banco.place(x=100, y=450)

    botao_criar_tabela_usuario = CTkButton(master=pagina_inicial_fm, text='Criar Tabela Usuário', command=criar_tabela_usuario, width=180, height=40, font=("Arial Bold", 17), hover_color="#3b3b3b", fg_color="#050505", text_color="#fff")
    botao_criar_tabela_usuario.place(x=300, y=450)

    botao_criar_tabela_voluntario = CTkButton(master=pagina_inicial_fm, text='Criar Tabela Voluntário', command=criar_tabela_voluntario, width=180, height=40, font=("Arial Bold", 17), hover_color="#3b3b3b", fg_color="#050505", text_color="#fff")
    botao_criar_tabela_voluntario.place(x=100, y=500)

    botao_criar_tabela_doacao = CTkButton(master=pagina_inicial_fm, text='Criar Tabela Doação', command=criar_tabela_doacao, width=180, height=40, font=("Arial Bold", 17), hover_color="#3b3b3b", fg_color="#050505", text_color="#fff")
    botao_criar_tabela_doacao.place(x=300, y=500)

    controller.add_frame("pagina_inicial", pagina_inicial_fm)

def cadastrar_voluntario_front():

    global nome_entry, email_entry, telefone_entry, data_nascimento_entry, endereco_entry, sexo_var

    cadastrar_voluntario_pagina_fm =  CTkFrame(master=pages_fm, width=550, height=570, fg_color='transparent')
    cadastrar_voluntario_pagina_fm.place(relx=0.5, rely=0.5, anchor="center")

    nome_label = CTkLabel(master=cadastrar_voluntario_pagina_fm, text='Nome', font=("Bold", 18))
    nome_label.place(x=55, y=50)
    nome_entry = CTkEntry(master=cadastrar_voluntario_pagina_fm, fg_color="#F0F0F0", border_width=0,height=30, width=200)
    nome_entry.place(x=55, y=80)

    email_label = CTkLabel(master=cadastrar_voluntario_pagina_fm, text='Email', font=("Bold", 18))
    email_label.place(x=295, y=50)
    email_entry = CTkEntry(master=cadastrar_voluntario_pagina_fm, fg_color="#F0F0F0", border_width=0,height=30, width=200)
    email_entry.place(x=295, y=80)

    telefone_label = CTkLabel(master=cadastrar_voluntario_pagina_fm, text='Telefone', font=("Bold", 18))
    telefone_label.place(x=55, y=130)
    telefone_entry = CTkEntry(master=cadastrar_voluntario_pagina_fm, fg_color="#F0F0F0", border_width=0,height=30, width=200)
    telefone_entry.place(x=55, y=160)

    data_nascimento_label = CTkLabel(master=cadastrar_voluntario_pagina_fm, text='Data de nascimento', font=("Bold", 18))
    data_nascimento_label.place(x=295, y=130)
    data_nascimento_entry = CTkEntry(master=cadastrar_voluntario_pagina_fm, fg_color="#F0F0F0", border_width=0,height=30, width=200)
    data_nascimento_entry.place(x=295, y=160)

    rua_label = CTkLabel(master=cadastrar_voluntario_pagina_fm, text='Endereço', font=("Bold", 18))
    rua_label.place(x=55, y=210)
    endereco_entry = CTkEntry(master=cadastrar_voluntario_pagina_fm, fg_color="#F0F0F0", border_width=0,height=30, width=440)
    endereco_entry.place(x=55, y=240)

    sexo_label = CTkLabel(master=cadastrar_voluntario_pagina_fm, text='Sexo', font=("Bold", 18))
    sexo_label.place(x=55, y=290)
    sexo_var = IntVar()
    masculino_rdb = CTkRadioButton(master=cadastrar_voluntario_pagina_fm, variable=sexo_var, value=1, text="Masculino", font=("Arial Bold", 14), fg_color="black", border_color="black", hover_color="#404040")
    masculino_rdb.place(x=55, y=325)
    feminino_rdb = CTkRadioButton(master=cadastrar_voluntario_pagina_fm, variable=sexo_var, value=2,text="Feminino", font=("Arial Bold", 14), fg_color="black", border_color="black", hover_color="#404040")
    feminino_rdb.place(x=55, y=355)

    botao_cadastrar_usuario = CTkButton(master=cadastrar_voluntario_pagina_fm, text='Cadastrar voluntário', command=cadastrar_voluntario, width=180, height=40, font=("Arial Bold", 17), hover_color="#3b3b3b", fg_color="#050505", text_color="#fff")
    botao_cadastrar_usuario.place(x=175, y=430)
    criar_tabela_voluntario()

    controller.add_frame("cadastrar_voluntario_front", cadastrar_voluntario_pagina_fm)

def remover_voluntario_front():

    def remover_voluntario():
        id_voluntario = entry_id_voluntario.get()
        if id_voluntario:
            remover_voluntario_por_id(int(id_voluntario))
        else:
            mostrar_aviso("Por favor, insira o ID do Voluntário.")

    remover_voluntario_pagina_fm =  CTkFrame(master=pages_fm, width=550, height=570, fg_color='transparent')
    remover_voluntario_pagina_fm.place(relx=0.5, rely=0.5, anchor="center")

    remover_voluntario_label_1 = CTkLabel(master=remover_voluntario_pagina_fm, text='Insira o ID do voluntário', font=("Bold", 25))
    remover_voluntario_label_1.place(x=142, y=200) 

    entry_id_voluntario = CTkEntry(master=remover_voluntario_pagina_fm, fg_color="#F0F0F0", border_width=1, border_color="black", width=250)
    entry_id_voluntario.place(x=150, y=250)

    b_remover_voluntario = CTkButton(master=remover_voluntario_pagina_fm, command=remover_voluntario, text="Remover", width=100, font=("Arial Bold", 17), hover_color="#3b3b3b", fg_color="#050505", text_color="#fff")
    b_remover_voluntario.place(x=220, y=300)

    controller.add_frame("remover_voluntario_front", remover_voluntario_pagina_fm)

def cadastrar_usuario_front():

    global username_entry, password_entry, email_entry

    cadastrar_usuario_pagina_fm =  CTkFrame(master=pages_fm, width=550, height=570, fg_color='transparent')
    cadastrar_usuario_pagina_fm.place(relx=0.5, rely=0.5, anchor="center")

    username_label = CTkLabel(master=cadastrar_usuario_pagina_fm, text='Nome', font=("Bold", 18))
    username_label.place(x=50, y=50)
    username_entry = CTkEntry(master=cadastrar_usuario_pagina_fm, fg_color="#F0F0F0", border_width=0,height=30, width=200)
    username_entry.place(x=50, y=80)

    password_label = CTkLabel(master=cadastrar_usuario_pagina_fm, text='Senha', font=("Bold", 18))
    password_label.place(x=290, y=50)
    password_entry = CTkEntry(master=cadastrar_usuario_pagina_fm, fg_color="#F0F0F0", border_width=0,height=30, width=200, show="*")
    password_entry.place(x=290, y=80)

    email_label = CTkLabel(master=cadastrar_usuario_pagina_fm, text='Email', font=("Bold", 18))
    email_label.place(x=50, y=130)
    email_entry = CTkEntry(master=cadastrar_usuario_pagina_fm, fg_color="#F0F0F0", border_width=0, height=30, width=440)
    email_entry.place(x=50, y=160)

    bcb_f = CTkButton(master=cadastrar_usuario_pagina_fm, command=cadastrar_usuario, text='Cadastrar usuário', width=180, height=40, font=("Arial Bold", 17), hover_color="#3b3b3b", fg_color="#050505", text_color="#fff")
    bcb_f.place(x=170, y=220)
    criar_tabela_usuario()

    controller.add_frame("cadastrar_usuario_front", cadastrar_usuario_pagina_fm)

def atualizar_usuario_front():

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

    atualizar_usuario_pagina_fm =  CTkFrame(master=pages_fm, width=550, height=570, fg_color='transparent')
    atualizar_usuario_pagina_fm.place(relx=0.5, rely=0.5, anchor="center")

    label_novo_username = CTkLabel(master=atualizar_usuario_pagina_fm, text='Novo nome', font=("Bold", 18))
    label_novo_username.place(x=50, y=50)
    entry_novo_username = CTkEntry(master=atualizar_usuario_pagina_fm, fg_color="#F0F0F0", border_width=0,height=30, width=200)
    entry_novo_username.place(x=50, y=80)

    label_novo_password = CTkLabel(master=atualizar_usuario_pagina_fm, text='Nova senha', font=("Bold", 18))
    label_novo_password.place(x=290, y=50)
    entry_novo_password = CTkEntry(master=atualizar_usuario_pagina_fm, fg_color="#F0F0F0", border_width=0,height=30, width=200, show="*")
    entry_novo_password.place(x=290, y=80)

    label_nova_email = CTkLabel(master=atualizar_usuario_pagina_fm, text='Novo email', font=("Bold", 18))
    label_nova_email.place(x=50, y=130)
    label_nova_email = CTkEntry(master=atualizar_usuario_pagina_fm, fg_color="#F0F0F0", border_width=0, height=30, width=200)
    label_nova_email.place(x=50, y=160)

    label_id_usuario = CTkLabel(master=atualizar_usuario_pagina_fm, text='ID do usuário', font=("Bold", 18))
    label_id_usuario.place(x=290, y=130)
    entry_id_usuario = CTkEntry(master=atualizar_usuario_pagina_fm, fg_color="#F0F0F0", border_width=0,height=30, width=200)
    entry_id_usuario.place(x=290, y=160)

    b_atualizar_usuario = CTkButton(master=atualizar_usuario_pagina_fm, command=atualizar_usuario, text='Atualizar usuário', width=180, height=40, font=("Arial Bold", 17), hover_color="#3b3b3b", fg_color="#050505", text_color="#fff")
    b_atualizar_usuario.place(x=170, y=220)

    controller.add_frame("atualizar_usuario_front", atualizar_usuario_pagina_fm)

def remover_usuario_front():

    def remover_usuario():
        id_usuario = entry_id_usuario.get()
        
        if id_usuario:
            remover_usuario_por_id(int(id_usuario))
        else:
            mostrar_aviso("Por favor, insira o ID do Voluntário.")

    remover_usuario_pagina_fm =  CTkFrame(master=pages_fm, width=550, height=570, fg_color='transparent')
    remover_usuario_pagina_fm.place(relx=0.5, rely=0.5, anchor="center")

    label_id_usuario = CTkLabel(master=remover_usuario_pagina_fm, text='Insira o ID do usuário', font=("Bold", 25))
    label_id_usuario.place(x=155, y=200) 
    entry_id_usuario = CTkEntry(master=remover_usuario_pagina_fm, fg_color="#F0F0F0", border_width=1, border_color="black", width=250)
    entry_id_usuario.place(x=150, y=250)

    b_remover_usuario = CTkButton(master=remover_usuario_pagina_fm, text="Remover", command=remover_usuario, width=100, font=("Arial Bold", 17), hover_color="#3b3b3b", fg_color="#050505", text_color="#fff")
    b_remover_usuario.place(x=220, y=300)

    controller.add_frame("remover_usuario_front", remover_usuario_pagina_fm)


def cadastrar_doacao_front():

    global valor_doacao_entry

    cadastrar_doacao_pagina_fm =  CTkFrame(master=pages_fm, width=550, height=570, fg_color='transparent')
    cadastrar_doacao_pagina_fm.place(relx=0.5, rely=0.5, anchor="center")

    valor_doacao_label = CTkLabel(master=cadastrar_doacao_pagina_fm, text='Valor da doação', font=("Bold", 25))
    valor_doacao_label.place(relx=0.5, rely=0.35, anchor="center") 

    valor_doacao_entry = CTkEntry(master=cadastrar_doacao_pagina_fm, fg_color="#F0F0F0", border_width=1, border_color="black", width=250)
    valor_doacao_entry.place(relx=0.5, rely=0.45, anchor="center")

    bcb_p = CTkButton(master=cadastrar_doacao_pagina_fm, text="Cadastrar", command=cadastrar_doacao, width=120, font=("Arial Bold", 17), hover_color="#3b3b3b", fg_color="#050505", text_color="#fff")
    bcb_p.place(relx=0.5, rely=0.55, anchor="center")
    criar_tabela_doacao()

    controller.add_frame("cadastrar_doacao_front", cadastrar_doacao_pagina_fm)

def remover_doacao_front():

    def remover_doacao():
        id_doacao = entry_id_doacao.get()
        if id_doacao:
            remover_doacao_por_id(int(id_doacao))
        else:
            mostrar_aviso("Por favor, insira o ID do doacao.")

    remover_doacao_pagina_fm =  CTkFrame(master=pages_fm, width=550, height=570, fg_color='transparent')
    remover_doacao_pagina_fm.place(relx=0.5, rely=0.5, anchor="center")

    label_id_doacao = CTkLabel(master=remover_doacao_pagina_fm, text='ID da doação', font=("Bold", 25))
    label_id_doacao.place(relx=0.5, rely=0.35, anchor="center") 

    entry_id_doacao = CTkEntry(master=remover_doacao_pagina_fm, fg_color="#F0F0F0", border_width=1, border_color="black", width=250)
    entry_id_doacao.place(relx=0.5, rely=0.45, anchor="center")

    b_remover_doacao = CTkButton(master=remover_doacao_pagina_fm, text="Remover",command=remover_doacao, width=120, font=("Arial Bold", 17), hover_color="#3b3b3b", fg_color="#050505", text_color="#fff")
    b_remover_doacao.place(relx=0.5, rely=0.55, anchor="center")

    controller.add_frame("remover_doacao_front", remover_doacao_pagina_fm)

class Controller:
    def __init__(self, container):
        self.container = container
        self.frames = {}

    def add_frame(self, name, frame):
        self.frames[name] = frame

    def show_frame(self, frame_name):
        frame = self.frames.get(frame_name)
        if frame:
            frame.tkraise()
    
controller = Controller(pages_fm)

cadastrar_voluntario_front()
remover_voluntario_front()
cadastrar_usuario_front()
atualizar_usuario_front()
cadastrar_doacao_front()
remover_doacao_front()
remover_usuario_front()
pagina_inicial()

controller.show_frame("pagina_inicial")


w.mainloop()
