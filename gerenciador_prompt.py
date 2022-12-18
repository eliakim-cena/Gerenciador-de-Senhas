import sqlite3
from cryptography.fernet import Fernet

class Gerenciador:
    def __init__(self):
        self.base_dados = "base.db"
        self.conn = sqlite3.connect(database=self.base_dados)
        self.cursor = self.conn.cursor()
        self.base = "services"
        self.op = ""
        self.chave = self.ler_chave()
        self.conectar()

    def logar(self, usuario, senha):
        self.cursor.execute(f"SELECT * FROM {self.base} WHERE service = "
                            "'Gerenciador' AND username = ?", (usuario,))
        for service in self.cursor.fetchall():
            senha_desc = str(self.descriptografar(service[2]))
            senha_desc = senha_desc.replace("b'", "").replace("'", "")
            if senha == senha_desc:
                return True
            else:
                return False

    def conectar(self):
        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {self.base}(
            service TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL);""")

    def ver_acesso(self):
        self.cursor.execute(f"SELECT * FROM {self.base} WHERE service = 'Gerenciador'")
        if not self.cursor.fetchall():
            return False
        else:
            return True

    def inserir(self, servico, usuario, senha):
        print(senha)
        senha = self.criptografar(senha)
        self.cursor.execute(f""" 
            INSERT INTO {self.base}
            VALUES  ( ?, ?, ?);""", (servico, usuario, senha))
        self.conn.commit()

    def atualiza(self, servico, usuario, senha):
        senha = self.criptografar(senha)
        self.cursor.execute(f"""
            UPDATE {self.base} SET password = ? WHERE service = ? AND username = ?;""", (senha, servico, usuario))
        self.conn.commit()

    def delete(self, servico, usuario):
        self.cursor.execute(f"""
            DELETE FROM {self.base} WHERE service = ? AND username = ?;""", (servico, usuario))
        self.conn.commit()

    def consulta(self, servico):
        self.cursor.execute(f"SELECT * FROM services WHERE service = ?", (servico,))

    def listar(self):
        self.cursor.execute(f"SELECT service, username, password FROM services;")
        lista = self.cursor.fetchall()
        for l in lista:
            print("Serviço: " + l[0], "Usuário: " + l [1], "Senha: " + str(l[2]))

    def ver_senha(self, servico, usuario):
        self.cursor.execute(f"SELECT * FROM {self.base} WHERE service = "
                            "? AND username = ?", (servico, usuario))
        for service in self.cursor.fetchall():
            senha = str(self.descriptografar(service[2])).replace("b", "").replace("'", "")
            return senha

    def gera_chave(self):
        self.chave = Fernet.generate_key()
        with open("encrypt.key", "wb") as key:
            key.write(self.chave)

    def ler_chave(self):
        try:
            with open("encrypt.key", "rb") as key:
                return key.read()
        except:
            self.gera_chave()

    def criptografar(self, senha):
        return Fernet(self.chave).encrypt(bytes(senha.encode("utf-8")))

    def descriptografar(self, senha):
        return Fernet(self.chave).decrypt(senha.decode("utf-8"))
    def menu_criar_acesso(self):
        print("**********************************************")
        print("*    Bem vindo ao Gerenciador de Senhas      *")
        print("**********************************************")
        print("* No momento não existe um usuário Gerenciador")
        print("* Por favor cadastrar um usuário e senha agora")
        print("**********************************************")
        s = False
        while s == False:
            usuario = input("         Usuário: ")
            senha = input("          Senha: ")
            senha2 = input("Confirme a senha: ")
            if senha == senha2:
                self.inserir("Gerenciador", usuario, senha)
                self.menu_principal()
                s = True
            else:
                print("Senhas Informadas não são iguais")

    def menu(sel1f):
        print("**************************************************")
        print("* 1 - Inserir novos dados                        *")
        print("* 2 - Listar dados registrados                   *")
        print("* 3 - Recuperar uma senha salva                  *")
        print("* 4 - Atualizar senha na base                    *")
        print("* 5 - Deletar um registro                        *")
        print("* S - Sair do sistema                            *")
        print("**************************************************")

    def menu_inserir(self):
        service = input("Informe o nome do serviço: ")
        username = input("Informe o usuário ou e-mail de acesso: ")
        password = input("Informe a senha para o serviço: ")
        if self.op == "1":
            self.inserir(service, username, password)
            print("Registro efetuado")
        elif self.op == "4":
            self.atualiza(service, username, password)
            print("Registro salvo")
    def menu_login(self):
        print("******************************************************************")
        print("*             Bem vindo ao Gerenciador de senhas                 *")
        print("******************************************************************")
        print("*             Informe abaixo os dados para acesso ao sistema     *")
        login = input("* Usuário:  ")
        senha = input("*   Senha:  ")
        if self.logar(login, senha) == True:
            self.menu_principal()
        else:
            print("Dados de acesso incorretos")
            self.menu_login()
    def menu_principal(self):
        while True:
            self.menu()
            self.op = input("O que deseja fazer? ")
            if self.op == "1" or self.op == "4":
                self.menu_inserir()
            elif self.op == "2":
                self.listar()
            elif self.op == "3":
                servico = input("Informe qual o serviço que deseja verificar: ")
                usuario = input("Informe qual o usuario do servico:")
                retorno = self.ver_senha(servico, usuario)
                print("Senha descriptografada: " + retorno)
            elif self.op == "5":
                servico = input("Informe qual o serviço que deseja remover: ")
                usuario = input("informe qual o usuário do serviço: ")
                self.delete(servico, usuario)
                print("Registro excluido")
            elif self.op.upper() == "S":
                self.menu_login()

gerenciador = Gerenciador()
if gerenciador.ver_acesso() == False:
    gerenciador.menu_criar_acesso()
else:
    gerenciador.menu_login()
