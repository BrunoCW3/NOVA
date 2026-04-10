# 🧠 NOVA — Local AI Assistant in Python

## 📌 Overview

**NOVA** is a local artificial intelligence assistant that runs entirely on your machine using Ollama, with a graphical interface built in Python.

The project was designed with a focus on:

* independence from paid external APIs
* full control over data and memory
* stable performance on consumer hardware
* simple and modular architecture

NOVA provides a chat experience similar to ChatGPT, but fully offline and customizable.

---

## 🧩 Project Structure

```plaintext
NOVA/
├── core/
│   └── ai.py              # Handles communication with local AI (Ollama)
│
├── ui/
│   └── chat.py            # Graphical interface (Tkinter)
│
├── memory/
│   ├── base.txt           # Base system memory
│   └── extra1.txt         # Additional persistent memory
│
├── saved_chats/
│   └── oi.txt             # Saved conversations
│
├── config.txt             # Selected AI model
├── main.py                # Application entry point
```

> ⚠️ Folders like `__pycache__` and backup files are intentionally omitted.

---

## ⚙️ Technologies Used

* **Python 3**
* **Tkinter** — GUI framework
* **Ollama** — Local LLM runtime
* **Requests** — HTTP communication
* **Threading** — Non-blocking execution
* **Plain text files (.txt)** — Data persistence

---

## 🧠 How the System Works

### 🔹 Interface

The interface allows:

* sending messages to the AI
* real-time response streaming
* text selection and copying
* visual feedback while the AI is processing

---

### 🔹 AI Communication

The system communicates with Ollama through:

```plaintext
http://localhost:11434/api/generate
```

Flow:

1. User sends a message
2. System loads memory files
3. Builds a structured prompt
4. Sends request to the local model
5. Receives streamed response
6. Displays output progressively in the UI

---

### 🔹 Memory System

Persistent memory is stored as `.txt` files:

📁 Location:

```plaintext
AppData\Local\NOVA\memory
```

Features:

* create new memory entries
* edit existing ones
* view stored content
* delete memory files

The AI uses this memory as contextual input.

---

### 🔹 Chat System

* clear separation between **USER** and **NOVA**
* continuous multi-message interaction
* chat saving system (`saved_chats/`)
* ability to open saved conversations

---

### 🔹 Model Management

Available models:

* `phi3`
* `llama3:8b`

The selected model:

* is stored in `config.txt`
* triggers automatic restart when changed
* directly affects AI behavior and performance

---

## 💾 Data Persistence

No database is used.

All data is stored locally:

* memory → `memory/`
* chats → `saved_chats/`
* config → `config.txt`

---

## 🚀 How to Run

### 1. Install dependencies

```bash
pip install requests
```

---

### 2. Install Ollama

https://ollama.com

---

### 3. Download the models

```bash
ollama pull phi3
ollama pull llama3:8b
```

---

### 4. Run the project

```bash
python main.py
```

---

## 🎯 Project Goal

The main goal of NOVA is to build a fully functional, local AI assistant that operates without reliance on paid external services.

The project aims to:

* demonstrate real integration with local LLMs
* provide a usable and responsive interface
* implement a simple but effective memory system
* serve as a foundation for more advanced AI applications

---

## 🔮 Future Improvements

* semantic memory (embeddings)
* automatic chat history
* executable build (.exe)
* improved UI (web or custom frameworks)
* voice interaction

---

## 🤖 AI Assistance

This project was developed with the assistance of AI tools (ChatGPT) for:
- Code generation
- Debugging
- Architecture suggestions

All code was reviewed, adapted, and integrated manually.

---

## 🧠 Final Notes

NOVA is a practical implementation of a local AI system featuring:

* simple architecture
* full user control
* real-world usability

It serves both as a working tool and a learning platform for building more advanced AI systems.

---

## 👨‍💻 Author

BrunoCW3
Independent project focused on learning and technical development.
