# LangGraph Mock Demo

A small LangGraph example without:
- OpenAI APIs
- Ollama
- Local LLMs

The goal is to demonstrate:
- shared state
- nodes
- routing
- graph execution
- Mermaid/PNG diagram generation

---

# Install

Create venv:

```bash
python -m venv .venv 
``` 
Activate venv:

```bash
source .venv/bin/activate
``` 

Install langgraph
```bash
pip install langgraph
```

Optional for PNG generation:

```bash
# Arch Linux
sudo pacman -S graphviz

# Debian/Ubuntu
sudo apt install graphviz
```

---

# Run

Run demo:

```bash
python demo.py
```

This will:
- execute the graph
- generate `workflow.mmd`
- generate `workflow.png`

---

# Workflow

```text
START
  ↓
classifier
  ├── math → math_handler
  └── general → general_handler
                ↓
               END
```

---

# State Evolution

Initial state:

```python
{
    "user_input": "can you add numbers?"
}
```

After classifier:

```python
{
    "user_input": "can you add numbers?",
    "intent": "math"
}
```

Final state:

```python
{
    "user_input": "can you add numbers?",
    "intent": "math",
    "response": "Pretend I solved a math problem here."
}
```

---

# Core Idea

Each node:
1. receives the current state
2. processes data
3. returns updates

LangGraph merges the updates into shared state automatically.

Example:

```python
return {
    "intent": "math"
}
```

This is what makes the workflow progress through the graph.