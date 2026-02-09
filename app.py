import streamlit as st
import pandas as pd

# 1. 페이지 설정 및 디자인 커스텀
st.set_page_config(page_title="LH숲속작은도서관", page_icon="📚", layout="centered")

# CSS를 이용한 도서관 스타일 꾸미기
st.markdown("""
    <style>
    /* 전체 배경색과 글꼴 */
    .stApp {
        background-color: #fdfaf5; /* 따뜻한 종이 느낌의 배경색 */
    }
    
    /* 제목 스타일 */
    .main-title {
        font-size: 28px !important;
        color: #2c3e50;
        font-weight: 800;
        text-align: center;
        padding-top: 10px;
        margin-bottom: 0px;
    }
    
    /* 부제목 스타일 */
    .sub-title {
        font-size: 14px !important;
        color: #7f8c8d;
        text-align: center;
        margin-bottom: 30px;
    }
    
    /* 검색창 박스 스타일 */
    .stTextInput > div > div > input {
        border-radius: 20px;
        border: 2px solid #d35400; /* 포인트 컬러: 따뜻한 주황색 */
    }
    </style>
    
    <div class="main-title">🌳 LH숲속작은도서관 📚</div>
    <div class="sub-title">우리 마을의 작은 쉼터, 책 속에서 보물을 찾아보세요.</div>
    """, unsafe_allow_html=True)

# 2. 데이터 로드 (캐싱 처리)
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
    # 검색 영역을 카드로 감싼 듯한 느낌 주기
    with st.container():
        keyword = st.text_input("", placeholder="어떤 책을 찾으시나요? (제목 또는 저자 입력)")

    if keyword:
        # 검색 필터링
        search_cols = ['서명', '저자', '출판사']
        available_cols = [c for c in search_cols if c in df.columns]
        
        mask = df[available_cols].astype(str).apply(lambda x: x.str.contains(keyword, case=False)).any(axis=1)
        result = df[mask]
        
        if len(result) > 0:
            st.success(f"✨ 검색된 도서는 총 {len(result)}권입니다.")
            # 표 디자인: 인덱스 숨기고 깔끔하게
            st.dataframe(result[available_cols], use_container_width=True, hide_index=True)
        else:
            st.warning("🧐 찾는 도서가 없습니다. 다른 검색어를 입력해 보세요.")
    else:
        # 초기 화면 가이드
        st.write("")
        st.info("💡 위 검색창에 책 제목이나 작가 이름을 입력하고 엔터를 눌러주세요.")
        
        # 도서관 추천 문구 같은 장식
        st.markdown("---")
        st.caption("📍 위치: LH사동휴먼시아2단지 203동 1층")
else:
    st.error("❌ 'books.xlsx' 파일을 불러올 수 없습니다. 파일명을 확인해 주세요!")

