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
            senha_desc =  senha_desc.replace("b'", "").replace("'", "")
            if senha == senha_desc:
                print("logou")
                return True
            else:
                print("Erro")
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
        senha = self.criptografar(senha)
        print(senha)
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

    def ver_senha(self, servico ,usuario):
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
        print("chave = " + str(self.chave))
        return Fernet(self.chave).decrypt(senha.decode("utf-8"))

g = Gerenciador()
