import streamlit as st
import pandas as pd
import numpy as np

def create_random_dataframe():
    return pd.DataFrame(
        np.random.randn(2, 3), 
        columns=['A', 'B', 'C']
    )

st.title('Task 2: 데이터 표시하기')

st.subheader('데이터프레임')

df = create_random_dataframe()
st.dataframe(df)

st.title("Streamlit 기본 실습")
st.markdown("## Task 1: 기본 UI 컴포넌트")
st.text_input("이름을 입력하세요: ")
st.slider("나이", min_value=0, max_value=100, value = 25)
colors = ["빨강", "파랑","초록","노랑","검정"]
st.selectbox("좋아하는 색",colors, index = 0)
st.checkbox("이용 약관에 동의합니다.")
st.button("제출")

df = pd.read_csv("penguins.csv")
st.header("원본 데이터 전체보기")
st.dataframe(df)

st.header("데이터 요약 정보")
st.write(f"**총 행 (데이터 포인트):** {df.shape[0]}개")
st.write(f"**총 열 (컬럼)** {df.shape[1]}개")

st.subheader("통계량")
st.write(df.describe())

st.subheader("컬럼 목록")
st.write(df.columns.tolist())

st.header("TASK 5")
st.subheader('csv 파일 업로드 ')

uploaded_file = st.file_uploader('CSV 파일 업로드', type=['csv'])

print(uploaded_file)
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.write("업로드 된 CSV 파일의 정보")
    st.dataframe(df)
    
else:
    st.write("CSV 파일을 업로드 하세요.")
