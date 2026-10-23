import base64
import os
import re

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def get_landing_page_html(hero_img_path, process_img_path):
    hero_b64 = get_base64_of_bin_file(hero_img_path) if os.path.exists(hero_img_path) else ""
    process_b64 = get_base64_of_bin_file(process_img_path) if os.path.exists(process_img_path) else ""

    hero_img_tag = f'<img src="data:image/png;base64,{hero_b64}" alt="Dashboard Preview" />' if hero_b64 else '<div class="placeholder-img">Dashboard Preview</div>'
    process_img_tag = f'<img src="data:image/png;base64,{process_b64}" alt="How it works" />' if process_b64 else '<div class="placeholder-img">Pipeline</div>'

    html = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap');

:root {{
    --primary: #0d9488;
    --primary-dark: #0f766e;
    --primary-light: #ccfbf1;
    --bg: #ffffff;
    --bg-alt: #f8fafc;
    --text-main: #0f172a;
    --text-muted: #475569;
    --border: #e2e8f0;
}}

/* Streamlit layout overrides */
[data-testid="stAppViewBlockContainer"] {{
    max-width: 100% !important;
    padding: 0 !important;
}}
header[data-testid="stHeader"] {{
    background-color: transparent !important;
}}
.stSidebar {{
    display: none !important;
}}

.landing-wrapper {{
    font-family: 'Inter', sans-serif;
    color: var(--text-main);
    background: var(--bg);
    line-height: 1.6;
    width: 100%;
}}

.landing-wrapper h1, .landing-wrapper h2, .landing-wrapper h3 {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: 1rem;
}}

.landing-wrapper p {{
    color: var(--text-muted);
}}

.container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
}}

/* Navbar */
.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem 0;
    position: relative;
    z-index: 100;
}}
.nav-logo {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    color: var(--primary-dark);
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}
.nav-links {{
    display: flex;
    gap: 2rem;
}}
.nav-links a {{
    text-decoration: none;
    color: var(--text-muted);
    font-weight: 500;
    transition: color 0.2s;
}}
.nav-links a:hover {{
    color: var(--primary);
}}
.btn {{
    display: inline-block;
    padding: 0.75rem 1.5rem;
    border-radius: 12px;
    font-weight: 600;
    text-decoration: none;
    transition: all 0.3s ease;
    cursor: pointer;
    border: none;
    font-family: 'Inter', sans-serif;
    font-size: 1rem;
}}
.btn-primary {{
    background: var(--primary);
    color: white !important;
    box-shadow: 0 4px 14px 0 rgba(13, 148, 136, 0.39);
}}
.btn-primary:hover {{
    background: var(--primary-dark);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(13, 148, 136, 0.23);
}}
.btn-secondary {{
    background: var(--bg);
    color: var(--primary) !important;
    border: 2px solid var(--border);
}}
.btn-secondary:hover {{
    border-color: var(--primary);
    background: var(--primary-light);
}}

/* Hero Section */
.hero {{
    padding: 6rem 0 10rem 0;
    background: linear-gradient(135deg, #f0fdfa 0%, #e0f2fe 100%);
    position: relative;
}}
.hero::after {{
    content: '';
    position: absolute;
    bottom: -1px;
    left: 0;
    right: 0;
    height: 120px;
    background: url('data:image/svg+xml;utf8,<svg viewBox="0 0 1440 320" xmlns="http://www.w3.org/2000/svg"><path fill="%23ffffff" fill-opacity="1" d="M0,128L48,144C96,160,192,192,288,197.3C384,203,480,181,576,149.3C672,117,768,75,864,80C960,85,1056,139,1152,149.3C1248,160,1344,128,1392,112L1440,96L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path></svg>') no-repeat bottom;
    background-size: cover;
}}
.hero .container {{
    display: flex;
    align-items: center;
    gap: 4rem;
    position: relative;
    z-index: 10;
}}
.hero-text {{
    flex: 1;
}}
.hero-text h1 {{
    font-size: 3.5rem;
    color: var(--text-main);
    letter-spacing: -0.02em;
}}
.hero-text h1 span {{
    color: var(--primary);
}}
.hero-text p {{
    font-size: 1.125rem;
    margin-bottom: 2.5rem;
    font-weight: 400;
}}
.hero-btns {{
    display: flex;
    gap: 1rem;
}}
.hero-image {{
    flex: 1;
    perspective: 1000px;
}}
.hero-image img {{
    width: 100%;
    border-radius: 24px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    transform: rotateY(-5deg) rotateX(5deg);
    transition: transform 0.5s;
    border: 1px solid rgba(255,255,255,0.4);
}}
.hero-image img:hover {{
    transform: rotateY(0deg) rotateX(0deg);
}}

/* Features */
.features {{
    padding: 5rem 0;
    text-align: center;
    background: var(--bg);
}}
.features h2 {{
    font-size: 2.5rem;
}}
.features-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin-top: 4rem;
}}
.feature-card {{
    padding: 2.5rem 1.5rem;
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 20px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    text-align: left;
}}
.feature-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    border-color: var(--primary-light);
}}
.feature-icon {{
    width: 60px;
    height: 60px;
    background: var(--primary-light);
    color: var(--primary-dark);
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.8rem;
    margin-bottom: 1.5rem;
}}

