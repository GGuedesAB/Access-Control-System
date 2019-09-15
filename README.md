# Access-Control-System
Software engineering discipline's project.

Tarefas

Sistema de Controle de Acesso

Estórias
	Tarefas


E1 Como usuário, quero verificar a quais instalações tenho acesso
	
	T1 Implementar autenticação com senha para entrada no sistema
 [Leone][2hr]	
	T2 Implementar um banco de dados para controle de acesso e armazenamento de cadastros [Victor][3hr]	
	T3 Implementar driver de banco de dados em Python
 [Victor][3hr]	
	T4 Implementar setup do BD em SQL [Victor][3hr]	
	T5 Desenvolver banco de dados no MySQL
	[Victor][3hr]
	T6 Desenvolver interface gráfica para visualização usando GTK [Gustavo][15hr]



E2 Como usuário, quero meus dados em segurança
	
	T7 Implementar algoritmo de encrypt/decrypt em C/C++
 [Leone][5hr]
	T8 Fazer driver em Python para associação com o banco de dados
	 [Victor][3hr]
	T9 Desenvolver e validar integração SQL <-> Python <-> C [Victor][4hr]



E3 Como administrador, quero controlar cadastros e permissões de usuários
	
	T10 Implementar controle de acesso de usuário em Python
	[Leone][6hr]
	T11 Inserir níveis de permissão no banco de dados (grupos de acesso)
 [Victor][1hr]	
	T12 Inserir instalações no banco de dados [Victor][1hr]
	T13 Desenvolver interface de comandos primária, para testes
 [Leone][7hr]
	T14 Associar operações de administrador a operações do BD 
 [Victor][3hr]
			(adicionar, editar, remover)->(usuário, grupo de acesso, instalação)



E4 Como administrador, quero garantir que só eu posso gerenciar o sistema

	T15 Implementar autenticação de administrador [Victor][1hr]
	T16 Incluir 2 níveis de permissão para os comandos [Leone][1hr]



E5 Como usuário, quero ser identificado pelo celular

	T17 Incluir endereço MAC como atributo de usuário
 [Victor][1hr]
	T18 Integrar interface de comunicação do Raspberry Pi no sistema [Gustavo][15hr]
