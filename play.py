# play.py

import streamlit as st
import random
from data import questions_data  # Импортируем нашу базу вопросов

st.set_page_config(page_title="Deep Talks", page_icon="🍷", layout="centered")

st.markdown("""
<style>
.card {
    padding: 3rem;
    border-radius: 15px;
    box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    background: linear-gradient(135deg, #ffffff, #f0f2f6);
    text-align: center;
    margin: 2rem 0;
    border: 1px solid #e1e4e8;
    transition: transform 0.3s ease;
}
.card:hover {
    transform: translateY(-5px);
}
.question-text {
    font-size: 1.5rem;
    color: #1f2937;
    font-weight: 500;
    line-height: 1.4;
}
</style>
""", unsafe_allow_html=True)

st.title("Карточки для разговоров 🃏")

category = st.selectbox("Выбери тему на этот вечер:", list(questions_data.keys()))

if st.button("Тянуть карту", use_container_width=True):
    selected_question = random.choice(questions_data[category])
    
    st.markdown(f'''
        <div class="card">
            <div class="question-text">{selected_question}</div>
        </div>
    ''', unsafe_allow_html=True)