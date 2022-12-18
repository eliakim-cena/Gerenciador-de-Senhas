from gerenciador import Gerenciador
import PySimpleGUI as sg

class Registros:
    def __init__(self):
        self.g = Gerenciador()
        self.g.listar()
        dados = self.g.cursor.fetchall()
        head = ["Serviço", "Usuário", "Senha"]
        layout = [
            [sg.Text("Serviços")],
            [sg.Table(values=dados, headings=head, key="servicos",
                      enable_events=True, visible_column_map=[True, True, False])]
        ]
        self.janela = sg.Window("Gerenciador de Senhas", layout=layout)

        while True:
            event, values = self.janela.read()
            if event == sg.WIN_CLOSED:
                break
            elif event == "servicos":
                index = values["servicos"][0]
                self.selecao = dados[index]
                self.janela.close()

    def dados(self):
        dados_retorno = list(self.selecao)
        return dados_retorno

