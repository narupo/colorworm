import curses
from curses import wrapper
import time


# 色セットの定数
COLOR_HEAD = 1
COLOR_BODY = 2


def render_worm(window, y, x, body):
    """
    芋虫を描画する

    @param window cursesのwindow
    """
    global COLOR_HEAD, COLOR_BODY

    for my in range(len(body)):
        for mx in range(len(body[my])):
            c = body[my][mx]
            ch = None
            color = -1
            
            if c == 1:
                ch = '*'
                color = COLOR_HEAD
            elif c == 2:
                ch = '+'
                color = COLOR_BODY
            else:
                continue
            
            window.addstr(y + my, x + mx, ch, curses.color_pair(color))


def main(window):
    global COLOR_HEAD, COLOR_BODY

    # カーソルを非表示
    curses.curs_set(False)

    # 色の初期化
    curses.init_pair(COLOR_HEAD, curses.COLOR_GREEN, curses.COLOR_RED)
    curses.init_pair(COLOR_BODY, curses.COLOR_BLUE, curses.COLOR_GREEN)

    # ノンブロッキングI/Oを有効化
    window.nodelay(True)
    
    # 芋虫の身体
    worm_bodies = [
        [
            [0, 0, 0, 2, 2, 0, 0],
            [0, 0, 2, 2, 2, 2, 0],
            [0, 1, 1, 0, 2, 2, 0],
            [0, 1, 1, 0, 2, 2, 0],
        ],
        [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [1, 1, 2, 2, 2, 2, 2],
            [1, 1, 2, 2, 2, 2, 2],
        ]
    ]

    sleep_time = 1/60 # スレッドを休ませるミリ秒
    frame = 0 # フレーム数
    y, x = 0, 0 # 芋虫の座標
    worm_bodies_index = 0 # 芋虫の身体のインデックス

    while True:
        # input
        ch = window.getch()
        if ch == ord('q'):
            break
        elif ch == ord('w'):
            y -= 1
        elif ch == ord('s'):
            y += 1
        elif ch == ord('a'):
            x -= 1
        elif ch == ord('d'):
            x += 1

        # update
        if frame % 16 == 0:
            worm_bodies_index = (worm_bodies_index + 1) % 2

        body = worm_bodies[worm_bodies_index]
        frame += 1

        # render
        window.clear()
        render_worm(window, y, x, body)
        window.refresh()

        # sleep
        time.sleep(sleep_time)


wrapper(main)
