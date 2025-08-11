import streamlit as st
import requests

st.set_page_config(page_title="Text Sentiment", layout="centered")
st.title("📝 Классификация отзыва (позитив/негатив)")
st.page_link("https://bbarft8l8qvurtgdgu9f.containers.yandexcloud.net/docs#/default/clf_text_clf_text_post", label="Перейти на FastAPI Классификации отзывов 🌐")

API_URL_TEXT = "https://bbarft8l8qvurtgdgu9f.containers.yandexcloud.net/docs"  # твой FastAPI

def send_text_to_api(text: str):
    r = requests.post(API_URL_TEXT, json={"text": text}, timeout=15)
    r.raise_for_status()
    return r.json()  # -> {"label": "...", "prob": 0.x}

text = st.text_area("Вставьте текст отзыва:", height=180, placeholder="Например: Очень понравилось обслуживание...")

label = None
prob = None

if st.button("Классифицировать"):
    if text.strip():
        resp = send_text_to_api(text.strip())
        label, prob = resp["label"], resp["prob"]
    else:
        st.warning("Введите текст, пожалуйста.")

# --- Вывод результата ---
if label is not None:
    st.success(label)
if prob is not None:
    st.caption(f"Вероятность: {prob:.4f}")
