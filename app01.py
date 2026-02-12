import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Configuración de la página (Siempre al principio)
st.set_page_config(page_title="Content Generator 🤖", page_icon="🤖")

# 2. Sidebar para la API Key
st.sidebar.title("Configuración")
user_api_key = st.sidebar.text_input(
    "Introduce tu Groq API Key:", 
    type="password", 
    placeholder="gsk_..."
)

st.sidebar.markdown("""
---
[¿No tienes una clave? Consíguela aquí](https://console.groq.com/keys)
""")

# 3. Función para inicializar el modelo solo si hay API Key
def get_llm(api_key):
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        groq_api_key=api_key
    )

# 4. Función de generación
def llm_generate(llm_instance, prompt_text):
    template = ChatPromptTemplate.from_messages([
        ("system", "You are a digital marketing expert specialized in SEO and persuasive copywriting."),
        ("human", "{prompt}"),
    ])
    chain = template | llm_instance | StrOutputParser()
    return chain.invoke({"prompt": prompt_text})

# --- INTERFAZ PRINCIPAL ---
st.title("Content generator 🤖")

# Verificamos si el usuario ha puesto la clave
if not user_api_key:
    st.info("👈 Por favor, introduce tu API Key de Groq en el menú de la izquierda para comenzar.")
else:
    # Si hay clave, mostramos el formulario
    topic = st.text_input("Topic:", placeholder="e.g., nutrition, mental health...")
    
    col1, col2 = st.columns(2)
    with col1:
        platform = st.selectbox("Platform:", ['Instagram', 'Facebook', 'LinkedIn', 'Blog', 'E-mail'])
        tone = st.selectbox("Message tone:", ['Normal', 'Informative', 'Inspiring', 'Urgent', 'Informal'])
    with col2:
        length = st.selectbox("Text length:", ['Short', 'Medium', 'Long'])
        audience = st.selectbox("Target audience:", ['All', 'Young adults', 'Families', 'Seniors', 'Teenagers'])

    cta = st.checkbox("Include CTA")
    hashtags = st.checkbox("Return Hashtags")
    keywords = st.text_area("Keywords (SEO):", placeholder="Example: wellness, preventive healthcare...")

    if st.button("Generate Content"):
        if not topic:
            st.warning("Please enter a topic.")
        else:
            with st.spinner("Writing your content..."):
                try:
                    # Inicializamos el LLM con la clave del usuario
                    llm = get_llm(user_api_key)
                    
                    prompt = f"""
                    Write an SEO-optimized text on the topic '{topic}'.
                    - Platform: {platform}.
                    - Tone: {tone}.
                    - Target audience: {audience}.
                    - Length: {length}.
                    - {"Include a clear Call to Action." if cta else "Do not include a Call to Action."}
                    - {"Include relevant hashtags." if hashtags else "Do not include hashtags."}
                    {"- Keywords: " + keywords if keywords else ""}
                    """
                    
                    res = llm_generate(llm, prompt)
                    st.subheader("Result:")
                    st.markdown(res)
                    
                except Exception as e:
                    st.error("Error: La API Key parece inválida o hay un problema de conexión.")
                    st.exception(e) # Esto ayuda a ver el error real si falla