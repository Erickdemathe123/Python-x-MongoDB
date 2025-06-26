# 📚 API Python x MongoDB - Cadastro de Documentos

Este projeto é uma API feita em Python com Flask + MongoDB, criada para cadastro e pesquisa de documentos com base em nome, rua e filhos.

---

## ✅ Funcionalidades da API

| Endpoint              | Método | Descrição                          |
|-----------------------|--------|-----------------------------------|
| `/cadastrar`          | POST   | Cadastra um novo documento        |
| `/pesquisar_nome`     | GET    | Pesquisa por nome                 |
| `/pesquisar_rua`      | GET    | Pesquisa por nome da rua          |
| `/pesquisar_filhos`   | GET    | Pesquisa por nome dos filhos      |

---

## 🛠️ Requisitos

- Python 3 instalado
- MongoDB instalado e em execução local (`localhost:27017`)
- Postman (ou outro cliente REST)

---

## 🔧 Como configurar e rodar

### 1. Clone ou baixe o projeto

```bash
git clone <link_do_projeto>
cd <nome_da_pasta>
