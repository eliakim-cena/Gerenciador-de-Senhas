import sqlite3

class Gerenciador:
    def __init__(self):
        self.base_dados = "base.db"
        self.conn = sqlite3.connect(database=self.base_dados)
        self.cursor = self.conn.cursor()
        self.n = 128
        self.base = "services"
        self.op = ""

    def logar(self, usuario, senha):
        self.cursor.execute(f"""
                    SELECT * FROM {self.base} WHERE service = 'Gerenciador' AND username = '{usuario}';""")
        for service in self.cursor.fetchall():
            senha_decritp = self.processa_criptografia(service[2], -7)
            if senha_decritp == senha:
                self.menu_principal()
            else:
                print("*** Informações de acesso incorretas     ***")
                self.menu_login()

    def conectar(self, base):
        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {base}(
            service TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL);""")

    def ver_acesso(self):
        self.cursor.execute(f"""
                    SELECT * FROM {self.base} WHERE service = 'Gerenciador';""")
        if not self.cursor.fetchall():
            s = False
            print("**********************************************")
            print("*    Bem vindo ao Gerenciador de Senhas      *")
            print("**********************************************")
            print("* No momento não existe um usuário Gerenciador")
            print("* Por favor cadastrar um usuário e senha agora")
            print("**********************************************")
            while s == False:
                usuario = input("         Usuário: ")
                senha = input("          Senha: ")
                senha2 = input("Confirme a senha: ")
                if senha == senha2:
                    senha = self.processa_criptografia(senha, 7)
                    self.inserir("Gerenciador", usuario, senha)
                    s = True
                else:
                    print("Senhas Informadas não são iguais")

    def inserir(self, servico, usuario, senha):
        self.cursor.execute(f""" 
            INSERT INTO {self.base}
            VALUES  ('{servico}','{usuario}','{senha}');""")
        self.conn.commit()

    def atualiza(self, servico, usuario, senha):
        self.cursor.execute(f"""
            UPDATE {self.base} SET password = '{senha}' WHERE service = '{servico}' AND username = 
            '{usuario}';""")
        self.conn.commit()

    def delete(self, servico, usuario):
        self.cursor.execute(f"""
            DELETE FROM {self.base} WHERE service = '{servico}' AND username = '{usuario}';""")
        self.conn.commit()

    def consulta(self, servico, descript):
        self.cursor.execute(f"""
            SELECT * FROM {self.base} WHERE service = '{servico}';""")
        for service in self.cursor.fetchall():
                if descript == True:
                    senha = self.processa_criptografia(service[2], -7)
                    print(f" Serviço: {service[0]} Usuário: {service[1]} Senha: {senha}")
                else:
                    print(f" Serviço: {service[0]} Usuário: {service[1]} Senha: {service[2]}")

    def listar(self):
        self.cursor.execute(f"""SELECT service, username FROM {self.base};""")
        for service in self.cursor.fetchall():
            print(f" Serviço: {service[0]} Usuário: {service[1]}")

    def processa_criptografia(self, dados, chave):
        novo_dado = ""
        for letra in dados:
             novo_dado = novo_dado + chr((ord(letra) + chave) % self.n)
        return novo_dado

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
            password = self.processa_criptografia(password, 7)
            self.inserir(service, username, password)
        elif self.op == "4":
            password = self.processa_criptografia(password, 7)
            self.atualiza(service, username, password)

    def menu_login(self):
        print("******************************************************************")
        print("*             Bem vindo ao Gerenciador de senhas                 *")
        print("******************************************************************")
        print("*             Informe abaixo os dados para acesso ao sistema     *")
        login = input("* Usuário:  ")
        senha = input("*   Senha:  ")
        self.logar(login, senha)

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
                descript = input("Descriptografada? S/N: ")
                if descript.upper() == "S":
                    self.consulta(servico, True)
                else:
                    self.consulta(servico, False)
            elif self.op == "5":
                servico = input("Informe qual o serviço que deseja remover: ")
                usuario = input("informe qual o usuário do serviço: ")
                self.delete(servico, usuario)
            elif self.op.upper() == "S":
                self.menu_login()
            elif self.op == "666":
                self.base = "secret"
            elif self.op == "0":
                self.base = "services"
gerenciador = Gerenciador()
gerenciador.conectar(gerenciador.base)
#gerenciador.ver_acesso()
#gerenciador.menu_login()
gerenciador.menu_principal()
gerenciador.conn.close()
