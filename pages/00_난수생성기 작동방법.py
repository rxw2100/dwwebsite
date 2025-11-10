import streamlit as st
import random

st.set_page_config(page_title="난수 생성기", page_icon="🎲")

# 페이지 제목
st.title("🎲 난수 생성기 사용 안내 페이지")

# 설명
st.markdown("""
이 페이지는 **난수 생성기**를 사용하여 사용자가 입력한 범위 내에서 무작위로 숫자를 생성하는 기능을 제공합니다.  

### 사용 방법
1. 아래의 **최소값**과 **최대값** 칸에 원하는 숫자를 입력합니다.
2. **난수 생성** 버튼을 클릭하면 범위 안의 난수가 표시됩니다.
3. 여러 번 버튼을 누르면 새로운 난수를 계속 생성할 수 있습니다.

### 주의 사항
- 최소값이 최대값보다 큰 경우에는 오류가 발생하므로 경고 메시지가 표시됩니다.
- 정수만 입력 가능합니다.
""")

# 사용자 입력
min_val = st.number_input("최소값 입력", value=0, step=1)
max_val = st.number_input("최대값 입력", value=10, step=1)

# 최소값 > 최대값 처리
if min_val > max_val:
    st.warning("⚠️ 최소값이 최대값보다 클 수 없습니다.")
else:
    # 난수 생성 버튼
    if st.button("난수 생성"):
        rand_num = random.randint(int(min_val), int(max_val))
        st.success(f"✅ 생성된 난수: {rand_num}")

# 추가 설명
st.markdown("""
---

이 난수 생성기는 예를 들어 **게임에서 랜덤 이벤트 발생**, **시험 문제 랜덤 선택**, **통계 실험** 등 다양한 용도로 활용할 수 있습니다.  
원하는 범위를 입력하고 버튼을 눌러 간편하게 난수를 확인해보세요.
""")
