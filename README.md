# Avaliador de ETECs

Um aplicativo desktop desenvolvido em Python para avaliação da qualidade das Escolas Técnicas Estaduais (ETECs) do estado de São Paulo, baseado em comentários e avaliações de alunos e professores. O sistema permite que usuários registrados compartilhem experiências e opiniões sobre as instituições, promovendo transparência e auxiliando na escolha educacional.

## Funcionalidades Principais

- **Autenticação de Usuários**: Sistema de login e cadastro para alunos e professores.
- **Lista de ETECs**: Visualização de uma lista completa de ETECs disponíveis para avaliação.
- **Detalhes da ETEC**: Informações detalhadas sobre cada instituição, incluindo avaliações, comentários e imagens.
- **Sistema de Avaliação**: Possibilidade de avaliar ETECs com estrelas (1-5) e comentários.
- **Blog de Avaliações**: Plataforma para visualizar todas as avaliações e comentários publicados.
- **Perfil do Usuário**: Gerenciamento de perfil pessoal, incluindo foto (exibida com borda arredondada), nome, email e alteração de senha.
- **Interface Intuitiva**: Design responsivo simulando uma tela de celular, desenvolvido com Tkinter.

## Pré-requisitos

- **Python**: Versão 3.7 ou superior instalada no sistema.
- **Sistema Operacional**: Compatível com Windows, macOS ou Linux.

## Instalação

Siga os passos abaixo para configurar o ambiente de desenvolvimento e executar o aplicativo:

### 1. Clonagem do Repositório

Clone o repositório para sua máquina local:

```bash
git clone https://github.com/seu-usuario/avaliador-de-etecs.git
cd avaliador-de-etecs
```

### 2. Instalação das Dependências

Instale as bibliotecas necessárias utilizando o arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

Este comando instalará automaticamente as seguintes dependências:
- **Pillow**: Para manipulação e exibição de imagens de perfil.
- **psycopg2-binary**: Preparado para futuras integrações com banco de dados PostgreSQL (atualmente o sistema utiliza arquivos JSON locais).

## Execução

Após a instalação, execute o aplicativo seguindo estes passos:

### 1. Inicialização do Aplicativo

Execute o arquivo principal `main.py` para iniciar a aplicação:

```bash
py main.py
```

### 2. Uso da Aplicação

1. **Tela Inicial**: A interface gráfica será aberta, simulando uma tela de celular.
2. **Cadastro/Login**: Selecione "Ir para Cadastro" para criar uma nova conta ou faça login com credenciais existentes.
3. **Navegação**: Após o login, acesse as funcionalidades através do menu principal:
   - **Lista de Etecs**: Visualize e selecione ETECs para avaliação.
   - **Blog de Avaliações**: Leia comentários e avaliações de outros usuários.
   - **Meu Perfil**: Gerencie suas informações pessoais.
4. **Avaliação**: Em uma ETEC específica, adicione estrelas e comentários para contribuir com a comunidade.


## Tecnologias Utilizadas

- **Python 3.7+**: Linguagem de programação principal.
- **Tkinter**: Biblioteca padrão para criação da interface gráfica.
- **Pillow**: Manipulação de imagens para fotos de perfil.
- **JSON**: Armazenamento local de dados (usuários, ETECs, avaliações).
- **psycopg2-binary**: Preparado para integração futura com PostgreSQL.
 :)