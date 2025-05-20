# app.py
import streamlit as st
from PyPDF2 import PdfReader
import requests

# --- Custom Header (Logo Removed) ---
st.markdown("""
    <div style="text-align: center;">
        <h2 style="color:#ffa726;">🤖 Saurabh's AI Assistant</h2>
        <p style="color: #ccc;">Your personal ChatGPT with PDF, Web Search & Summarizer</p>
    </div>
""", unsafe_allow_html=True)

st.title("AI Assistant: Chat | PDFs | Web Search")

option = st.sidebar.selectbox("Choose feature", ["Chat", "PDF Q&A", "Web Search"])

# Load OpenAI API Key
try:
    openai_api_key = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error("OpenAI API key not found. Please set it in Streamlit secrets.")
    st.stop()

# Chat Mode
if option == "Chat":
    user_input = st.text_input("Ask me anything")
    if user_input:
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": user_input}]
                },
                headers={"Authorization": f"Bearer {openai_api_key}"}
            ).json()
            
            if "choices" in response and response["choices"]:
                st.markdown("### Response:")
                st.write(response["choices"][0]["message"]["content"])
            else:
                st.error("Error: Unexpected response from OpenAI API.")
                st.write(response)
        except Exception as e:
            st.error(f"Error during API call: {str(e)}")

# PDF Q&A
elif option == "PDF Q&A":
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")
    question = st.text_input("Ask a question from PDF")
    if uploaded_file and question:
        try:
            reader = PdfReader(uploaded_file)
            pdf_text = "".join(page.extract_text() for page in reader.pages)
            prompt = f"Answer based on this PDF:\n{pdf_text[:2000]}\n\nQuestion: {question}"
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": prompt}]
                },
                headers={"Authorization": f"Bearer {openai_api_key}"}
            ).json()
            
            if "choices" in response and response["choices"]:
                st.write(response["choices"][0]["message"]["content"])
            else:
                st.error("Error: Unexpected response from OpenAI API.")
                st.write(response)
        except Exception as e:
            st.error(f"Error during PDF processing or API call: {str(e)}")

# Web Search
elif option == "Web Search":
    search_query = st.text_input("Search the web")
    if search_query:
        try:
            duck_url = f"https://api.duckduckgo.com/?q={search_query}&format=json"
            response = requests.get(duck_url)
            response.raise_for_status()
            data = response.json()
            result = data.get("Abstract", "No answer found. Try rephrasing.")
            st.write(result)
        except Exception as e:
            st.error(f"Error during web search: {str(e)}")

# Footer watermark
st.markdown("<p style='text-align: center; opacity: 0.4;'>© Saurabh's AI</p>", unsafe_allow_html=True)