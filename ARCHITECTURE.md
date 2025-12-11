# ���️ Cognitive Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     LumenAI API Gateway                         │
│  • JWT Authentication  • GPT-5 Models  • missingContext         │
│  • Cryptographic Signatures  • Usage Tracking                   │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                       CLI & SDK Layer                           │
│  lumen_cli.py  │  lumen_sdk.py  │  Authentication              │
└──────────────────────────────────┬──────────────────────────────┘
                                   │
        ┌──────────────────────────┼──────────────────────────┐
        │                          │                          │
        ▼                          ▼                          ▼
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│   Schema     │         │  Recursive   │         │ Multi-Agent  │
│  Generation  │         │   Research   │         │ Orchestration│
│              │         │              │         │              │
│ • AI-powered │         │ • Auto-      │         │ • Specialized│
│   schema     │         │   explores   │         │   agents     │
│   creation   │         │   missing    │         │ • Synthesis  │
│ • Validation │         │   context    │         │ • Comparison │
│ • Extraction │         │ • Builds     │         │ • Refinement │
│              │         │   knowledge  │         │              │
│              │         │   trees      │         │              │
└──────┬───────┘         └──────┬───────┘         └──────┬───────┘
       │                        │                        │
       └────────────────────────┼────────────────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   Application Layer   │
                    │                       │
                    │ • Knowledge Graphs    │
                    │ • Research Pipelines  │
                    │ • Data Extraction     │
                    │ • Comparative Analysis│
                    └───────────────────────┘
```

## Core Components

### 1. Schema-Driven Extraction

**Purpose**: Convert unstructured text into structured data

**Flow**:
```
Natural Language Description
         ↓
    AI generates JSON Schema
         ↓
    Schema validates structure
         ↓
    Extract data from text
         ↓
    Structured JSON output
```

**Example**:
```bash
# Generate schema
$ lumen_cli.py generate-schema "person with name and email"

# Use schema
$ lumen_cli.py validate "John, john@example.com" -f person.json
→ {"name": "John", "email": "john@example.com"}
```

### 2. Recursive Research Agent

**Purpose**: Automatically explore knowledge gaps

**Algorithm**:
```python
def research(query, depth=0):
    if depth >= max_depth:
        return result
    
    result = api.query(query)
    missing = result.missingContext
    
    for context_item in missing:
        branch = research(context_item, depth+1)
        result.branches.append(branch)
    
    return result
```

**Key Feature**: The API returns `missingContext` - things it knows it doesn't know. The agent automatically explores these branches.

**Example Output**:
```
Query: "Who won the 2024 Nobel Prize?"
├─ Names of laureates
│  ├─ Official announcement date
│  └─ Prize categories
├─ Affiliations of winners
│  ├─ Institution details
│  └─ Research contributions
└─ Press release information
   ├─ Citation text
   └─ Prize amount
```

### 3. Multi-Agent Collaboration

**Purpose**: Combine different perspectives for comprehensive analysis

**Pattern**:
```
Topic
  ↓
  ├─→ Technical Agent → Technical perspective
  ├─→ Business Agent → Business perspective  
  ├─→ Ethics Agent → Ethical perspective
  ↓
Synthesis Agent → Combined view
```

**Example**:
```python
# Agent 1: Technical
tech_view = agent.query("Technical aspects of quantum computing")

# Agent 2: Business
biz_view = agent.query("Business applications of quantum computing")

# Agent 3: Synthesizer
synthesis = agent.query(f"Synthesize: {tech_view} and {biz_view}")
```

### 4. Iterative Refinement

**Purpose**: Self-aware agents that fill their own knowledge gaps

**Loop**:
```
1. Query → Get response with missingContext
2. Detect gaps in knowledge
3. Generate follow-up queries
4. Refine answer with new context
5. Repeat until complete or max iterations
```

## Advanced Patterns

### Knowledge Graph Builder

Combines recursive research + schema extraction:

```python
entity_schema = {
    "entities": [{"name": str, "type": str, "description": str}],
    "relationships": [{"from": str, "to": str, "type": str}]
}

# Research topic recursively
tree = researcher.research("neural networks")

# Extract entities at each level
graph = extract_with_schema(tree, entity_schema)
```

### Pipeline Orchestration

Chain multiple agents and schemas:

```
Input → [Schema A] → Agent 1 → Extract Topics
                                     ↓
                              For each topic
                                     ↓
                              [Schema B] → Agent 2 → Deep Research
                                                          ↓
                                                    [Schema C] → Agent 3 → Synthesis
                                                                              ↓
                                                                         Final Output
```

### Comparative Analysis

Parallel research + synthesis:

```
Topic A ─→ Research Agent A ─┐
                              ├─→ Comparison Agent → Analysis
Topic B ─→ Research Agent B ─┘
```

## Why This Works

1. **missingContext awareness**: The API explicitly tells you what it doesn't know
2. **Schema flexibility**: Generate schemas on-the-fly for any data structure
3. **Composability**: Chain agents and schemas in unlimited ways
4. **Self-improvement**: Agents can refine their own queries

## Use Cases

- ��� **Research Automation**: Deep dive into topics with automatic gap-filling
- ��� **Data Extraction**: Convert unstructured text to structured databases
- ��� **Knowledge Management**: Build comprehensive knowledge graphs
- ��� **Agent Swarms**: Parallel specialized agents for complex tasks
- ��� **Iterative Refinement**: Self-improving answers through multiple passes

## Performance

- **Free tier**: 50 requests/day, gpt-5-nano only
- **Recursive depth**: Typically 2-3 levels (exponential branches)
- **Response time**: ~1-2 seconds per query
- **Rate limiting**: Built-in delays (configurable)

## Next Steps

1. **Memory Systems**: Add long-term context retention
2. **Agent Swarms**: Parallel exploration of multiple branches
3. **Learning Loop**: Agents that learn from failures
4. **Human-in-the-Loop**: Interactive refinement with user feedback
5. **Cross-API Integration**: Chain with other AI services

---

**This is not just a CLI - it's a cognitive architecture for building truly intelligent agents.**
