import streamlit as st
from PIL import Image
import easyocr
import io
import numpy as np
from typing import Dict, Any, Optional

@st.cache_resource
def load_ocr_reader() -> easyocr.Reader:
    """Load EasyOCR model for Russian and English text recognition."""
    return easyocr.Reader(['ru', 'en'], gpu=False)

def extract_text_from_image(image_file) -> Dict[str, Any]:
    """Extract text from image using EasyOCR."""
    try:
        if image_file is None:
            return {'text': '', 'confidence': 0, 'image': None, 'error': 'File not loaded'}
        
        image = Image.open(image_file)
        if image.mode not in ('RGB', 'RGBA', 'L'):
            image = image.convert('RGB')
        
        image_array = np.array(image)
        if image_array.size == 0:
            return {'text': '', 'confidence': 0, 'image': None, 'error': 'Image is empty or corrupted'}
        
        reader = load_ocr_reader()
        results = reader.readtext(image_array)
        
        if not results:
            return {'text': 'Text not found', 'confidence': 0, 'image': image, 'error': None}
        
        extracted_text = '\n'.join([str(text[1]) for text in results if len(text) > 1])
        confidence_scores = [float(text[2]) for text in results if len(text) > 2]
        avg_confidence = np.mean(confidence_scores) if confidence_scores else 0.0
        
        return {'text': extracted_text, 'confidence': float(avg_confidence), 'image': image, 'error': None}
    except Exception as e:
        return {'text': '', 'confidence': 0, 'image': None, 'error': f'Error: {str(e)}'}

def add_ocr_section_to_streamlit(sidebar: bool = False) -> Optional[Dict[str, Any]]:
    """Add OCR section to Streamlit app."""
    location = st.sidebar if sidebar else st
    
    with location.expander("📋 OCR: Распознавание текста из документов", expanded=False):
        st.markdown("### Загрузите изображение")
        uploaded_file = st.file_uploader(
            "Выберите изображение (PNG, JPG, JPEG)",
            type=['png', 'jpg', 'jpeg'],
            key='ocr_uploader'
        )
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            col1, col2 = st.columns(2)
            
            with col1:
                st.image(image, caption="Загруженное изображение", use_column_width=True)
            
            with st.spinner('🔄 Распознаю текст...'):
                result = extract_text_from_image(uploaded_file)
            
            if result.get('error'):
                st.error(f"❌ Ошибка: {result['error']}")
                return None
            else:
                with col2:
                    st.markdown("#### ✅ Результаты")
                    confidence = result['confidence'] * 100
                    st.metric("Уверенность", f"{confidence:.1f}%")
                
                st.markdown("#### 📋 Выписанный текст:")
                extracted_text = result['text']
                st.text_area(
                    "Текст:",
                    value=extracted_text,
                    height=200,
                    key='ocr_text'
                )
                
                if st.button("📝 Копировать"):
                    st.code(extracted_text)
                    st.success("✅ Готово!")
                
                return {'text': extracted_text, 'confidence': result['confidence'], 'image': result['image']}
        
        return None
