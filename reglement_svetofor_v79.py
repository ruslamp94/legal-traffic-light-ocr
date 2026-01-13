import streamlit as st

st.set_page_config(
    page_title="Legal Traffic Light - OCR",
    page_icon="⚠",
    layout="wide"
)

st.title("⚠ Legal Traffic Light - анализ юридических документов с OCR")

st.markdown("""
Приложение для распознавания текста из изображений документов.
""")

try:
    from ocr_module import add_ocr_section_to_streamlit
    ocr_result = add_ocr_section_to_streamlit(sidebar=False)
    
    if ocr_result:
        st.success("✅ Текст распознан успешно!")
        st.info(f"**Уровень уверенности:** {ocr_result['confidence']*100:.1f}%")
    else:
        st.info("📁 Загрузите изображение для начала")
except Exception as e:
    st.error(f"❌ Ошибка: {str(e)}")
    st.info("**Подсказка:** Приложение оснащают OCR. Попытайтесь если проблема продолжается.")
