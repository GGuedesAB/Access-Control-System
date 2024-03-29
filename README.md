# Sistema de Controle de Acesso

## Link Planilha de Apuração de Horas Trabalhadas e Gráfico de Burn-Down
https://docs.google.com/spreadsheets/d/1UihpmunBnBeLRJsAMpuaPuoDvKpMd1tuBW4egLVNJ4I/edit#gid=279617827

## Estórias e tarefas

##### E1 Como usuário, quero verificar a quais instalações tenho acesso
	T1 Implementar autenticação com senha para entrada no sistema [Leone][2hr]	
	T2 Implementar o setup do BD em SQL [Victor] [3hr]	
	T3 Implementar driver do banco de dados em Python [Victor][3hr]	
	T4 Implementar um setup dos pacotes do sistema [Gustavo][3hr]
	T5 Implementar o setup do MySQL para o sistema [Gustavo] [3hr]
	T6 Validar a integração entre as tarefas 2-5 [Victor] [5hr]
	T7 Implementar interface de execução terminal e gerar testes [Gustavo][15hr]

##### E2 Como usuário, quero meus dados em segurança
	T8 Implementar algoritmo de encrypt/decrypt em C/C++ [Leone][5hr]
	T9 Criptografar informações dos usuários no banco de dados [Victor] [3hr]
	T10 Desenvolver e validar integração SQL <-> Python <-> C [Victor][4hr]

##### E3 Como administrador, quero controlar cadastros e permissões de usuários
	T11 Implementar controle de acesso de usuário em Python [Leone][6hr]
	T12 Inserir níveis de permissão no banco de dados (grupos de acesso) [Victor][1hr]	
	T13 Inserir instalações no banco de dados [Victor][1hr]
	T14 Desenvolver interface de comandos para testes [Leone][7hr]
	T15 Associar operações de administrador a operações do BD [Victor][3hr]
		(adicionar, editar, remover)->(usuário, grupo de acesso, instalação)

##### E4 Como administrador, quero garantir que só eu posso gerenciar o sistema
	T16 Implementar autenticação de administrador [Victor][1hr]
	T17 Implementar um script de configuração automática do sistema [Gustavo][7hr]
	T18 Incluir 2 níveis de permissão para os comandos [Leone][1hr]
	
##### E5 Como usuário, quero ser identificado pelo celular
	T19 Incluir endereço MAC como atributo de usuário [Victor][1hr]
	T20 Implementar interface gráfica [Gustavo][15hr]
