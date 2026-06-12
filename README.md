# MCP MVP Application

## Overview

This project demonstrates a simple MCP (Model Context Protocol) architecture consisting of:

* **MCP Client (Node.js + TypeScript)** - Receives user requests and communicates with MCP tools.
* **MCP Server (Python)** - Exposes tools over Streamable HTTP.
* **LLM Provider Support**

  * Ollama
  * llama.cpp
* **Chat Interface** - Sends requests to the MCP Client.

---

# Prerequisites

Install the following:

* Node.js 20+
* npm
* Python 3.11+
* uv

Verify installation:

```bash
node --version
npm --version
python --version
uv --version
```

---

# Project Structure

```text
project-root/
│
├── package.json
│
├── mcp-client/
│   ├── src/
│   ├── dist/
│   └── package.json
│
├── mcp-server/
│   ├── main.py
│   └── pyproject.toml
│
└── README.md
```

---

# Installation

## 1. Install MCP Client Dependencies

```bash
cd mcp-client
npm install
```

## 2. Install MCP Server Dependencies

```bash
cd ../mcp-server
uv sync
```

## 3. Build Entire Project

From project root:

```bash
npm run build
```

This executes:

```bash
npm run build:server
npm run build:client
```

Where:

```bash
build:server -> cd mcp-server && uv sync
build:client -> cd mcp-client && npm run build
```

---

# Running the Application

## Start Everything

From project root:

```bash
npm start
```

This runs both services in parallel:

```bash
run:server -> cd mcp-server && uv run --with mcp main.py
run:client -> cd mcp-client && npm run start
```

---

# Available Root Scripts

| Command              | Description                              |
| -------------------- | ---------------------------------------- |
| npm run build        | Build entire project                     |
| npm run build:server | Install/update Python dependencies       |
| npm run build:client | Compile TypeScript client                |
| npm start            | Start MCP Server and MCP Client together |
| npm run run:server   | Start Python MCP Server                  |
| npm run run:client   | Start Node.js MCP Client                 |

---

# MCP Client Commands

Navigate to:

```bash
cd mcp-client
```

### Build

```bash
npm run build
```

### Start Client

```bash
npm run start
```

### Start with Ollama

```bash
npm run start:ollama
```

### Start with llama.cpp

```bash
npm run start:llamacpp
```

---

# MCP Server Commands

Navigate to:

```bash
cd mcp-server
```

### Install Dependencies

```bash
uv sync
```

### Start Streamable HTTP MCP Server

```bash
uv run --with mcp main.py
```

---

# End-to-End Startup

### Step 1

Build project:

```bash
npm run build
```

### Step 2

Start application:

```bash
npm start
```

### Step 3

Open the chat application and send a message.

Flow:

```text
User
  ↓
Chat Application
  ↓
MCP Client
  ↓
MCP Server (Streamable HTTP)
  ↓
Tool Execution
  ↓
MCP Client
  ↓
Chat Application
```

---

# Supported Providers

The MCP Client currently supports:

* Ollama
* llama.cpp

Examples:

```bash
cd mcp-client

npm run start:ollama
```

or

```bash
npm run start:llamacpp
```

---

<!-- # MVP Goal

This MVP demonstrates:

* MCP Client ↔ MCP Server communication
* Streamable HTTP transport
* Tool discovery and execution
* Local LLM integration
* End-to-end chat workflow
* Foundation for future privacy and security tooling -->

#### Ollama
- Install Ollama using
`curl -fsSL https://ollama.com/install.sh | sh` or visit ollama.com
- Start Ollama: `ollama serve`
- Check if Ollama is running: `curl http://localhost:11434`.
- Download a LLM: `ollama pull <model_name>`.
- Start inference session with a model name: `ollama run <model_name>`.
- List current local models: `ollama list`
- List all currently loaded or running AI models in Ollama: `ollama ps`


```
```

