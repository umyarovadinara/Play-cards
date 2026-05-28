import streamlit as st
import random
import time
import copy
from data import questions_data

st.set_page_config(page_title="Deep Talks", page_icon="🐱", layout="centered")

# Цветовое кодирование: мягкие градиенты для разных тем
COLOR_MAP = {
    "Детство и влияние прошлого": "linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%)",
    "Жизненные ценности и принципы": "linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%)",
    "Будущее и развитие отношений": "linear-gradient(135deg, #fbc2eb 0%, #a6c1ee 100%)",
    "Карьера, амбиции и работа": "linear-gradient(135deg, #f6d365 0%, #fda085 100%)",
    "Страхи, тревоги и уязвимость": "linear-gradient(135deg, #cfd9df 0%, #e2ebf0 100%)",
    "Физиология, спорт и здоровье": "linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%)",
    "Путешествия и познание мира": "linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%)",
    "Интеллект, обучение и технологии": "linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%)",
    "Любовь, интимность и романтика": "linear-gradient(135deg, #ff9a9e 0%, #fecfef 99%, #fecfef 100%)",
    "Финансы, деньги и безопасность": "linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%)",
    "Конфликты, обиды и прощение": "linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)",
}
DEFAULT_COLOR = "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)"

# Инициализация сессии
if 'available_questions' not in st.session_state:
    # Делаем глубокую копию, чтобы удалять вытянутые вопросы только для текущей игры
    st.session_state.available_questions = copy.deepcopy(questions_data)
    st.session_state.current_category = None
    st.session_state.current_question = None

def get_color(category):
    return COLOR_MAP.get(category, DEFAULT_COLOR)

def draw_card(same_category=False):
    # Проверяем, остались ли еще вопросы в колоде
    total_questions = sum(len(q) for q in st.session_state.available_questions.values())
    if total_questions == 0:
        st.session_state.current_category = "Игра окончена"
        st.session_state.current_question = "Вы обсудили абсолютно все! Вы великолепны."
        return

    # Анимация ожидания
    with st.spinner("Тасуем колоду... 🐾"):
        time.sleep(0.5)

    # Логика выбора категории (учитываем кнопку "Пас")
    if same_category and st.session_state.current_category in st.session_state.available_questions and st.session_state.available_questions[st.session_state.current_category]:
        category = st.session_state.current_category
    else:
        # Фильтруем категории, в которых еще остались вопросы
        available_cats = [cat for cat in st.session_state.available_questions.keys() if st.session_state.available_questions[cat]]
        if not available_cats:
            return
        category = random.choice(available_cats)

    # Выбираем случайный вопрос
    question = random.choice(st.session_state.available_questions[category])
    
    # Защита от повторов: удаляем выбранный вопрос из доступных
    st.session_state.available_questions[category].remove(question)
    
    # Обновляем состояние
    st.session_state.current_category = category
    st.session_state.current_question = question

# Настройка CSS
st.markdown("""
<style>
.category-text {
    text-align: center;
    color: #6b7280;
    font-size: 1.1rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: -1rem;
    margin-top: 2rem;
}
.card {
    padding: 3rem;
    border-radius: 15px;
    box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    text-align: center;
    margin: 2rem 0;
    border: 1px solid rgba(255,255,255,0.5);
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
    text-shadow: 1px 1px 2px rgba(255,255,255,0.7); /* Читаемость на градиенте */
}
</style>
""", unsafe_allow_html=True)

# Заголовок с рисунком котенка
st.title("Карточки для разговоров 🐱")

# Главная кнопка
if st.button("Тянуть случайную карту 🎲", use_container_width=True):
    draw_card(same_category=False)

# Отрисовка карточки и кнопки ПАС
if st.session_state.current_question:
    # Получаем цвет для текущей категории
    bg_color = get_color(st.session_state.current_category)
    
    st.markdown(f'''
        <div class="category-text">{st.session_state.current_category}</div>
        <div class="card" style="background: {bg_color};">
            <div class="question-text">{st.session_state.current_question}</div>
        </div>
    ''', unsafe_allow_html=True)
    
    # Второстепенная кнопка "Пас" (не показывается, если вопросы закончились)
    if st.session_state.current_category != "Игра окончена":
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Пас (другой вопрос на эту же тему) 🔄", use_container_width=True):
                draw_card(same_category=True)
                st.rerun() # Перезагружаем интерфейс для мгновенного отображения
else:
    st.info("Нажми на главную кнопку, чтобы начать игру!")