/* About / How it Works */
.about {{
    padding: 6rem 0;
    background: var(--bg-alt);
}}
.about .container {{
    display: flex;
    align-items: center;
    gap: 5rem;
}}
.about-text {{
    flex: 1;
}}
.about-text h2 {{
    font-size: 2.5rem;
    margin-bottom: 2rem;
}}
.about-image {{
    flex: 1;
}}
.about-image img {{
    width: 100%;
    border-radius: 20px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
}}
.step-item {{
    display: flex;
    gap: 1.25rem;
    margin-bottom: 1.5rem;
}}
.step-icon {{
    width: 36px;
    height: 36px;
    background: var(--primary);
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    flex-shrink: 0;
    font-size: 1.1rem;
}}
.step-content h4 {{
    margin: 0 0 0.25rem 0;
    font-size: 1.1rem;
}}
.step-content p {{
    margin: 0;
    font-size: 0.95rem;
}}

/* Stats */
.stats {{
    padding: 5rem 0;
    background: var(--primary-dark);
    color: white;
    text-align: center;
}}
.stats-grid {{
    display: flex;
    justify-content: space-around;
    flex-wrap: wrap;
    gap: 2rem;
}}
.stat-card h3 {{
    font-size: 3.5rem;
    margin-bottom: 0.5rem;
    color: white;
}}
.stat-card p {{
    color: var(--primary-light);
    font-size: 1.1rem;
    font-weight: 500;
}}

/* Trust */
.trust {{
    padding: 5rem 0;
    text-align: center;
    background: var(--bg);
}}
.trust-logos {{
    display: flex;
    justify-content: center;
    gap: 4rem;
    margin-top: 3rem;
    flex-wrap: wrap;
    align-items: center;
}}
.trust-logos div {{
    font-size: 1.5rem;
    font-weight: 800;
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #94a3b8;
    transition: color 0.3s;
}}
.trust-logos div:hover {{
    color: var(--primary);
}}

/* Footer */
.footer {{
    padding: 3rem 0;
    background: var(--bg-alt);
    border-top: 1px solid var(--border);
    text-align: center;
    color: var(--text-muted);
}}

/* Streamlit App Container Styling */
#app-section {{
    padding: 4rem 2rem;
    max-width: 1000px;
    margin: 0 auto;
    background: white;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    transform: translateY(-20px);
    border: 1px solid var(--border);
    position: relative;
    z-index: 20;
}}
.stFileUploader {{
    border: 2px dashed var(--primary) !important;
    border-radius: 16px !important;
    padding: 2rem !important;
    background-color: var(--bg-alt) !important;
}}
.stButton button {{
    background-color: var(--primary) !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 0.5rem 1.5rem !important;
    font-weight: 600 !important;
    border: none !important;
    transition: all 0.3s ease !important;
}}
.stButton button:hover {{
    background-color: var(--primary-dark) !important;
    transform: translateY(-2px);
}}
.stTextInput input {{
    border-radius: 12px !important;
    border: 1px solid var(--border) !important;
    padding: 0.75rem 1rem !important;
}}
.stTextInput input:focus {{
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 2px var(--primary-light) !important;
}}
.stAlert {{
    border-radius: 12px !important;
}}

/* Mobile responsiveness */
@media (max-width: 768px) {{
    .hero .container, .about .container {{
        flex-direction: column;
        text-align: center;
    }}
    .hero-text h1 {{
        font-size: 2.5rem;
    }}
    .hero-btns {{
        justify-content: center;
    }}
    .nav-links {{
        display: none;
    }}
    .step-item {{
        text-align: left;
    }}
}}
</style>

