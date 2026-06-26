# Sistema de Agenda para Clínica

Aplicação web de **agendamento de consultas** para clínicas, feita em **Flask + SQLite**,
estruturada para subir **de graça no PythonAnywhere**.

## Funcionalidades

- **Painel (dashboard)** com indicadores do dia e da semana
- **Agenda diária** por profissional, com grade de horários e navegação por dia
- **Cadastro de pacientes** (nome, CPF, nascimento, contato, observações) com busca
- **Cadastro de profissionais** (especialidade, registro, cor na agenda, ativo/inativo)
- **Agendamentos** com:
  - controle de **status**: agendado → confirmado → atendido / cancelado / faltou
  - **detecção de conflito de horário** por profissional
  - duração configurável e procedimento
- Interface responsiva (Bootstrap 5)

## Tecnologias

| Camada | Escolha |
|--------|---------|
| Backend | Flask 3 (app factory + blueprints) |
| ORM | Flask-SQLAlchemy |
| Banco | SQLite (zero configuração) |
| Frontend | Bootstrap 5 + Bootstrap Icons (via CDN) |

## Estrutura

```
Clinica/
├── app.py                  # app factory + entrada
├── config.py               # configurações (banco, horários da clínica)
├── extensions.py           # instância do SQLAlchemy
├── models.py               # Paciente, Profissional, Agendamento
├── seed.py                 # dados de exemplo (opcional)
├── requirements.txt
├── wsgi_pythonanywhere.py  # modelo do WSGI para deploy
├── blueprints/
│   ├── main.py             # dashboard
│   ├── pacientes.py
│   ├── profissionais.py
│   └── agendamentos.py     # agenda + agendamentos
├── templates/
└── static/css/
```

## Rodar localmente (Windows)

```powershell
cd "$env:USERPROFILE\Desktop\Clínica"
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python seed.py          # (opcional) cria dados de exemplo
python app.py
```

Acesse: http://127.0.0.1:5000

## Deploy no PythonAnywhere (grátis)

1. **Crie a conta** gratuita em https://www.pythonanywhere.com (plano "Beginner").

2. **Envie o código.** No menu **Files**, crie a pasta `Clinica` e faça upload dos
   arquivos, OU abra um **Bash console** e clone via Git (se você tiver subido para o GitHub):
   ```bash
   git clone https://github.com/SEUUSUARIO/Clinica.git
   ```

3. **Crie o virtualenv** no Bash console:
   ```bash
   cd ~/Clinica
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python seed.py        # opcional: dados de exemplo
   ```

4. **Crie a Web App.** Menu **Web > Add a new web app**:
   - Framework: **Manual configuration** (não escolha "Flask" automático)
   - Versão do Python: a mais nova disponível (ex.: 3.10+)

5. **Aponte o virtualenv.** Na página da Web app, campo **Virtualenv**:
   ```
   /home/SEUUSUARIO/Clinica/venv
   ```

6. **Configure o WSGI.** Clique no link do **WSGI configuration file**, apague todo o
   conteúdo e cole o que está em `wsgi_pythonanywhere.py` (trocando `SEUUSUARIO`):
   ```python
   import sys
   project_home = "/home/SEUUSUARIO/Clinica"
   if project_home not in sys.path:
       sys.path.insert(0, project_home)
   from app import app as application
   ```

7. **(Recomendado) Defina a SECRET_KEY.** Na seção *Web*, em "Environment variables",
   ou no topo do WSGI: `os.environ["SECRET_KEY"] = "uma-chave-bem-grande-e-secreta"`.

8. Clique em **Reload** (botão verde). Sua agenda estará em:
   ```
   https://SEUUSUARIO.pythonanywhere.com
   ```

### Observações do plano gratuito
- O banco **SQLite** já é suficiente; o arquivo `clinica.db` fica na própria pasta.
- A app "hiberna" após um tempo sem acesso e precisa de **1 reload a cada ~3 meses**
  (o PythonAnywhere avisa por e-mail).
- Os CDNs do Bootstrap carregam no navegador do usuário, então **não precisam** de
  liberação na whitelist do plano grátis.

## Próximos passos (ideias para evoluir)

- Login de usuários (Flask-Login)
- Lembrete por WhatsApp/e-mail
- Visão semanal e exportação da agenda
- Prontuário e módulo financeiro
```
