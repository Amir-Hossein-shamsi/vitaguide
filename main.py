from typing import Set
from dotenv import load_dotenv
import os
import re
import streamlit as st
from backend.core import run_llm
# Load environment variables FIRST
load_dotenv()


# ===== CRITICAL: INITIALIZE SESSION STATE FIRST =====
if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []
if "chat_answer_history" not in st.session_state:
    st.session_state["chat_answer_history"] = []
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
# ===== CUSTOM CSS STYLING - OPTIMIZED FOR TEXT VISIBILITY =====
st.markdown("""
<style>
:root {
    --primary: #6B8E23;       /* Avocado green */
    --primary-light: #e3f1be; /* Soft green */
    --primary-dark: #3E4E1E;  /* Dark rind-like green */
    --accent: #E6C36F;        /* Avocado seed / toast highlight */
    --light-bg: #e3f1be;      /* Dark background */
    --card-bg: white;       /* Deep olive card */
    --text-dark: black;     /* Light cream text */
    --text-light: #A0A088;    /* Subtle tan */
    --border: #2E2E1E;
    --user-msg-bg: #202B1F;
    --source-bg: #23281B;
}

.stApp {
    background-color: var(--light-bg);
    color: var(--text-dark);
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
}

.header {
    background: linear-gradient(135deg, var(--primary-dark), var(--primary));
    color: white;
    padding: 1.8rem;
    border-radius: 16px;
    margin-bottom: 1.8rem;
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.4);
}

.stChatMessage {
    border-radius: 20px !important;
    padding: 1.4rem !important;
    margin-bottom: 1.2rem !important;
    background-color: var(--card-bg);
    color: var(--text-dark);
    border: 1px solid var(--border);
}

.stChatMessage[data-testid="user"] {
    background-color: var(--user-msg-bg) !important;
    border-left: 4px solid var(--primary-light) !important;
}

.stChatMessage[data-testid="assistant"] {
    background-color: var(--card-bg) !important;
    border-left: 4px solid var(--primary) !important;
}

.stChatInput {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 14px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
}

.stChatInput input {
    background: #262B1E;
    color: var(--text-dark);
    padding: 1.2rem;
    font-size: 1.1rem;
    border: 1px solid var(--border);
    border-radius: 12px;
}

.stChatInput input::placeholder {
    color: var(--text-light);
    opacity: 0.7;
}

.sources-container {
    background: var(--source-bg);
    border-left: 4px solid var(--primary);
    padding: 1.2rem;
    border-radius: 12px;
    margin-top: 1.2rem;
}

footer {
    color: var(--text-light);
}

a {
    color: var(--primary-light);
}

.pro-tips {
    background: #1F2517;
    border-left: 3px solid var(--primary);
    padding: 1rem;
    border-radius: 12px;
}

.pro-tips h4 {
    color: var(--primary-light);
}

[data-testid="stSidebar"] {
    background: #181C13 !important;
    border-right: 1px solid var(--border);
}

hr {
    border-color: var(--border);
}
</style>
""", unsafe_allow_html=True)
# ===== APP CONFIGURATION =====
st.set_page_config(
    page_title="VitaGuide Nutrition Assistant",
    page_icon="🥑",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ===== SIDEBAR =====
with st.sidebar:
    st.markdown("<h2 style='color: var(--primary-dark); margin-top: 1rem;'>🥑 VitaGuide</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--text-light); line-height: 1.6; margin-bottom: 1.5rem;'>Your AI-powered nutrition & wellness companion</p>", unsafe_allow_html=True)
    st.divider()
    st.markdown("### 🌿 Key Features")
    st.markdown("""
    <div class="pro-tips">
        <h4>💡 Smart Nutrition Guidance</h4>
        <p class="text-light">Get personalized advice based on your goals and dietary needs</p>
    </div>
    <div class="pro-tips">
        <h4>📊 Evidence-Based Answers</h4>
        <p class="text-light">All recommendations backed by scientific research</p>
    </div>
    <div class="pro-tips">
        <h4>🍳 Meal Planning Help</h4>
        <p class="text-light">Custom meal suggestions for any diet or restriction</p>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    if st.button("🔄 Start Fresh Chat", use_container_width=True, type="primary"):
        st.session_state["user_prompt_history"] = []
        st.session_state["chat_answer_history"] = []
        st.rerun()
# ===== MAIN CONTENT =====
st.markdown("""
<div class="header">
    <h1>🥑 VitaGuide Nutrition Assistant</h1>
    <p class="tagline">Personalized, science-backed nutrition guidance tailored to your unique health goals. All recommendations are verified against the latest nutritional science research.</p>
</div>
""", unsafe_allow_html=True)
# ===== CHAT HISTORY CONTAINER =====
chat_container = st.container()
# Display chat history
with chat_container:
    st.markdown("""
            <div id="chat-container" style="max-height: 80vh; overflow-y: auto; padding-right: 1rem;">
            """, unsafe_allow_html=True)
    
    if st.session_state["chat_answer_history"]:
        for i, (user_prompt, generated_answer) in enumerate(zip(
            st.session_state["user_prompt_history"], 
            st.session_state["chat_answer_history"]
        )):
            
            with st.chat_message("user", avatar="👤"):
                st.markdown(f"<div style='font-weight: 500; color: var(--text-dark);'>{user_prompt}</div>", unsafe_allow_html=True)
            
            with st.chat_message("assistant", avatar="🥑"):
                
                if "**Answer:**" in generated_answer:
                    try:
                        answer_part = generated_answer.split("**Answer:**")[1]
                        
                        if "sources:" in answer_part:
                            answer, sources = answer_part.split("sources:")
                            st.markdown(f"<div style='line-height: 1.7; color: var(--text-dark);'>{answer.strip()}</div>", unsafe_allow_html=True)

                            # Extract all http/https URLs
                            raw_urls = re.findall(r"https?://[^\s]+", sources)

                            # Clean each URL: remove backslashes and trailing punctuation
                            cleaned_urls = []
                            for url in raw_urls:
                                url = url.replace("\\", "")  
                                url = url.rstrip(".,);")      
                                cleaned_urls.append(url)
                            cleaned_urls = sorted(set(cleaned_urls))
                            # Display cleaned URLs
                            if cleaned_urls:
                                st.markdown('<div class="sources-container"><h4 style="color: var(--primary-light); margin-top: 0;">🔬 Research Sources</h4>', unsafe_allow_html=True)
                                for idx, url in enumerate(cleaned_urls, 1):
                                    st.markdown(
                                        f"<p style='margin: 0.4rem 0; font-size: 0.95rem; color: black;'>"
                                        f"<span style='color: black; font-weight: 600;'>{idx}.</span> "
                                        f"<a href='{url}' target='_blank' style='color: black; text-decoration: none;'>{url}</a></p>",
                                        unsafe_allow_html=True
                                    )
                                st.markdown('</div>', unsafe_allow_html=True)
                    except Exception as e:
                        # Fallback if parsing fails
                        st.markdown(f"<div style='color: var(--text-dark);'>{generated_answer}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='color: var(--text-dark);'>{generated_answer}</div>", unsafe_allow_html=True)
# ===== INPUT SECTION =====
st.markdown("<br>", unsafe_allow_html=True)
# Custom input with better placeholder
prompt = st.chat_input(
    "Ask about nutrition, fitness, or healthy eating... (e.g. 'What are good protein sources for vegetarians?')",
    key="input"
)
# ===== PROCESS USER INPUT =====
if prompt:
    # Add user message immediately
    st.session_state["user_prompt_history"].append(prompt)
    # Show thinking indicator with health-themed animation
    with st.spinner("🌱 Analyzing latest nutrition research..."):
        generated_answer = run_llm(query=prompt,chat_history=st.session_state["chat_history"])
        source = set([doc.metadata["source"] for doc in generated_answer["source_documents"]])
        # Format response with improved structure
        formatted_response = (
            f"**Answer:** {generated_answer['results']}\n"
            f"sources:\n" + "\n".join([f"{i+1}. {s}" for i, s in enumerate(source)])
        )
        st.session_state["chat_answer_history"].append(formatted_response)
        st.session_state["chat_history"].append(("human", prompt))
        st.session_state["chat_history"].append(("ai", generated_answer["results"]))
    # Auto-scroll to new message
    st.rerun()

# ===== smooth scroll to bottom of chat container =====
st.markdown("""
    <script>
        const chatDiv = document.getElementById("chat-container");
        if (chatDiv) {
            setTimeout(() => {
                chatDiv.scrollTo({
                    top: chatDiv.scrollHeight,
                    behavior: "smooth"
                });
            }, 100);
        }
    </script>
    """, unsafe_allow_html=True)

# ===== FOOTER =====
st.markdown("""
<div style="margin-top: 2.5rem; padding-top: 1.5rem; border-top: 1px solid var(--border);">
    <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 1rem; max-width: 1000px; margin: 0 auto;">
        <div style="flex: 1; min-width: 200px;">
            <h4 style="color: var(--primary-dark); margin-bottom: 0.5rem;">🥑 VitaGuide</h4>
            <p style="color: var(--text-light); line-height: 1.6; font-size: 0.95rem;">
                Science-backed nutrition guidance for a healthier you. All recommendations are evidence-based and personalized.
            </p>
        </div>
        <div style="flex: 1; min-width: 150px;">
            <h4 style="color: var(--primary-dark); margin-bottom: 0.7rem;">Quick Links</h4>
            <ul style="list-style: none; padding: 0; margin: 0;">
                <li style="margin-bottom: 0.4rem;"><a href="#" style="color: var(--text-light); text-decoration: none;">Our Methodology</a></li>
                <li style="margin-bottom: 0.4rem;"><a href="#" style="color: var(--text-light); text-decoration: none;">Nutrition Resources</a></li>
                <li style="margin-bottom: 0.4rem;"><a href="#" style="color: var(--text-light); text-decoration: none;">Contact Support</a></li>
            </ul>
        </div>
        <div style="flex: 1; min-width: 150px;">
            <h4 style="color: var(--primary-dark); margin-bottom: 0.7rem;">Legal</h4>
            <ul style="list-style: none; padding: 0; margin: 0;">
                <li style="margin-bottom: 0.4rem;"><a href="#" style="color: var(--text-light); text-decoration: none;">Privacy Policy</a></li>
                <li style="margin-bottom: 0.4rem;"><a href="#" style="color: var(--text-light); text-decoration: none;">Terms of Service</a></li>
                <li style="margin-bottom: 0.4rem;"><a href="#" style="color: var(--text-light); text-decoration: none;">Disclaimer</a></li>
            </ul>
        </div>
    </div>
    <div style="text-align: center; color: var(--text-light); font-size: 0.9rem; margin-top: 1.8rem; padding-top: 1rem; border-top: 1px dashed var(--border);">
        © 2025 VitaGuide Nutrition Assistant • Powered by Evidence-Based Research • Made with 🌱 for your wellness journey
    </div>
</div>
""", unsafe_allow_html=True)