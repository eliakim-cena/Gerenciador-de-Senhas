from gerenciador import Gerenciador
from registros import Registros
import PySimpleGUI as sg

class Programa:
    def __init__(self):
        self.g = Gerenciador()
        layout = [
            [sg.Text("Serviço", size=7), sg.Input(key="servico", size=30)],
            [sg.Text("Usuário", size=7), sg.Input(key="usuario", size=30)],
            [sg.Text("Senha", size=7), sg.Input(key="senha", size=20, password_char="*"), sg.Button("Ver", visible=False)],
            [sg.Button("Consulta"), sg.Button("Lista"), sg.Button("Limpar"),
             sg.Button("Cadastrar"), sg.Button("Atualizar", visible=False), sg.Button("Deletar", visible=False)]
        ]
        self.janela = sg.Window("Gerenciador de Senhas").layout(layout)
        while True:
            event, self.values = self.janela.read()
            if event == sg.WIN_CLOSED:
                break
            elif event == "Cadastrar":
                self.Salvar(1, self.values["servico"], self.values["usuario"], self.values["senha"])
                self.Limpar()
            elif event == "Consulta":
                servico = sg.PopupGetText("Informe o serviço que deseja consultar")
                self.g.consulta(servico, False)
                self.janela["Cadastrar"].update(visible=False)
                self.janela["Atualizar"].update(visible=True)
                self.janela["Deletar"].update(visible=True)
                self.janela["Ver"].update(visible=True)
                dados = self.g.cursor.fetchall()
                if len(dados) == 0:
                    sg.Popup("Nenhum registro encontrado com o nome informado")
                else:
                    self.Registros(dados)
            elif event == "Limpar":
                self.Limpar()
            elif event == "Ver":
                senha_desc = self.g.processa_criptografia(self.values["senha"], -7)
                sg.Popup(f"Senha: {senha_desc}")
            elif event == "Lista":
                try:
                    r = Registros()
                    dados = r.dados()
                    self.janela["servico"].update(dados[0])
                    self.janela["usuario"].update(dados[1])
                    self.janela["senha"].update(dados[2])
                    self.janela["Cadastrar"].update(visible=False)
                    self.janela["Atualizar"].update(visible=True)
                    self.janela["Deletar"].update(visible=True)
                    self.janela["Ver"].update(visible=True)
                except:
                    pass
            elif event == "Atualizar":
                self.Salvar(2,self.values["servico"], self.values["usuario"], self.values["senha"])
                self.Limpar()
            elif event == "Deletar":
                self.Deletar(self.values["servico"], self.values["usuario"])

    def Registros(self, dados):
        for dado in dados:
            self.janela["servico"].update(dado[0])
            self.janela["usuario"].update(dado[1])
            self.janela["senha"].update(dado[2])

    def Limpar(self):
        self.janela["servico"].update("")
        self.janela["usuario"].update("")
        self.janela["senha"].update("")
        self.janela["Deletar"].update(visible=False)
        self.janela["Atualizar"].update(visible=False)
        self.janela["Cadastrar"].update(visible=True)
        self.janela["Ver"].update(visible=False)

    def Salvar(self, op, servico, usuario, senha):
        if servico != "" and usuario != "" and senha != "":
            if op == 1:
                self.g.inserir(servico, usuario, senha)
            elif op == 2:
                self.g.atualiza(servico, usuario, senha)
            sg.Popup("Salvo")
        else:
            sg.Popup("Verifique os dados, há campo sem preencher")

    def Deletar(self, servico, usuario):
        if servico == "Gerenciador":
            sg.Popup("O Gerenciador não pode ser removido, caso deseje utilize a opção de atualizar para alterar o usuário e senha")
        else:
            if sg.PopupYesNo("Deseja confirmar a exclusão do registro?") == "Yes":
                self.g.delete(servico,usuario)
                sg.Popup("Registro Deletado")
                self.Limpar()
