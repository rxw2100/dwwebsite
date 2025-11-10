import streamlit as st
import time
import random

# 게임 설정
WIDTH = 10
HEIGHT = 10

# 세션 상태 초기화
if 'player_x' not in st.session_state:
    st.session_state.player_x = WIDTH // 2
if 'bullets' not in st.session_state:
    st.session_state.bullets = []
if 'enemies' not in st.session_state:
    st.session_state.enemies = [[random.randint(0, WIDTH-1), 0] for _ in range(5)]
if 'score' not in st.session_state:
    st.session_state.score = 0

# 플레이어 이동
col1, col2, col3 = st.columns([1,2,1])
with col1:
    if st.button("◀"):
        st.session_state.player_x = max(0, st.session_state.player_x - 1)
with col3:
    if st.button("▶"):
        st.session_state.player_x = min(WIDTH-1, st.session_state.player_x + 1)
with col2:
    if st.button("🔥"):
        st.session_state.bullets.append([st.session_state.player_x, HEIGHT-1])

# 적과 총알 업데이트
new_enemies = []
for ex, ey in st.session_state.enemies:
    if ey + 1 < HEIGHT:
        new_enemies.append([ex, ey+1])
st.session_state.enemies = new_enemies

new_bullets = []
for bx, by in st.session_state.bullets:
    hit = False
    for enemy in st.session_state.enemies:
        if enemy[0] == bx and enemy[1] == by:
            st.session_state.enemies.remove(enemy)
            st.session_state.score += 1
            hit = True
            break
    if not hit and by > 0:
        new_bullets.append([bx, by-1])
st.session_state.bullets = new_bullets

# 새로운 적 생성
if random.random() < 0.2:
    st.session_state.enemies.append([random.randint(0, WIDTH-1), 0])

# 화면 출력
board = [['⬛' for _ in range(WIDTH)] for _ in range(HEIGHT)]
for ex, ey in st.session_state.enemies:
    board[ey][ex] = '👾'
for bx, by in st.session_state.bullets:
    board[by][bx] = '🔺'
board[HEIGHT-1][st.session_state.player_x] = '🚀'

st.write("\n".join("".join(row) for row in board))
st.write(f"점수: {st.session_state.score}")

# 자동 새로고침
time.sleep(0.2)
st.experimental_rerun()
