# MCP MVP Application

## Overview

This project demonstrates a simple MCP (Model Context Protocol) architecture consisting of:

- **MCP Client (Node.js + TypeScript)** – Receives user requests and communicates with MCP tools.
- **MCP Server (Python)** – Exposes tools via:
  - stdio (local MCP clients)
  - Streamable HTTP (remote usage)
- **LLM Provider Support**
  - Ollama
  - llama.cpp
- **Chat Interface** – Sends requests to MCP Client.

---

# Prerequisites

- Node.js 20+
- npm
- Python 3.11+
- uv

Verify:

```bash
node --version
npm --version
python --version
uv --version
```

---

# Project Structure

project-root/
├── package.json
├── mcp-client/
│   ├── src/
│   ├── dist/
│   └── package.json
├── mcp-server/
│   ├── src/
│   │   ├── run_stdio.py
│   │   ├── run_http.py
│   │   ├── server.py
│   │   ├── tools/
│   │   ├── prompts/
│   │   └── services/
│   └── pyproject.toml
└── README.md

---

# Installation

## MCP Client

cd mcp-client
npm install

## MCP Server

cd ../mcp-server
uv sync

## Build

npm run build

---

# Running

## Start full app

npm start

## MCP Server (stdio)

npm run start:mcp-server-local

## MCP Server (HTTP)

npm run start:mcp-server-remote

## Inspector

npm run inspect-server

---

# MCP Server Commands

cd mcp-server
uv run --with mcp src/run_stdio.py
uv run --with mcp src/run_http.py

---

# MCP Client Commands

cd mcp-client
npm run start

---

# LLM Providers

## Ollama

curl -fsSL https://ollama.com/install.sh | sh
ollama serve
ollama pull llama3
ollama run llama3

---

## llama.cpp

git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make -j

./llama-server -m models/model.gguf -c 4096

Endpoint:
http://localhost:8080

---

# Flow

User → MCP Client → MCP Server → Tool → MCP Client → UI
