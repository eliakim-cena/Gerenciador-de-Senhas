# Gerenciador de Senhas
Projeto de um Gerenciador de Acesso criado em Python, onde pode ser cadastrados dados de acessos a sites e sistemas para ser recuperado quando necessário lembrar os dados de acesso. 
 
Neste projeto foram Usadas as biblioteca PySimpleGUI para criação de Interface, a biblioteca cryptography.fernet para criptografar a senha salva na base e a Sqlite3 para uso de um arquivo de banco de dados. 
No projeto há também uma versão que roda no terminal, utilizando comandos para execução das funções do sistema de acordo com o que deseja fazer. 

O sistema possui ao iniciar a primeira vez, cria a base de dados e solicita a criação do usuário de acesso ao sistema, efetuando o login após este cadastro. 
Ao logar no sistema, há as opções de listar todos os registros, cadastrar, consultar, atualizar e deletar e a opção de visualizar a senha, descriptografando e mostrando em tela. 

Inicial - Cadastro do usuário Gerenciador

<img width="274" alt="cadastra" src="https://user-images.githubusercontent.com/120613380/207892452-b2ce1687-7ebf-447a-9a75-d8f7320d4364.png">

Login

<img width="274" alt="login" src="https://user-images.githubusercontent.com/120613380/207897981-26948df6-68e5-48b5-994b-e2d29d013ce1.png">

Dentro do sistema

<img width="249" alt="programa" src="https://user-images.githubusercontent.com/120613380/207892924-3c999d7f-77b9-45da-bec9-1842b18143ee.png">

Exemplo da tela mostrando a senha criptografada:

<img width="262" alt="senha cripto" src="https://user-images.githubusercontent.com/120613380/208325933-7c0f07c1-0bbc-43cf-ba17-ae7b47f867ea.png">

Ao clicar para ver a senha. 

<img width="93" alt="mostra_senha" src="https://user-images.githubusercontent.com/120613380/208325948-e25359a9-e788-4e2e-8adf-f0e66ed7daf5.png">

Consulta por nome do serviço registrado

<img width="264" alt="consulta" src="https://user-images.githubusercontent.com/120613380/207893011-165b5596-5497-42c6-bc72-5e219a7c48f5.png">

Lista de acessos cadastrados. 

<img width="170" alt="lista" src="https://user-images.githubusercontent.com/120613380/207893502-2fd84c9e-c4e6-435e-9630-92649db06b17.png">
