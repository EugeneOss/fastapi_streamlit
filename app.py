import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import mimetypes

st.set_page_config(page_title="Weather Classification", layout="centered")
st.title("🌤️ Классификация погодных условий по фото")
st.page_link("https://bbarft8l8qvurtgdgu9f.containers.yandexcloud.net/docs#/default/classify_image_clf_weather_post/", label="Перейти на FastAPI Weather Classification 🌐")

API_URL = "https://bbarft8l8qvurtgdgu9f.containers.yandexcloud.net/clf_weather"

def send_to_api(image_bytes, filename, content_type):
    files = {"file": (filename, image_bytes, content_type)}  # <-- важен 3-й аргумент!
    r = requests.post(API_URL, files=files, timeout=15)
    r.raise_for_status()
    return r.json()

option = st.radio("Способ загрузки изображения:", ["Загрузить файл", "Указать URL"], horizontal=True)

image = None
class_name = None
class_prob = None

if option == "Загрузить файл":
    uploaded_file = st.file_uploader("Загрузите изображение", type=["jpg", "jpeg", "png", "webp"])
    if uploaded_file:
        img_bytes = uploaded_file.getvalue()
        # берём content-type из файла или угадываем по расширению
        ctype = uploaded_file.type or mimetypes.guess_type(uploaded_file.name)[0] or "image/jpeg"
        resp = send_to_api(img_bytes, uploaded_file.name or "upload.jpg", ctype)
        class_name, class_prob = resp["class_name"], resp["class_prob"]
        image = Image.open(BytesIO(img_bytes)).convert("RGB")

elif option == "Указать URL":
    url = st.text_input("Введите URL изображения:")
    if url:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        img_bytes = r.content
        ctype = r.headers.get("Content-Type", "image/jpeg")  # возьми тип из ответа
        resp = send_to_api(img_bytes, url.split("/")[-1] or "remote.jpg", ctype)
        class_name, class_prob = resp["class_name"], resp["class_prob"]
        image = Image.open(BytesIO(img_bytes)).convert("RGB")

# --- Вывод результата ---

CLASS_NAMES_dict = {
    'dew': 'Роса',
    'fogsmog': 'Туман',
    'frost': 'Изморозь',
    'glaze': 'Гололёд',
    'hail': 'Град',
    'lightning': 'Молния',
    'rain': 'Ливень, потоп',
    'rainbow': 'Радуга',
    'rime': 'Иней',
    'sandstorm': 'Песчаная буря',
    'snow': 'Снегопад'
}

if image is not None:
    st.image(image, caption="Загруженное изображение", use_container_width=True)
if class_name is not None:
    st.text(CLASS_NAMES_dict[class_name])
if class_prob is not None:
    st.text(class_prob)

