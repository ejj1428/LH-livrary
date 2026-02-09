import streamlit as st
import pandas as pd

st.set_page_config(page_title="LH숲속작은도서관", page_icon="📚")
st.markdown("### 📚 LH숲속작은도서관 도서 검색")

# 파일 읽기 함수
@st.cache_data
def load_data():
    try:
        # 새로 저장한 .xlsx 파일을 읽어옵니다.
        df = pd.read_excel('books.xlsx')
        # 열 이름의 앞뒤 공백을 제거합니다.
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"파일을 찾을 수 없습니다. 이름이 'books.xlsx'인지 확인해 주세요!")
        return None

df = load_data()

if df is not None:
    # 엑셀 열 이름 확인 (사진 기준: 서명, 저자, 출판사)
    search_cols = ['서명', '저자', '출판사']
    # 혹시 엑셀에 위 이름이 없을 경우를 대비해 실제 존재하는 열만 선택
    available_cols = [c for c in search_cols if c in df.columns]

    keyword = st.text_input("🔍 찾으시는 책 제목이나 저자를 입력하세요", placeholder="예: 나의 미래, 무라카미 등")

    if keyword:
        # 선택한 열들에서 검색어 찾기
        mask = df[available_cols].astype(str).apply(lambda x: x.str.contains(keyword, case=False)).any(axis=1)
        result = df[mask]
        
        st.info(f"총 {len(result)}권의 검색 결과가 있습니다.")
        # 필요한 정보만 표로 보여주기
        st.dataframe(result[available_cols], use_container_width=True, hide_index=True)
    else:
        st.write("📖 검색어를 입력하면 도서 목록이 나타납니다.")
