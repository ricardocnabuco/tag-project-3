# tag-project-3
# Nome: Ricardo de Carvalho Nabuco Matrícula 231021360
# Projeto de Teoria e Aplicação de Grafos 3
1- Introdução:
Este projeto aplica métodos de coloração de grafos para solucionar um desafio relacionado à programação de jogos em um torneio de futebol. O conceito principal é descrever cada partida entre duas equipes como um nó em um grafo, onde as conexões ligam partidas que não podem ser realizadas na mesma rodada – seja por compartilharem uma equipe ou devido a restrições específicas (como regras de mandante e rodadas proibidas). Através de um algoritmo de retrocesso, o sistema distribui as rodadas (representadas por cores) às partidas de modo que todas as limitações sejam atendidas, possibilitando a criação de um cronograma eficaz e a visualização do grafo com a organização dos jogos por rodada.
![image](https://github.com/user-attachments/assets/b304d9e2-b40f-48f4-9bb8-20f33ab7c6b7)
2- Solução:
---> Com isso, fiz uma implementação em python:
---> Requisitos: Este projeto foi desenvolvido em Python 3.9.6 e utiliza as seguintes bibliotecas:
---> networkx: para a construção e manipulação do grafo.
---> matplotlib: para a visualização do grafo com cores que representam as rodadas.
---> itertools e collections: para a criação de combinações de jogos e manipulação de contadores.
---> matplotlib.patches: para a criação de legendas na visualização.

3- Como executar o projeto:
-1. Abra o projeto:
cd /caminho/para/o/projeto
-2. Configura e ativa o Ambiente Virtual:
python3 -m venv venv

%^ No macOs ou Linux:
source venv/bin/activate

%^ No Windows:
venv\Scripts\activate

-3. Instalar as Dependências:
pip install -r requirements.txt

-4. Executar o Projeto:
python projeto3.py

-5. Fechar o Ambiente Virtual
deactivate
