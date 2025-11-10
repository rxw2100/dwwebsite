import streamlit as st
import random

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

st.title("🎮 턴제 갤라그 게임")

# 키 입력 선택 (턴제 방식)
move = st.radio("플레이어 이동/행동 선택:", ["← 왼쪽", "→ 오른쪽", "발사", "그대로"])

# 플레이어 이동 및 발사 처리
if move == "← 왼쪽":
    st.session_state.player_x = max(0, st.session_state.player_x - 1)
elif move == "→ 오른쪽":
    st.session_state.player_x = min(WIDTH-1, st.session_state.player_x + 1)
elif move == "발사":
    st.session_state.bullets.append([st.session_state.player_x, HEIGHT-1])

# 적 이동
new_enemies = []
for ex, ey in st.session_state.enemies:
    if ey + 1 < HEIGHT:
        new_enemies.append([ex, ey+1])
st.session_state.enemies = new_enemies

# 총알 이동 및 충돌
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
if random.random() < 0.3:
    st.session_state.enemies.append([random.randint(0, WIDTH-1), 0])

# 게임판 출력
board = [['⬛' for _ in range(WIDTH)] for _ in range(HEIGHT)]
for ex, ey in st.session_state.enemies:
    board[ey][ex] = '👾'
for bx, by in st.session_state.bullets:
    board[by][bx] = '🔺'
board[HEIGHT-1][st.session_state.player_x] = '🚀'

st.text("\n".join("".join(row) for row in board))
st.text(f"점수: {st.session_state.score}")