<div class="landing-wrapper">
    <!-- NAVBAR -->
    <div class="navbar container">
        <div class="nav-logo">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect width="24" height="24" rx="6" fill="#0d9488"/>
                <path d="M7 12L10.5 15.5L18 8" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            TalentAI
        </div>
        <div class="nav-links">
            <a href="#">Home</a>
            <a href="#features">Features</a>
            <a href="#how-it-works">How it Works</a>
        </div>
        <a href="#app-section" class="btn btn-primary" onclick="window.parent.document.getElementById('app-section').scrollIntoView({{behavior: 'smooth'}})">Get Started</a>
    </div>

    <!-- HERO SECTION -->
    <div class="hero">
        <div class="container">
            <div class="hero-text">
                <h1>Next-Gen <br><span>AI Resume Screening</span> System</h1>
                <p>Automate your hiring pipeline. Our advanced AI instantly parses, analyzes, and ranks candidates to help you find the perfect match 10x faster.</p>
                <div class="hero-btns">
                    <a href="#app-section" class="btn btn-primary" onclick="window.parent.document.getElementById('app-section').scrollIntoView({{behavior: 'smooth'}})">Upload Resume</a>
                    <a href="#features" class="btn btn-secondary">Try Demo</a>
                </div>
            </div>
            <div class="hero-image">
                {hero_img_tag}
            </div>
        </div>
    </div>

    <!-- FEATURES -->
    <div class="features container" id="features">
        <h2>Key Features</h2>
        <p>Everything you need to scale your technical hiring.</p>
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon">📄</div>
                <h3>Resume Parsing</h3>
                <p>Extract text perfectly from complex PDFs using our advanced OCR and parsing engine.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🧠</div>
                <h3>AI Candidate Ranking</h3>
                <p>Semantic matching algorithms to identify the best candidates based on contextual search.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <h3>Skill Extraction</h3>
                <p>Automatically identify programming languages, frameworks, and soft skills.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🎯</div>
                <h3>Smart Filtering</h3>
                <p>Ask natural language questions to filter through thousands of candidates instantly.</p>
            </div>
        </div>
    </div>

    <!-- ABOUT / HOW IT WORKS -->
    <div class="about" id="how-it-works">
        <div class="container">
            <div class="about-text">
                <h2>How It Works</h2>
                <div class="step-list">
                    <div class="step-item">
                        <div class="step-icon">1</div>
                        <div class="step-content">
                            <h4>Upload Resumes</h4>
                            <p>Batch upload PDF resumes via our secure portal.</p>
                        </div>
                    </div>
                    <div class="step-item">
                        <div class="step-icon">2</div>
                        <div class="step-content">
                            <h4>Process & Embed</h4>
                            <p>Our pipeline chunks text and generates high-dimensional embeddings.</p>
                        </div>
                    </div>
                    <div class="step-item">
                        <div class="step-icon">3</div>
                        <div class="step-content">
                            <h4>Analyze with AI</h4>
                            <p>Large Language Models interpret the experience and skills.</p>
                        </div>
                    </div>
                    <div class="step-item">
                        <div class="step-icon">4</div>
                        <div class="step-content">
                            <h4>Instant Results</h4>
                            <p>Query your talent pool and get ranked recommendations instantly.</p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="about-image">
                {process_img_tag}
            </div>
        </div>
    </div>

    <!-- STATS -->
    <div class="stats">
        <div class="container stats-grid">
            <div class="stat-card">
                <h3>95%</h3>
                <p>Parsing Accuracy</p>
            </div>
            <div class="stat-card">
                <h3>10x</h3>
                <p>Faster Screening</p>
            </div>
            <div class="stat-card">
                <h3>500+</h3>
                <p>Resumes Processed</p>
            </div>
        </div>
    </div>

    <!-- TRUST -->
    <div class="trust container">
        <h2>Trusted by Innovative Teams</h2>
        <div class="trust-logos">
            <div>ACME Corp</div>
            <div>GlobalTech</div>
            <div>CloudSync</div>
            <div>Nexus Innovations</div>
            <div>Quantum Data</div>
        </div>
    </div>

    <!-- FOOTER -->
    <div class="footer">
        <div class="container">
            <p>&copy; 2026 TalentAI Solutions. All rights reserved. Designed for Modern Teams.</p>
        </div>
    </div>
</div>
"""
    html = re.sub(r'^\s+', '', html, flags=re.MULTILINE)
    return html
