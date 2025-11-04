# Avaliador-de-etecs

Um aplicativo que avalia a "qualidade" das ETECs através de comentários de alunos ou professores da instituição.

## Como Funciona

O aplicativo permite que usuários (alunos e professores) façam login ou se cadastrem para avaliar ETECs. As principais funcionalidades incluem:

- **Lista de ETECs**: Visualize uma lista de ETECs disponíveis para avaliação.
- **Detalhes da ETEC**: Veja informações detalhadas sobre uma ETEC específica, incluindo avaliações e comentários.
- **Blog de Avaliações**: Acesse um blog com todas as avaliações e comentários feitos pelos usuários.
- **Perfil do Usuário**: Gerencie seu perfil, incluindo alteração de foto (que é exibida arredondada com borda), nome, email e senha.

O aplicativo utiliza uma interface gráfica em Tkinter, simulando uma tela de celular, e armazena dados em arquivos JSON locais.

## Instalação e Execução

### Pré-requisitos

- Python 3.7 ou superior instalado no sistema.

### Passos para Instalação

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu-usuario/avaliador-de-etecs.git
   cd avaliador-de-etecs
   ```

2. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

### Como Executar

1. Execute o aplicativo principal:
   ```bash
   python main.py
   ```

2. A interface gráfica será aberta. Faça login ou cadastre-se para começar a usar o aplicativo.

## Dependências

- **Pillow**: Para manipulação de imagens (usado para exibir fotos de perfil arredondadas).
- **psycopg2-binary**: Para conexão com banco de dados PostgreSQL (embora o aplicativo atual use arquivos JSON locais, essa dependência pode ser usada para futuras expansões).

## Estrutura do Projeto

- `main.py`: Arquivo principal que inicia a aplicação.
- `data.py`: Gerenciamento de dados (usuários, ETECs, avaliações).
- `profile.py`: Tela de perfil do usuário.
- `lista.py`: Lista de ETECs.
- `etec_details.py`: Detalhes de uma ETEC específica.
- `blog.py`: Blog de avaliações.
- `change_password.py`: Alteração de senha.
- `data/`: Diretório com arquivos JSON de dados.
- `images/`: Imagens das ETECs.
- `user_photos/`: Fotos de perfil dos usuários.
