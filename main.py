import streamlit as st
import pandas as pd
import numpy as np

def create_random_dataframe():
    return pd.DataFrame(
        np.random.randn(2, 3), 
        columns=['A', 'B', 'C']
    )


st.title("Streamlit 기본 실습")
st.markdown("## Task 1: 기본 UI 컴포넌트")
st.text_input("이름을 입력하세요: ")
st.slider("나이", min_value=0, max_value=100, value = 25)
colors = ["빨강", "파랑","초록","노랑","검정"]
st.selectbox("좋아하는 색",colors, index = 0)
st.checkbox("이용 약관에 동의합니다.")
st.button("제출")

st.title('Task 2: 데이터 표시하기')

st.subheader('데이터프레임')

df = create_random_dataframe()
st.dataframe(df)

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


#task 4 : 인터렉티브 필터링
st.header("TASK 4: 인터랙티브 필터링")

categorical_columns = df.select_dtypes(include=['object']).columns.tolist()

selected_col = st.selectbox(
    "개수를 확인할 카테고리(컬럼)를 선택하세요:",
    options=categorical_columns
)
count_df = (
    df[selected_col]
    .value_counts(dropna=False)
    .reset_index()
)
count_df.columns = [selected_col, "count"]

st.subheader(f"'{selected_col}' 카테고리별 개수")
st.dataframe(count_df)

#task 6 : UI 레이아웃 구성
st.header("TASK 6: UI 레이아웃 구성")
st.header("데이터 요약 정보")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("행 개수", df.shape[0])
with col2:
    st.metric("열 개수", df.shape[1])
with col3:
    st.metric("결측치 개수", df.isna().sum().sum())
    
st.header("데이터 상세 보기")

tab1, tab2, tab3 = st.tabs(["원본 데이터", "통계량", "컬럼 목록"])
with tab1:
    st.dataframe(df)
with tab2:
    st.write(df.describe())
with tab3:
    st.write(df.columns.tolist())

with st.expander("컬럼별 결측치 보기"):
    na_df = df.isna().sum().reset_index()
    na_df.columns = ["column", "missing_count"]
    st.dataframe(na_df)

#task 7 : 종합 대시보드
st.header("TASK 7: 종합 대시보드")

required_cols = {"species", "island"}
if not required_cols.issubset(df.columns):
    st.info("이 대시보드는 palmer penguins 데이터셋(species, island 컬럼)을 기준으로 만들어졌어요.")
else:
    st.sidebar.header("🔧 대시보드 필터")

    species_list = ["전체"] + sorted(df["species"].dropna().unique().tolist())
    selected_species = st.sidebar.selectbox("Species 선택", species_list)

    island_list = ["전체"] + sorted(df["island"].dropna().unique().tolist())
    selected_island = st.sidebar.selectbox("Island 선택", island_list)

    filtered_df = df.copy()
    if selected_species != "전체":
        filtered_df = filtered_df[filtered_df["species"] == selected_species]
    if selected_island != "전체":
        filtered_df = filtered_df[filtered_df["island"] == selected_island]

    st.subheader("🎯 필터 적용 결과")
    st.write(f"현재 선택된 조건에 해당하는 행: **{len(filtered_df)}개**")
    st.dataframe(filtered_df.head())

    tab_summary, tab_raw = st.tabs(["요약", "원본 데이터"])

    with tab_summary:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("총 개체 수", len(filtered_df))
        if "body_mass_g" in filtered_df.columns:
            with col2:
                st.metric(
                    "평균 체중 (g)",
                    f"{filtered_df['body_mass_g'].mean():.1f}"
                )
        if "flipper_length_mm" in filtered_df.columns:
            with col3:
                st.metric(
                    "평균 지느러미 길이 (mm)",
                    f"{filtered_df['flipper_length_mm'].mean():.1f}"
                )
        st.markdown("### 🐧 species별 개수")
        if "species" in filtered_df.columns:
            count_df = (
                filtered_df["species"]
                .value_counts(dropna=False)
                .reset_index()
            )
            count_df.columns = ["species", "count"]
            st.dataframe(count_df)

    with tab_raw:
        with st.expander("📂 필터가 적용된 전체 데이터 보기", expanded=True):
            st.dataframe(filtered_df)