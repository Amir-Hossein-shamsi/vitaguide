# 🥑 VitaGuide Nutrition Assistant

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![RAG Pipeline](https://img.shields.io/badge/RAG-Powered-purple)](https://arxiv.org/abs/2005.11401)
[![GitHub Repo](https://img.shields.io/badge/GitHub-vitaGuide-blue?logo=github)](https://github.com/Amir-Hossein-shamsi/vitaguide)

> **AI-Powered Nutrition Guidance Backed by Science**
> VitaGuide analyzes **1,367+ nutrition and fitness articles** from FitDay.com to deliver personalized, evidence-based recommendations. Our RAG system transforms unstructured content into structured knowledge for trustworthy nutrition advice.

> ⚠️ *Disclaimer:* This project processes content from [FitDay.com](https://www.fitday.com) under **fair use** for research and educational purposes. No official partnership exists.


## 🌐 Overview: How VitaGuide Works

VitaGuide ingests real-world nutrition and fitness articles from trusted sources and extracts structured insights using an advanced Retrieval-Augmented Generation (RAG) pipeline.

### 📱 Application Interface

Here's how the VitaGuide interface operates:

![VitaGuide Application Interface](assets/Screenshot%202025-08-01%20225723.png)
*Screenshot: User asks a workout question and receives an evidence-based answer with source citation.*

#### 🔑 Key Features:

1. **Intuitive UI** designed for nutrition and fitness queries
2. **Source-attributed responses** with citations from trusted articles
3. **Evidence-based guidance** using verified nutritional data
4. **Personalized advice** based on user goals
5. **Interactive follow-ups** to refine insights

---

## 🧠 Under the Hood: Technology Stack

VitaGuide employs a custom pipeline that transforms unstructured HTML content into usable, nutrition-specific responses.

### 🔍 System Architecture

```mermaid
graph LR
    A[FitDay Content] --> B(HTML Processing Pipeline)
    B --> C[Structured Knowledge Base]
    C --> D[Retrieval-Augmented Generation]
    D --> E[Evidence-Based Recommendations]
    E --> F[User-Friendly Interface]
```

## 📚 FitDay Content Integration

VitaGuide builds its knowledge base by parsing and analyzing a wide range of real nutrition content from FitDay.

### 📊 Content Categories Processed

| Category             | Count     | Content Type                    | Key Features Extracted                            |
| -------------------- | --------- | ------------------------------- | ------------------------------------------------- |
| **Nutrition Guides** | 782       | Diet plans, food breakdowns     | Macronutrients, sustainability, health effects    |
| **Fitness Articles** | 321       | Exercise and recovery methods   | Training effects, metrics, performance            |
| **Expert Insights**  | 144       | Research-backed recommendations | Clinical data, scientific studies, expert reviews |
| **User Experiences** | 120       | Personal case studies           | Goals, challenges, real-world results             |
| **TOTAL**            | **1,367** | **Comprehensive content**       | **6,786 extracted data points**                   |

### 🌱 Sample Articles Processed

Some example articles VitaGuide understands:

* "Have You Heard of the Pegan Diet?"
* "How Much Healthier is Organic Peanut Butter?"


## 🔬 RAG-Powered Knowledge Framework

VitaGuide uses a Retrieval-Augmented Generation (RAG) system based on [this paper](https://python.langchain.com/docs/tutorials/rag/), tailored for nutrition-specific reasoning.

> *“Models with access to explicit, non-parametric memory can overcome factual limitations in traditional LLMs.”*

### ✅ Our Implementation Highlights

* Built on **GPT-4o-mini** (OpenAI-based model adapted for lightweight inference)
* Ingests **domain-specific FitDay content**
* Uses **dual-retrieval strategy**: both document-level and passage-level
* Maintains **provenance tracking** for all facts

### 📊 RAG Pipeline Diagram

```mermaid
graph LR
    A[Raw Web Content] --> B(Content Extraction)
    B --> C[Knowledge Structuring]
    C --> D[Vector Embedding]
    D --> E[Retrieval System]
    E --> F[Retrieved Context]
    F --> G[GPT-4o-mini LLM]
    G --> H[Source-Attributed Output]
```


## 🚀 Getting Started

### ✅ Prerequisites

* Python 3.10+
* Pinecone account (for vector database)
* OpenAI API key
* Access to FitDay content

### ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/Amir-Hossein-shamsi/vitaguide.git
cd vitaguide

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Use venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env to include:
# OPENAI_API_KEY=your_key
# PINECONE_API_KEY=your_key
# OTHER_CONFIG=...
```

### ▶️ Run the App

```bash
streamlit run main.py
```


## 🌱 Why Nutrition-Specific RAG Matters

Generic LLMs often struggle with:

* Rapidly evolving nutrition science
* Fine distinctions between similar diets
* Requirement for citation and accuracy
* Context-specific nutrient recommendations

### 🔎 VitaGuide’s Edge

* **Focused nutrition retrieval**
* **Fact-checked, attributed outputs**
* **Terminology-aware LLM prompts**
* **Continuously updated knowledge base**

---

## 🤝 Contribution & Contact

I welcome suggestions, ideas, and contributions!

* Open an [issue](https://github.com/Amir-Hossein-shamsi/vitaguide/issues)
* Follow or message on [Twitter](https://twitter.com/Amir_ho3einsh)

---

## 📜 License

Distributed under the [MIT License](https://en.wikipedia.org/wiki/MIT_License).

---

> **Transforming nutrition knowledge into personalized guidance**
> VitaGuide combines cutting-edge AI with evidence-based dietary science.

Made with ❤️ and 🌱 for your wellness journey.


