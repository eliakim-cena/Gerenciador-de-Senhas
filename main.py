from gerenciador import Gerenciador
from programa import Programa
import PySimpleGUI as sg

class Login:
    def __init__(self):
        layout = [
            [sg.Text("Login", size=13), sg.Input(key="usuario", size=30)],
            [sg.Text("Senha", size=13), sg.Input(key="senha", size=30, password_char="*")]
        ]
        self.gerenciador = Gerenciador()
        self.gerenciador.conectar(self.gerenciador.base)
        if self.gerenciador.ver_acesso() == False:
            layout.append([sg.Text("Confirme a Senha", key="lconfirma"), sg.Input(key="csenha", password_char="*", size=30)])
            layout.append([sg.Button("Cadastrar")])
        else:
            layout.append([sg.Button("Logar")])
        self.janela = sg.Window("Gerenciador de Senhas", layout=layout)
        while True:
            event, values = self.janela.read()
            if event == sg.WIN_CLOSED:
                break
            elif event == "Logar":
                self.logar(values["usuario"], values["senha"])
            elif event == "Cadastrar":
                self.cadastra_acesso(values["usuario"], values["senha"], values["csenha"])

    def cadastra_acesso(self, usuario, senha, csenha):
        if usuario != "":
            if senha == csenha and senha != "":
                 self.gerenciador.inserir("Gerenciador", usuario, senha)
                 sg.Popup("Usuário Cadastrado")
                 self.logar(usuario, senha)
            else:
                sg.Popup("Verifique os dados informados, os campos 'Senha' e 'Confirma Senha' não foram preenchidos ou estão diferentes")
        else:
            sg.Popup("Sem usuário informado no campo Usuário")

    def logar(self, usuario, senha):
        logado = self.gerenciador.logar(usuario, senha)
        if logado == True:
            self.janela.close()
            p = Programa()
        else:
            sg.Popup("Dados de acesso incorretos")

login = Login()
