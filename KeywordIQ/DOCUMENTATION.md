# 🚀 SEOMaster - Functional Documentation

**SEOMaster** is an AI-powered marketing and SEO intelligence platform designed to analyze websites and search results using advanced NLP and Generative AI. It empowers users to extract top keywords, analyze metadata, identify trends, and generate SEO-optimized suggestions using Groq Llama 3.

---

## 🛠 Features Overview

### 1. **Smart Keyword Search**
*   **Real-time Google Search**: Powered by SerpApi to fetch organic search results.
*   **Automated Scraping**: Extracts text, page titles, and meta tags from top-ranking pages.
*   **NLP Extraction**:
    *   **RAKE Algorithm**: Fast statistical keyword extraction.
    *   **KeyBERT**: AI-driven semantic keyword extraction for deeper context.
*   **Visual Analysis**: Word clouds and frequency charts.

### 2. **AI-Powered Insights (Groq Llama 3)**
*   **Semantic Clustering**: Groups keywords into meaningful themes (e.g., "AI Tools", "Machine Learning").
*   **Long-Tail Suggestions**: Generates 20+ related search terms to target niche queries.
*   **Content Gap Analysis**: Identifies missing opportunities in your content strategy.

### 3. **Interactive Analytics**
*   **Data Visualization**: Bar charts, line graphs, and treemaps for keyword distribution.
*   **Export Options**: Download results as CSV, JSON, or Excel.
*   **Search History**: Tracks previous queries for quick access.

---

## 🏗 Architecture & Tech Stack

SEOMaster combines real-time web scraping with state-of-the-art AI to provide actionable SEO insights.

### Tech Stack
*   **Frontend**: Streamlit (Python-based web app framework)
*   **Backend Logic**: Python 3.10+
*   **Search Engine**: SerpApi (Google Search Results)
*   **GenAI Model**: Groq API (Llama-3-70b-Versatile)
*   **NLP Libraries**: RAKE-NLTK, KeyBERT, NLTK
*   **Data Processing**: Pandas, BeautifulSoup4, Requests
*   **Visualizations**: Matplotlib, Plotly WordCloud

---

## 🚀 Installation & Setup

### Prerequisites
*   Python 3.8 or higher
*   Git installed
*   API Keys for **SerpApi** and **Groq**

### Step-by-Step Guide

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/YourUsername/SEOMaster.git
    cd SEOMaster
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**
    Create a `.env` file in the root directory and add your keys:
    ```env
    SERPAPI_API_KEY=your_serpapi_key_here
    GROQ_API_KEY=your_groq_api_key_here
    ```

5.  **Run the Application**
    ```bash
    streamlit run app.py
    ```

---

*   **Detailed Cards**: For each result, view the URL, snippet, scraped page title, meta keywords, and **extracted keywords**.
*   **Content Preview**: A snippet of the scraped text.

#### 3. Data Export
*   **Download CSV/JSON**: Export the raw data including extracted keywords and metadata.
*   **Save to Session**: Automatically saves results for analysis in the Analytics module.

### 📊 Keyword Analytics Module (`pages/Keyword_Analytics.py`)
Analyze the data collected from your search or upload a past CSV.

#### 1. Data Loading
*   **Upload CSV**: Load a previously exported `keywordiq_results.csv`.
*   **Use Demo Data**: Toggle to explore features with sample data.

#### 2. Visualizations (Tabs)
*   **Overview**:
    *   **Word Cloud**: Visual representation of most frequent terms.
    *   **Bar Charts & Treemaps**: Top keywords by frequency.
*   **Relationships**: Co-occurrence analysis showing which keywords appear together.
*   **Trends**: Distribution of keyword lengths (word count vs character count).
*   **Keyword Gap**: Identifies "emerging" keywords (frequency 2-4) that might be opportunities.

#### 3. AI Insights & Clustering
*   **AI Theme Analysis**: Uses Groq Llama 3 to summarize the main themes of your keyword set.
*   **Semantic Clustering**:
    *   Groups keywords into clusters based on meaning (using `sentence-transformers`).
    *   Visualizes clusters in a 2D scatter plot.
    *   Auto-labels clusters using AI (e.g., "Cluster 1: Machine Learning Algorithms").

#### 4. Keyword Expansion Engine
*   **Input**: Enter a main topic.
*   **Generate**: The AI generates new related keywords.
*   **Compare**: Checks generated keywords against your existing dataset to find **New Opportunities** vs **Existing Coverage**.

---

## 🏗️ Technical Architecture

### Core Modules
*   `app.py`: Main entry point and landing page.
*   `scraper.py`: Handles HTTP requests and HTML parsing using `BeautifulSoup`.
*   `search.py`: Interfaces with `SerpApi` to get Google search results.
*   `nlp_kewords.py`: Contains logic for `RAKE` and `KeyBERT` extraction.
*   `generator.py`: Wrapper for `Groq` API to generate AI text and suggestions.

### Libraries Used
*   **Streamlit**: UI Framework.
*   **Pandas**: Data manipulation.
*   **Plotly/Matplotlib**: Data visualization.
*   **NLTK/Spacy**: Natural Language Processing.
*   **KeyBERT**: Keyword extraction model.
*   **Sentence-Transformers**: Embeddings for clustering.
*   **Scikit-learn**: K-Means clustering and PCA.
