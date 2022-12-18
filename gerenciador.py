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
        senha_decritp = self.processa_criptografia(senha, 7)
        self.cursor.execute(f"SELECT * FROM {self.base} WHERE service = "
                            "'Gerenciador' AND username = ? AND password = ?", (usuario, senha_decritp))
        for service in self.cursor.fetchall():
            if service:
                return True
            else:
                return False

    def conectar(self, base):
        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {base}(
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
        senha = self.processa_criptografia(senha, 7)
        self.cursor.execute(f""" 
            INSERT INTO {self.base}
            VALUES  ( ?, ?, ?);""", (servico, usuario, senha))
        self.conn.commit()

    def atualiza(self, servico, usuario, senha):
        senha = self.processa_criptografia(senha, 7)
        self.cursor.execute(f"""
            UPDATE {self.base} SET password = ? WHERE service = ? AND username = ?;""", (senha, servico, usuario))
        self.conn.commit()

    def delete(self, servico, usuario):
        self.cursor.execute(f"""
            DELETE FROM {self.base} WHERE service = ? AND username = ?;""", (servico, usuario))
        self.conn.commit()

    def consulta(self, servico):
        self.cursor.execute(f"SELECT * FROM services WHERE service = ?;", servico)

    def listar(self):
        self.cursor.execute(f"SELECT service, username, password FROM services;")

    def processa_criptografia(self, dados, chave):
        novo_dado = ""
        for letra in dados:
             novo_dado = novo_dado + chr((ord(letra) + chave) % self.n)
        return novo_dado

