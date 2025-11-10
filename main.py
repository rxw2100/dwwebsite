import streamlit as st
import random
import time

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
if 'move' not in st.session_state:
    st.session_state.move = None
if 'shoot' not in st.session_state:
    st.session_state.shoot = False

# HTML + JS로 키보드 입력 받기
st.components.v1.html("""
<script>
document.addEventListener('keydown', function(event) {
    if(event.key === 'ArrowLeft'){
        window.parent.postMessage({func:'move', dir:'left'}, '*');
    } else if(event.key === 'ArrowRight'){
        window.parent.postMessage({func:'move', dir:'right'}, '*');
    } else if(event.key === ' '){
        window.parent.postMessage({func:'shoot'}, '*');
    }
});
</script>
""", height=0)

# Streamlit에서 메시지 처리
def handle_msg(msg):
    if msg["func"] == "move":
        st.session_state.move = msg["dir"]
    elif msg["func"] == "shoot":
        st.session_state.shoot = True

st.experimental_set_query_params()  # 메시지 초기화

# 플레이어 이동
if st.session_state.move == 'left':
    st.session_state.player_x = max(0, st.session_state.player_x - 1)
elif st.session_state.move == 'right':
    st.session_state.player_x = min(WIDTH-1, st.session_state.player_x + 1)
st.session_state.move = None

# 총알 발사
if st.session_state.shoot:
    st.session_state.bullets.append([st.session_state.player_x, HEIGHT-1])
    st.session_state.shoot = False

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
if random.random() < 0.2:
    st.session_state.enemies.append([random.randint(0, WIDTH-1), 0])

# 게임판 출력
board = [['⬛' for _ in range(WIDTH)] for _ in range(HEIGHT)]
for ex, ey in st.session_state.enemies:
    board[ey][ex] = '👾'
for bx, by in st.session_state.bullets:
    board[by][bx] = '🔺'
board[HEIGHT-1][st.session_state.player_x] = '🚀'

st.write("\n".join("".join(row) for row in board))
st.write(f"점수: {st.session_state.score}")

time.sleep(0.2)
st.experimental_rerun()
