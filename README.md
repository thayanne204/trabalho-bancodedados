# trabalho-bancodedados
# 🥗 Sistema de Recomendação de Receitas Fitness

Trabalho de Banco de Dados Vetoriais  
Universidade: SANTO AGOSTINHO 
Curso: ENGENHARIA DE SOFTWARE
Professor: ANDERSON SOARES  

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Database-green.svg)](https://www.trychroma.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Sobre o Projeto

Sistema de recomendação de receitas fitness utilizando **banco de dados vetorial (ChromaDB)** e **modelos de IA (Sentence Transformers)** para busca por similaridade semântica.

### 🎯 Objetivos
- Implementar um banco de dados vetorial local
- Criar sistema de busca inteligente por receitas
- Desenvolver API REST para integração
- Demonstrar aplicação prática de IA em BD

## 🏗️ Arquitetura
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Usuário │────▶│ API │────▶│ ChromaDB │
│ (n8n/Web) │ │ FastAPI │ │ Vector │
└─────────────┘ └─────────────┘ └─────────────┘
│ │
└──────▶[Modelo IA]◀┘
SentenceTransformer


## ⚙️ Tecnologias Utilizadas

- **Python 3.11** - Linguagem principal
- **ChromaDB 0.4.18** - Banco de dados vetorial
- **Sentence Transformers** - Modelo de embeddings
- **FastAPI** - Framework para API REST
- **NumPy** - Computação numérica

## 📦 Instalação e Execução

### Pré-requisitos
```bash
Python 3.11+
Git
