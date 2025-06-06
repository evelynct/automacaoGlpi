# 🤖 Automação de Distribuição de Chamados – GLPI

Este repositório contém uma automação desenvolvida para otimizar o processo de **distribuição de chamados** no sistema **GLPI** dentro da empresa.  
A rotina, que antes era feita manualmente, agora é realizada automaticamente a cada **30 minutos**, garantindo **agilidade**, **equidade** e **eficiência operacional**. ⏱️⚙️

---

## 🧠 Objetivo

Automatizar a atribuição de chamados com status `"Novo"` (`status: 1`) para um grupo específico de técnicos, de forma **igualitária**, com base na quantidade atual de chamados atribuídos a cada um.

---

## ✅ Funcionalidades

- 🔐 Autenticação segura via App-Token e credenciais do GLPI  
- 🧾 Consulta de chamados com status **Novo**  
- 👥 Identificação de técnicos pertencentes a um grupo específico  
- 📊 Verificação de quantidade de chamados atribuídos por técnico  
- 🧮 Ordenação por menor carga atual de chamados  
- 🎯 Atribuição automática dos chamados ao técnico com menor fila  
- 🔁 Execução programada a cada 30 minutos (via `crontab`, `Task Scheduler`, etc)

---

## 🧰 Tecnologias Utilizadas

- 🐍 **Python 3**
- 🌐 `requests` para chamadas HTTP à API GLPI
- 📁 JSON para leitura de credenciais
- 🔄 Integração com **API REST do GLPI**

---

## 🗂️ Estrutura do Projeto

```
bot_glpi_base/
├── config/
│   └── credenciais_glpi.json   # Arquivo com as credenciais da API
├── main.py                     # Script principal da automação
```

---

## 🔐 Configuração

Crie um arquivo `credenciais_glpi.json` dentro da pasta `config/` com o seguinte conteúdo:

```json
{
  "Url_Base": "https://seu-glpi.com/apirest.php",
  "App-Token": "SEU_APP_TOKEN",
  "User": "usuario",
  "Senha": "senha"
}
```

> ⚠️ **Importante:** Nunca envie esse arquivo para repositórios públicos!

---

## ⏱️ Agendamento da Automação

Para rodar a automação a cada 30 minutos, você pode configurar um agendador.  
Exemplo com `crontab` (Linux/macOS):

```bash
*/30 * * * * /usr/bin/python3 /caminho/para/seu/script/main.py
```

---

## 🙋‍♀️ Autor(a)

Feito com 💙 por [@evelynct](https://github.com/evelynct)
