import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="LH숲속작은도서관", page_icon="📚", layout="centered")

# CSS 디자인
st.markdown("""
    <style>
    .stApp { background-color: #fdfaf5; }
    .main-title { font-size: 28px !important; color: #2c3e50; font-weight: 800; text-align: center; padding-top: 10px; }
    .sub-title { font-size: 14px !important; color: #7f8c8d; text-align: center; margin-bottom: 10px; }
    /* 안내 문구 박스 스타일 */
    .notice-box {
        background-color: #fff4e5; 
        border-left: 5px solid #d35400;
        padding: 10px;
        margin-bottom: 20px;
        border-radius: 5px;
        font-size: 13px;
        color: #856404;
    }
    .stTextInput > div > div > input { border-radius: 20px; border: 2px solid #d35400; }
    </style>
    
    <div class="main-title">🌳 LH숲속작은도서관 📚</div>
    <div class="sub-title">우리 마을의 작은 쉼터, 책 속에서 보물을 찾아보세요.</div>
    
    <div class="notice-box">
        ⚠️ <b>안내:</b> 대출 여부는 실시간으로 반영되지 않습니다. <br>
        정확한 도서 상태는 도서관 데스크에 문의해 주세요.
    </div>
    """, unsafe_allow_html=True)

# 2. 데이터 로드
@st.cache_data
def load_data():
    try:
        df = pd.read_excel('books.xlsx')
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception:
        return None

df = load_data()

# 3. 본문 구성
if df is not None:
    keyword = st.text_input("", placeholder="어떤 책을 찾으시나요? (제목 또는 저자 입력)")

    if keyword:
        search_cols = ['서명', '저자', '출판사']
        available_cols = [c for c in search_cols if c in df.columns]
        
        mask = df[available_cols].astype(str).apply(lambda x: x.str.contains(keyword, case=False)).any(axis=1)
        result = df[mask]
        
        if len(result) > 0:
            st.success(f"✨ 검색된 도서는 총 {len(result)}권입니다.")
            st.dataframe(result[available_cols], use_container_width=True, hide_index=True)
        else:
            st.warning("🧐 찾는 도서가 없습니다. 다른 검색어를 입력해 보세요.")
    else:
        st.info("💡 위 검색창에 책 제목이나 작가 이름을 입력하고 엔터를 눌러주세요.")
        st.markdown("---")
        st.caption("📍 위치: LH 6단지 커뮤니티 센터 내 2층")
else:
    st.error("❌ 'books.xlsx' 파일을 불러올 수 없습니다.")
