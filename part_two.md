# Processo de criação do Chatbot com Crawler e Busca

Nesta etapa do projeto, foi necessário criar um chatbot capaz de fazer webscraping, armazenar dados em um banco de dados e responder a consultas de busca. Para isso, foram seguidos os passos descritos no README.md.

## Configuração do ambiente e instalação de dependências

Para fazer o webscraping, foi necessário instalar as bibliotecas BeautifulSoup4 e requests, além da biblioteca discord.py para criar e configurar o bot do Discord. Também foi utilizado o banco de dados SQLite e a biblioteca SQLAlchemy para armazenar os dados coletados pelo webscraping. Para instalar as dependências, foi utilizado o gerenciador de pacotes pip e o arquivo requirements.txt.

## Configuração do bot do Discord

O bot do Discord foi criado utilizando a biblioteca discord.py e configurado para receber comandos dos usuários, como o comando \crawl xxx para fazer o webscraping de uma URL e o comando \search xxx para buscar termos ou conceitos no banco de dados.

## Configuração do banco de dados

Foi utilizado o banco de dados SQLite para armazenar os dados coletados pelo webscraping. A tabela pages foi criada com as colunas id, url, title e content, onde id é a chave primária, url é a URL da página, title é o título da página e content é o conteúdo da página.

## Implementação do webscraping

O webscraping foi implementado utilizando a biblioteca BeautifulSoup4 para fazer o parsing do HTML das páginas e a biblioteca requests para fazer as requisições HTTP. O bot armazena o título, o conteúdo e a URL de cada página no banco de dados e segue os links nas páginas para coletar mais dados e adicioná-los ao banco de dados.

## Implementação da busca usando um índice invertido

Para responder às consultas de busca, foi criado um índice invertido que mapeia cada palavra em cada documento para a lista de documentos que contêm essa palavra. Isso permite que o bot responda rapidamente a consultas de busca, procurando apenas as palavras que correspondem à consulta.

## Implementação da busca usando um índice de semelhança baseado em Wordnet

Foi implementado um índice de semelhança baseado em Wordnet para fazer uma busca mais avançada. O bot utiliza a biblioteca nltk para acessar o Wordnet e encontrar sinônimos e palavras relacionadas à consulta do usuário. Isso permite que o bot encontre documentos que não contenham exatamente a consulta do usuário, mas que ainda sejam relevantes.

## Configuração das respostas do bot

Com base nas consultas de busca do usuário, o bot fornece uma resposta com uma lista de documentos que correspondem à consulta. As respostas do bot foram formatadas utilizando a biblioteca discord.py e enviadas para o usuário do Discord.

## Conclusão

A implementação do chatbot com crawler e busca foi um desafio interessante e envolveu diversos aspectos da programação, desde a configuração do ambiente até a implementação dos algoritmos de webscraping e busca. Durante o processo de desenvolvimento, uma das maiores dificuldades encontradas foi a implementação do crawling de forma eficiente e escalável. Inicialmente, implementamos o crawling de maneira recursiva, seguindo cada link encontrado na página atual. No entanto, essa abordagem logo se mostrou ineficiente para lidar com grandes quantidades de dados, já que a recursão pode se tornar muito profunda e consumir muita memória.

Para resolver esse problema, optamos por implementar o crawling usando uma abordagem baseada em filas, em que armazenamos os links a serem processados em uma fila e iteramos sobre ela até que ela esteja vazia. Dessa forma, podemos lidar com grandes quantidades de dados de forma mais eficiente, sem consumir excessivamente a memória.

Outra dificuldade encontrada foi a implementação da busca usando um índice invertido. Apesar de ser uma abordagem eficiente para lidar com consultas de busca, a construção de um índice invertido pode ser bastante complexa e exigir um grande esforço computacional. Para contornar esse problema, utilizamos a biblioteca Whoosh, que fornece uma implementação de índice invertido já pronta e fácil de usar.
