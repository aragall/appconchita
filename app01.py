import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

# 1. Configuración de entorno
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# 2. Configuración de la página Streamlit (DEBE IR PRIMERO)
st.set_page_config(page_title="Content Generator 🤖", page_icon="🤖")

# 3. Inicialización del modelo (LangChain)
if not api_key:
    st.error("⚠️ No se encontró la API Key de Groq. Revisa tu archivo .env")
    st.stop()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7,
    groq_api_key=api_key # Aseguramos que use la key cargada
)

# 4. Función de generación
def llm_generate(prompt_text):
    template = ChatPromptTemplate.from_messages([
        ("system", "You are a digital marketing expert specialized in SEO and persuasive copywriting. Respond always in the language of the user's prompt."),
        ("human", "{prompt}"),
    ])
    
    chain = template | llm | StrOutputParser()
    return chain.invoke({"prompt": prompt_text})

# 5. Interfaz de Usuario
st.title("Content generator 🤖")

topic = st.text_input("Topic:", placeholder="e.g., nutrition, mental health...")
platform = st.selectbox("Platform:", ['Instagram', 'Facebook', 'LinkedIn', 'Blog', 'E-mail'])
tone = st.selectbox("Message tone:", ['Normal', 'Informative', 'Inspiring', 'Urgent', 'Informal'])
length = st.selectbox("Text length:", ['Short', 'Medium', 'Long'])
audience = st.selectbox("Target audience:", ['All', 'Young adults', 'Families', 'Seniors', 'Teenagers'])

col1, col2 = st.columns(2)
with col1:
    cta = st.checkbox("Include CTA")
with col2:
    hashtags = st.checkbox("Return Hashtags")

keywords = st.text_area("Keywords (SEO):", placeholder="Example: wellness, preventive healthcare...")

# 6. Ejecución
if st.button("Generate Content"):
    if not topic:
        st.warning("Please enter a topic.")
    else:
        with st.spinner("Writing your content..."):
            prompt = f"""
            Write an SEO-optimized text on the topic '{topic}'.
            Return only the final text in your response.
            - Platform: {platform}.
            - Tone: {tone}.
            - Target audience: {audience}.
            - Length: {length}.
            - {"Include a clear Call to Action." if cta else "Do not include a Call to Action."}
            - {"Include relevant hashtags." if hashtags else "Do not include hashtags."}
            {"- Keywords: " + keywords if keywords else ""}
            """
            try:
                res = llm_generate(prompt)
                st.subheader("Result:")
                st.markdown(res)
            except Exception as e:
                st.error(f"Error al generar contenido: {e}")
