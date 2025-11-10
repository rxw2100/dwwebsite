import streamlit as st
import random

st.title("🎲 난수 생성기")

# 사용자 입력
min_val = st.number_input("최소값 입력", value=0, step=1)
max_val = st.number_input("최대값 입력", value=10, step=1)

# 최소값이 최대값보다 크면 경고
if min_val > max_val:
    st.warning("⚠️ 최소값이 최대값보다 클 수 없습니다.")
else:
    # 난수 생성 버튼
    if st.button("난수 생성"):
        rand_num = random.randint(int(min_val), int(max_val))
        st.success(f"생성된 난수: {rand_num}")
