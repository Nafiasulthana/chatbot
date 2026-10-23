import streamlit as st
import os
from src.pdf_processor import process_pdf
from src.vector_store import VectorStore
from src.llm_chain import create_qa_chain
from src.ui_template import get_landing_page_html
from src.advanced_features import ResumeAnalyzer

st.set_page_config(
    page_title="TalentAI | Resume Screening",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def init_state():
    defaults = {
        "vector_store": None,
        "chain": None,
        "resume_texts": [],
        "chat_history": [],
        "processed": False
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def main():
    init_state()

    # Paths to generated images in the brain folder
    # We will copy the generated images to the workspace to be accessible easily or just point to their absolute paths.
    # The generated images are at:
    # C:\Users\nafia\.gemini\antigravity\brain\db2a3769-c50e-409e-9ca1-ed4b30f2d750\hero_dashboard_ui_1777367591562.png
    # C:\Users\nafia\.gemini\antigravity\brain\db2a3769-c50e-409e-9ca1-ed4b30f2d750\how_it_works_illustration_1777367614673.png
    # Wait, the artifact images path is specific. I will just pass the strings.
    # Since I don't know the exact filenames reliably across sessions if I restart, I'll find them or copy them.
    # Actually, I have their paths from the tool responses!
    
    hero_img_path = r"C:\Users\nafia\.gemini\antigravity\brain\db2a3769-c50e-409e-9ca1-ed4b30f2d750\hero_dashboard_ui_1777367591562.png"
    process_img_path = r"C:\Users\nafia\.gemini\antigravity\brain\db2a3769-c50e-409e-9ca1-ed4b30f2d750\how_it_works_illustration_1777367614673.png"

    # 1. Render Landing Page HTML
    st.markdown(get_landing_page_html(hero_img_path, process_img_path), unsafe_allow_html=True)

    # 2. Render Streamlit App Interface (The Interactive Part)
    st.markdown("<div id='app-section'>", unsafe_allow_html=True)
    
    st.markdown("## 🚀 Try TalentAI Now")
    st.markdown("Upload resumes below to test our AI screening pipeline.")

    selected_model = "Qwen/Qwen2.5-1.5B-Instruct"

    uploaded_files = st.file_uploader(
        "Upload PDF Resumes",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="hidden"
    )

    if uploaded_files:
        if st.button("Process Resumes", use_container_width=True):
            with st.spinner("Processing PDFs..."):
                resumes = []
                for file in uploaded_files:
                    text = process_pdf(file)
                    resumes.append({
                        "filename": file.name,
                        "content": text
                    })
                st.session_state.resume_texts = resumes

            with st.spinner("Setting up AI..."):
                try:
                    vs = VectorStore()
                    vs.add_documents(resumes)
                    chain = create_qa_chain(
                        model_name=selected_model,
                        vector_store=vs
                    )
                    st.session_state.vector_store = vs
                    st.session_state.chain = chain
                    st.session_state.processed = True
                    st.success(f"✅ {len(resumes)} Resumes processed successfully!")
                except Exception as e:
                    st.error(str(e))

    if st.session_state.processed:
        st.divider()
        st.markdown(f"### 🔍 Analyze {len(st.session_state.resume_texts)} Candidates")
        
        mode = st.radio("Select Analysis Mode", ["Standard Q&A", "Job Fit Scoring", "Profile Extraction", "Portfolio UI Generation"], horizontal=True)
        analyzer = ResumeAnalyzer(st.session_state.chain)

        if mode == "Standard Q&A":
            query = st.text_input("Ask a question (e.g., 'Who has experience with React?')")
            if st.button("Ask AI") and query:
                with st.spinner("Thinking..."):
                    try:
                        answer = analyzer.process("qa", query=query)
                        st.session_state.chat_history.append({"q": query, "a": answer})
                    except Exception as e:
                        st.error(str(e))
                        
        elif mode == "Job Fit Scoring":
            job_desc = st.text_area("Paste Job Description")
            if st.button("Calculate Fit Score") and job_desc:
                with st.spinner("Analyzing fit..."):
                    try:
                        answer = analyzer.process("job_fit", job_description=job_desc)
                        st.session_state.chat_history.append({"q": "Job Fit Score Calculation", "a": answer})
                    except Exception as e:
                        st.error(str(e))
                        
        elif mode == "Profile Extraction":
            if st.button("Extract Profiles"):
                with st.spinner("Extracting..."):
                    try:
                        answer = analyzer.process("extract_profile")
                        st.session_state.chat_history.append({"q": "Structured Profile Extraction", "a": answer})
                    except Exception as e:
                        st.error(str(e))
                        
        elif mode == "Portfolio UI Generation":
            if st.button("Generate UI JSON"):
                with st.spinner("Generating Portfolio Data..."):
                    try:
                        answer = analyzer.process("portfolio_ui")
                        st.session_state.chat_history.append({"q": "Portfolio UI Generation (JSON)", "a": answer})
                    except Exception as e:
                        st.error(str(e))

        if st.session_state.chat_history:
            st.markdown("### 💬 Analysis Results")
            for item in reversed(st.session_state.chat_history):
                st.info(f"**Q:** {item['q']}")
                st.success(f"**A:** {item['a']}")
                st.markdown("---")

            if st.button("Clear History"):
                st.session_state.chat_history = []
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()