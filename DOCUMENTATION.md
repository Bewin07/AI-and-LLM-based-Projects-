# 🧠 KeywordIQ Studio - Functional Documentation

**KeywordIQ Studio** is an AI-powered marketing and SEO intelligence platform designed to analyze websites and search results using advanced NLP and Generative AI. It empowers users to extract top keywords, analyze metadata, identify trends, and generate SEO-optimized suggestions using Groq Llama 3.

---

## 📋 Table of Contents

1.  [Project Overview](#project-overview)
2.  [Installation & Setup](#installation--setup)
3.  [Functional Guide](#functional-guide)
    *   [Home Dashboard](#home-dashboard)
    *   [Keyword Search Module](#keyword-search-module)
    *   [Keyword Analytics Module](#keyword-analytics-module)
4.  [Technical Architecture](#technical-architecture)

---

## 🚀 Project Overview

KeywordIQ Studio combines real-time web scraping with state-of-the-art AI to provide actionable SEO insights.

### Key Features
*   **Smart Search**: Fetches real-time Google search results via SerpApi.
*   **Intelligent Scraping**: Extracts content, metadata, and headers from top-ranking pages.
*   **AI Extraction**: Utilizes **RAKE** (Rapid Automatic Keyword Extraction) and **KeyBERT** (Neural Network) for precise keyword identification.
*   **Generative Insights**: Integrates **Groq Llama 3** to generate long-tail keyword suggestions and thematic summaries.
*   **Visual Analytics**: Offers interactive dashboards with word clouds, treemaps, and frequency charts.
*   **Semantic Clustering**: Groups keywords by meaning using embeddings and K-Means clustering.

---

## 🛠️ Installation & Setup

### Prerequisites
*   **Python 3.10+**
*   API Keys for:
    *   **SerpApi** (for Google Search results)
    *   **Groq Cloud** (for Llama 3 AI features)

### Step-by-Step Guide

1.  **Clone the Repository**
    ```bash
    git clone <repository-url>
    cd KeywordIQ
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Environment Configuration**
    Create a `.env` file in the root directory and add your API keys:
    ```env
    GROQ_API_KEY=your_groq_api_key_here
    # Note: SerpApi key is currently hardcoded in search.py, but best practice is to move it here.
    ```

4.  **Run the Application**
    ```bash
    streamlit run app.py
    ```

---

## 📖 Functional Guide

### 🏠 Home Dashboard (`app.py`)
The landing page provides a high-level overview of the platform.
*   **Quick Stats**: Displays total keywords analyzed, sites scraped, and accuracy metrics.
*   **Feature Highlights**: Brief descriptions of Smart Search, AI Extraction, and Analytics.
*   **How It Works**: A visual step-by-step guide to the KeywordIQ process.

### 🔍 Keyword Search Module (`pages/Keyword_Search.py`)
This is the core data collection engine.

#### 1. Configuration Sidebar
*   **Search Keyword**: Enter your target topic (e.g., "SaaS marketing trends").
*   **Number of Results**: Slider to choose how many Google results to scrape (1-20).
*   **Extraction Method**:
    *   **RAKE**: Faster, statistical method. Good for large texts.
    *   **KeyBERT**: Slower, context-aware AI method. Better for precise semantic extraction.
*   **Advanced Options**: Enable parallel processing for speed, or site previews.

#### 2. Results View
After running a search, you see:
*   **Metrics**: Success rate, processing time, and total results.
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
