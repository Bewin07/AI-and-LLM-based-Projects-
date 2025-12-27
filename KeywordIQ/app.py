import streamlit as st
from datetime import datetime
import time

# --- App Configuration ---
st.set_page_config(
    page_title="SEOMaster - AI Keyword Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS Styling ---
st.markdown("""
<style>
    /* Global Theme & Reset */
    :root {
        --primary-gradient: linear-gradient(135deg, #0F2027 0%, #203A43 50%, #2C5364 100%);
        --accent-gradient: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%);
        --glass-bg: rgba(255, 255, 255, 0.05); /* Darker glass */
        --glass-border: 1px solid rgba(255, 255, 255, 0.1);
        --text-primary: #ffffff;
        --text-secondary: #a0aec0;
        --card-bg: rgba(17, 25, 40, 0.75);
    }

    .stApp {
        background: #0f172a; /* Deep dark blue background */
        background-image: radial-gradient(at 0% 0%, hsla(253,16%,7%,1) 0, transparent 50%), 
                          radial-gradient(at 50% 0%, hsla(225,39%,30%,1) 0, transparent 50%), 
                          radial-gradient(at 100% 0%, hsla(339,49%,30%,1) 0, transparent 50%);
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
    }

    h1, h2, h3, h4, h5, h6 {
        color: white !important;
    }
    
    p, li, span, div {
        color: #e2e8f0;
    }

    /* Hero Section - Modern & Techy */
    .hero-section {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        padding: 4rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 3rem;
        border: var(--glass-border);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%; left: -50%;
        width: 200%; height: 200%;
        background: radial-gradient(circle, rgba(0,198,255,0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
        pointer-events: none;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .hero-title {
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
        background: linear-gradient(to right, #00c6ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(0, 114, 255, 0.3);
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        font-weight: 300;
        color: var(--text-secondary);
        margin-bottom: 2rem;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }

    /* Feature Cards - Dark Glassmorphism */
    .feature-card {
        background: var(--card-bg);
        padding: 2.5rem;
        border-radius: 16px;
        height: 100%;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: var(--glass-border);
        backdrop-filter: blur(16px);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        border-color: #0072ff;
        box-shadow: 0 20px 40px -10px rgba(0,114,255,0.2);
        background: rgba(17, 25, 40, 0.9);
    }

    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1.2rem;
        background: rgba(0, 114, 255, 0.1);
        width: 60px;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 12px;
        border: 1px solid rgba(0, 114, 255, 0.2);
    }
    
    .feature-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.8rem;
    }
    
    .feature-description {
        color: var(--text-secondary);
        line-height: 1.6;
        font-size: 0.95rem;
    }
    
    /* Stats Container */
    .stats-container {
        display: flex;
        justify-content: space-around;
        padding: 2rem;
        background: rgba(0, 0, 0, 0.2);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin: 3rem 0;
        backdrop-filter: blur(5px);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        color: #00c6ff;
        display: block;
        margin-bottom: 0.2rem;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }

    /* Process Steps */
    .process-step {
        background: var(--card-bg);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        border: var(--glass-border);
        transition: transform 0.2s ease;
        display: flex;
        align-items: flex-start;
        gap: 1.5rem;
    }
    
    .process-step:hover {
        transform: translateX(5px);
        border-color: #00c6ff;
    }

    .step-number {
        background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%);
        color: white;
        min-width: 40px;
        height: 40px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 1.1rem;
        box-shadow: 0 4px 10px rgba(0,114,255,0.3);
    }
    
    .process-step strong {
        color: white;
        font-size: 1.1rem;
    }
    
    .process-step span {
        color: var(--text-secondary) !important;
    }

    /* Tech Badges */
    .tech-badge {
        display: inline-block;
        background: rgba(255,255,255,0.05);
        color: #e2e8f0;
        padding: 0.6rem 1.2rem;
        border-radius: 50px;
        margin: 0.4rem;
        font-weight: 600;
        font-size: 0.9rem;
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.2s;
    }
    
    .tech-badge:hover {
        border-color: #00c6ff;
        color: #00c6ff;
        background: rgba(0, 198, 255, 0.1);
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 4rem 2rem;
        background: rgba(0,0,0,0.2);
        color: var(--text-secondary);
        border-radius: 20px 20px 0 0;
        margin-top: 5rem;
        border-top: 1px solid rgba(255,255,255,0.05);
    }
    
    .footer h3 {
        color: white;
        margin-bottom: 1rem;
    }
    
    .cta-box {
        background: linear-gradient(135deg, rgba(0, 198, 255, 0.1) 0%, rgba(0, 114, 255, 0.1) 100%);
        border-radius: 20px;
        padding: 3rem;
        text-align: center;
        color: white;
        margin-top: 3rem;
        border: 1px solid rgba(0, 114, 255, 0.3);
        box-shadow: 0 0 40px rgba(0, 114, 255, 0.1);
    }

</style>
""", unsafe_allow_html=True)

# --- Initialize Session State ---
if "page_views" not in st.session_state:
    st.session_state.page_views = 1
else:
    st.session_state.page_views += 1

if "last_visit" not in st.session_state:
    st.session_state.last_visit = datetime.now()

# --- Hero Section ---
st.markdown("""
<div class="hero-section">
    <div class="hero-title">🚀 SEOMaster</div>
    <div class="hero-subtitle">Next-Gen AI Keyword Intelligence Platform</div>
    <p style="margin-top: 1.5rem; font-size: 1.1rem; opacity: 0.8;">
        Dominate the SERPs with intelligent, data-driven keyword research powered by advanced AI and real-time scraping.
    </p>
</div>
""", unsafe_allow_html=True)

# --- Quick Stats ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-item">
        <span class="stat-number">10K+</span>
        <span class="stat-label">Keywords Analyzed</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-item">
        <span class="stat-number">500+</span>
        <span class="stat-label">Sites Scraped</span>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-item">
        <span class="stat-number">98%</span>
        <span class="stat-label">Accuracy Rate</span>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-item">
        <span class="stat-number">⚡</span>
        <span class="stat-label">Real-time Analysis</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Feature Cards ---
st.markdown("## ✨ Core Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔍</div>
        <div class="feature-title">Smart Search</div>
        <div class="feature-description">
            • Google-powered search results<br>
            • Real-time web scraping<br>
            • Metadata extraction<br>
            • Content analysis<br>
            • Customizable result count
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🧠</div>
        <div class="feature-title">AI Extraction</div>
        <div class="feature-description">
            • RAKE algorithm support<br>
            • KeyBERT neural extraction<br>
            • Groq Llama 3 integration<br>
            • Context-aware keywords<br>
            • Semantic clustering
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Analytics Dashboard</div>
        <div class="feature-description">
            • Keyword trend visualization<br>
            • Frequency analysis<br>
            • Export to CSV/JSON<br>
            • Interactive charts<br>
            • Performance metrics
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- How It Works Section ---
st.markdown("## 🎯 How SEOMaster Works")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="process-step">
        <span class="step-number">1</span>
        <div>
            <strong>Enter Search Topic</strong><br>
            <span style="color: #718096; font-size: 0.9rem;">Start by entering your target keyword or topic (e.g., "AI tools 2025")</span>
        </div>
    </div>
    
    <div class="process-step">
        <span class="step-number">2</span>
        <div>
            <strong>Fetch Google Results</strong><br>
            <span style="color: #718096; font-size: 0.9rem;">Our system queries Google via SerpApi for top-ranking pages</span>
        </div>
    </div>
    
    <div class="process-step">
        <span class="step-number">3</span>
        <div>
            <strong>Intelligent Scraping</strong><br>
            <span style="color: #718096; font-size: 0.9rem;">We extract titles, meta tags, and full text content instantly</span>
        </div>
    </div>
    
    <div class="process-step">
        <span class="step-number">4</span>
        <div>
            <strong>NLP Analysis</strong><br>
            <span style="color: #718096; font-size: 0.9rem;">Advanced algorithms (RAKE/KeyBERT) extract high-value keywords</span>
        </div>
    </div>
    
    <div class="process-step">
        <span class="step-number">5</span>
        <strong>AI Enhancement</strong><br>
        Groq's Llama 3 suggests related keywords, analyzes themes, and generates insights
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103845.png", width=250)
    
    st.markdown("""
    <div style="background: #f0f9ff; padding: 1.5rem; border-radius: 10px; margin-top: 1rem;">
        <h4 style="color: #0369a1; margin-top: 0;">💡 Pro Tip</h4>
        <p style="margin-bottom: 0; color: #0c4a6e;">
            Use specific, long-tail keywords for better results. 
            The more focused your search, the more actionable insights you'll get!
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Technology Stack ---
st.markdown("## 🛠️ Built With Cutting-Edge Technology")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **Frontend & Framework**
    <div style="margin-top: 0.5rem;">
        <span class="tech-badge">Streamlit</span>
        <span class="tech-badge">Python 3.10+</span>
        <span class="tech-badge">Custom CSS</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    **AI & NLP**
    <div style="margin-top: 0.5rem;">
        <span class="tech-badge">Groq Llama 3</span>
        <span class="tech-badge">KeyBERT</span>
        <span class="tech-badge">RAKE</span>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    **APIs & Services**
    <div style="margin-top: 0.5rem;">
        <span class="tech-badge">SerpApi</span>
        <span class="tech-badge">BeautifulSoup</span>
        <span class="tech-badge">Pandas</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Use Cases ---
st.markdown("## 🎪 Perfect For")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    **👨‍💼 SEO Professionals**
    
    Discover high-value keywords and analyze competitor strategies
    """)

with col2:
    st.markdown("""
    **✍️ Content Creators**
    
    Find trending topics and optimize your content strategy
    """)

with col3:
    st.markdown("""
    **📈 Digital Marketers**
    
    Research market trends and identify content gaps
    """)

with col4:
    st.markdown("""
    **🔬 Researchers**
    
    Analyze web content and extract key insights efficiently
    """)

st.markdown("<br>", unsafe_allow_html=True)

# --- CTA Section ---
st.markdown("## 🚀 Ready to Get Started?")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    <div class="cta-box">
        <h2 style="margin-top: 0; font-weight: 800;">Start Your Research Now</h2>
        <p style="font-size: 1.2rem; margin-bottom: 2rem; opacity: 0.9;">
            Unlock the power of AI-driven SEO analysis today.
        </p>
        <p style="background: rgba(255,255,255,0.2); display: inline-block; padding: 0.5rem 1rem; border-radius: 50px;">
            Navigate to <strong>🔍 Keyword Search</strong> in the sidebar
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Quick Tips ---
with st.expander("💡 Quick Tips for Better Results", expanded=False):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Search Optimization:**
        - Use specific, descriptive keywords
        - Try different keyword combinations
        - Include year for time-sensitive topics
        - Use industry-specific terminology
        """)
    
    with col2:
        st.markdown("""
        **Analysis Best Practices:**
        - Start with 5-10 results for speed
        - Enable parallel processing for faster scraping
        - Use KeyBERT for context-aware extraction
        - Export data regularly for comparison
        """)

# --- Recent Activity (if applicable) ---
if st.session_state.page_views > 1:
    st.markdown("## 📊 Your Session Stats")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Page Views", st.session_state.page_views)
    
    with col2:
        time_diff = datetime.now() - st.session_state.last_visit
        st.metric("Last Visit", f"{time_diff.seconds}s ago")
    
    with col3:
        st.metric("Status", "🟢 Active")

# --- FAQ Section ---
with st.expander("❓ Frequently Asked Questions", expanded=False):
    st.markdown("""
    **Q: How many search results can I analyze at once?**  
    A: You can analyze 1-20 results per search. We recommend starting with 5-10 for optimal speed.
    
    **Q: What's the difference between RAKE and KeyBERT?**  
    A: RAKE is faster and rule-based, while KeyBERT uses neural networks for context-aware extraction.
    
    **Q: Can I export my data?**  
    A: Yes! Export to CSV or JSON format with timestamps for easy tracking.
    
    **Q: Is my data private?**  
    A: All analysis happens in your session and is not stored permanently on our servers.
    
    **Q: What APIs do I need?**  
    A: You'll need a SerpApi key for Google search and optionally a Groq API key for AI features.
    """)

# --- Footer ---
st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    <h3 style="margin-top: 0;">🚀 SEOMaster</h3>
    <p style="margin: 1rem 0;">
        Empowering digital marketers with next-gen AI keyword intelligence
    </p>
    <p style="font-size: 0.9rem; opacity: 0.6; margin-bottom: 2rem;">
        Built with Premium Tech • Streamlit • SerpApi • Groq Llama 3
    </p>
    <div style="border-top: 1px solid #2d3748; padding-top: 2rem; margin-top: 2rem;">
        <p style="font-size: 0.85rem; margin: 0; color: #718096;">
            © 2025 SEOMaster. All rights reserved. 
        </p>
    </div>
</div>
""", unsafe_allow_html=True)