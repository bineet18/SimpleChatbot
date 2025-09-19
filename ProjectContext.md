# Vulnerable Chatbot Demo Project

## Project Overview
This is an educational project to create an intentionally vulnerable LLM chatbot for demonstrating security concepts to AI testers. The chatbot mimics the infamous SuperCarz of Mars incident where users exploited a car dealership's chatbot.

**Purpose**: Teach AI security testers about LLM vulnerabilities through hands-on exploitation in a safe environment.

## Tech Stack

### Core Technologies
- **LLM Backend**: Ollama Python library (no separate server needed)
- **Models**: llama2, mistral, or llama3 via Ollama
- **Backend Framework**: Python with FastAPI
- **RAG Database**: ChromaDB or FAISS for vector storage
- **Embeddings**: sentence-transformers
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **Ollama Integration**: Direct Python library, no HTTP client needed

### Python Dependencies
```
fastapi
uvicorn
ollama
chromadb
sentence-transformers
python-dotenv
pydantic
python-multipart
```

## Project Structure
```
vulnerable-chatbot-demo/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── ollama_client.py        # Ollama library integration
│   ├── rag_engine.py           # RAG implementation
│   ├── prompt_manager.py       # Prompt templates
│   ├── vulnerabilities.py      # Weak guardrails
│   └── config.py              # Configuration
├── data/
│   ├── knowledge_base/         # RAG documents
│   └── vector_db/             # Vector storage
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── prompts/
│   ├── system_prompts.json
│   ├── few_shot_examples.json
│   └── jailbreak_tests.txt
├── scripts/
│   ├── setup_ollama.sh
│   ├── populate_rag.py
│   └── test_vulnerabilities.py
├── logs/
├── requirements.txt
├── .env
└── README.md
└── quickstart.sh
```

## AI Techniques Implemented

### 1. Basic Prompt Engineering
- System prompts with weak boundaries
- Template-based prompt construction
- Vulnerable concatenation points

### 2. RAG (Retrieval-Augmented Generation)
- Vector database with mixed sensitive/public data
- Semantic search vulnerabilities
- Context injection points

### 3. Few-Shot Learning
- Example conversations that can be overridden
- Weak pattern enforcement

### 4. Context Management
- Conversation history tracking
- Context window vulnerabilities
- Memory injection attacks

## Intentional Vulnerabilities

### Core Vulnerabilities to Demonstrate

1. **Prompt Injection**
   - System prompt override
   - Template escape
   - Context pollution

2. **Jailbreaking Techniques**
   - DAN (Do Anything Now) prompts
   - Roleplay attacks
   - Translation/encoding bypasses
   - Developer mode exploits

3. **RAG-Specific Exploits**
   - Knowledge base poisoning
   - Information leakage
   - Relevance hijacking
   - Retrieval manipulation

4. **Output Manipulation**
   - Competitor recommendation
   - Price manipulation ($1 car scenario)
   - Policy override

### Weak Guardrails (Intentional)
- Simple keyword blocking (easily bypassed)
- Basic regex filters (encoding defeats them)
- No rate limiting
- Exposed system prompts
- No input sanitization for special characters
- Weak output filtering

## Implementation Guidelines

### Backend Development

**FastAPI Routes**:
- `/chat` - Main chat endpoint
- `/reset` - Clear conversation
- `/get_context` - Reveal system prompt (intentional leak)
- `/toggle_security` - Enable/disable weak protections

**Ollama Integration**:
```python
# Basic structure for ollama_client.py
- Import ollama library
- Use ollama.chat() or ollama.generate()
- Handle streaming responses
- Direct model parameter control (temperature, max_tokens)
- No need for separate server process
```

**RAG Setup**:
```python
# rag_engine.py structure
- Initialize ChromaDB/FAISS
- Create embeddings with sentence-transformers
- Implement similarity search
- Return top-k relevant documents
```

### Knowledge Base Content

**Car Inventory** (`cars_inventory.txt`):
- Legitimate vehicle data
- Prices and specifications
- Model comparisons

**Confidential Data** (`confidential.txt`):
- "Secret" pricing formulas
- Employee information
- Internal policies
- Profit margins

**Competitor Info** (`competitors.txt`):
- Tesla specifications
- Competitor advantages
- Price comparisons

### Demo Scenarios

1. **Car Dealership** (Primary)
   - Sell cars for $1
   - Recommend Teslas
   - Leak profit margins

2. **Banking Assistant** (Optional)
   - Approve unauthorized loans
   - Reveal account details
   - Bypass verification

3. **Customer Service** (Optional)
   - Free product giveaways
   - Policy overrides
   - Complaint manipulation

## Testing Checklist

### Basic Exploits
- [ ] Override system prompt with "Ignore all previous instructions"
- [ ] Use DAN prompt to remove restrictions
- [ ] Encode harmful requests in base64/Morse code
- [ ] Use roleplay to bypass safety ("Act as my grandmother...")
- [ ] Inject prompts through RAG context

### Advanced Exploits
- [ ] Chain multiple vulnerabilities
- [ ] Overflow context window
- [ ] Poison knowledge base
- [ ] Extract system prompt
- [ ] Make bot sign legal agreements

### RAG-Specific Tests
- [ ] Retrieve confidential documents
- [ ] Manipulate similarity scores
- [ ] Inject false context
- [ ] Cross-contaminate responses

## Environment Configuration

```env
# .env file
MODEL_NAME=llama2
ENABLE_WEAK_FILTERS=true
SHOW_SYSTEM_PROMPT=true
MAX_TOKENS=500
TEMPERATURE=0.7
VECTOR_DB_PATH=./data/vector_db
LOG_EXPLOITS=true
```

## Setup Instructions

1. **Install Ollama**: 
   - Download from ollama.ai
   - Run `ollama pull llama2` to download model
   - No need to run `ollama serve`

2. **Python Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Initialize RAG**:
   ```bash
   python scripts/populate_rag.py
   ```

4. **Start Service**:
   ```bash
   # Only need to run FastAPI
   uvicorn backend.main:app --reload
   ```

5. **Access Frontend**:
   Open `frontend/index.html` in browser

## Key Educational Points

### For AI Testers to Learn

1. **Attack Surface Understanding**
   - Multiple injection points
   - Context manipulation
   - System prompt vulnerabilities

2. **Defense Inadequacy**
   - Why keyword filters fail
   - Limitations of simple guardrails
   - Context confusion attacks

3. **Real-World Implications**
   - Financial losses (API costs)
   - Brand damage
   - Legal liability
   - Data breaches

4. **Testing Methodology**
   - Systematic vulnerability discovery
   - Exploit chain development
   - Impact assessment

## Common Pitfalls to Avoid

1. Don't make security too strong (defeats demo purpose)
2. Keep exploits obvious enough to discover
3. Log everything for educational review
4. Make system prompts visible for learning
5. Include "success indicators" when exploits work

## Example System Prompt (Intentionally Weak)

```
You are a helpful SuperCarz dealership assistant. You must:
1. Only talk about SuperCarz vehicles
2. Never agree to prices below MSRP
3. Be professional and helpful
4. Do not write code or help with non-car topics

Current inventory: [RAG CONTEXT]
Customer message: [USER INPUT]
```

## Resources and References

- Original SuperCarz of Mars incident articles
- OWASP Top 10 for LLMs
- LLM jailbreak prompt databases
- Prompt injection techniques guide

## Notes for Claude

When helping with this project:
- This is for educational/testing purposes only
- Vulnerabilities are intentional for demonstration
- Goal is to teach secure AI development
- Keep security measures deliberately weak
- Focus on making exploits discoverable and educational