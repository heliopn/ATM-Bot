# Modificações no Projeto

Foi realizada a mudança do banco de dados SQLite para o MySQL para lidar com grandes quantidades de dados de forma mais eficiente. Foi utilizada a biblioteca PyMySQL para fazer a conexão e executar consultas no banco de dados MySQL.
Classificação de Sentimento

Foi implementado um classificador de sentimento utilizando a biblioteca NLTK. A coluna sentiment foi adicionada à tabela pages para armazenar o sentimento da página, que pode ser positivo, negativo ou neutro. O classificador utiliza a técnica de análise de sentimento baseada em léxicos para classificar o sentimento das páginas. Isso permite que o bot retorne páginas relevantes com base no sentimento da consulta do usuário.

## Requirements

    Python 3.8 or higher
    Flask
    MySQL Connector
    NLTK
