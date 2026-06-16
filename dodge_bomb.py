import os
import pygame as pg
import random
import sys
import time


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),  # 上矢印キー
    pg.K_DOWN: (0, +5),  # 下矢印キー
    pg.K_LEFT: (-5, 0),  # 左矢印キー
    pg.K_RIGHT: (+5, 0),  # 右矢印キー
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))
def check_bound(rct: pg.Rect) -> tuple[bool, bool]:   # 練習問題03 / 画面内or画面外を判定
    """
    引数：Rect
    戻り値：真偽値タプル（横方向、縦方向）
    """
    x, y = True, True
    if rct.left < 0 or WIDTH < rct.right:
        x =  False
    if rct.top < 0 or HEIGHT < rct.bottom:
        y = False
    return (x, y)

def gameover(screen: pg.Surface) -> None:   # 演習01 / ゲームオーバーを表示
    """
    ゲームオーバーの表示
    """
    bluck = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(bluck, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    bluck.set_alpha(200)
    fonto = pg.font.Font(None, 70)
    text = fonto.render("Game Over", True, (255, 225, 225))
    bluck.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
    kk_img_2 = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    bluck.blit(kk_img_2, (WIDTH//2 - text.get_width()//2 - 60, HEIGHT//2 - text.get_height() + 20//2))
    bluck.blit(kk_img_2, (WIDTH//2 - text.get_width()//2 + 275, HEIGHT//2 - text.get_height() + 20//2))
    screen.blit(bluck, (0, 0))
    pg.display.update()
    time.sleep(5)

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]: # 演習02 / 爆弾の画像と加速のリストを作成
    """
        爆弾の画像と加速
    """ 
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
    bb_accs = [a for a in range(1, 11)]
    return bb_imgs, bb_accs

def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]: # 演習03 / 飛ぶ方向に従ってこうかとん画像を切り替え
    """
        こうかとんの方向転換
    """
    kk_dict = {
        (0, 0): pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9),
        (5, 0): pg.transform.flip(pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9), True, False),
        (5, 5): pg.transform.flip(pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 0.9), True, False),
        (0, 5): pg.transform.flip(pg.transform.rotozoom(pg.image.load("fig/3.png"), 90, 0.9), True, False),
        (-5, 5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 0.9),
        (-5, 0): pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9),
        (-5, -5): pg.transform.rotozoom(pg.image.load("fig/3.png"), -45, 0.9),
        (0, -5): pg.transform.flip(pg.transform.rotozoom(pg.image.load("fig/3.png"), -90, 0.9), True, False),
        (5, -5): pg.transform.flip(pg.transform.rotozoom(pg.image.load("fig/3.png"), -45, 0.9), True, False)
    }
    return kk_dict

def main():
    """
    ゲームのメイン処理
    """
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    # こうかとんの初期化
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    # 爆弾の初期化
    bb_imgs, bb_accs = init_bb_imgs()   # 演習02 / 爆弾の画像と加速のリストを作成

    bb_img = pg.Surface((20, 20))  # 爆弾用の空のSurface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 半径10の赤い円を描画
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()  # 爆弾Rect
    bb_rct.centerx = random.randint(0, WIDTH)  # 横初期座標
    bb_rct.centery = random.randint(0, HEIGHT)  # 縦初期座標
    vx, vy = +5, +5

    kk_dict = get_kk_imgs() # 演習03 / 飛ぶ方向に従ってこうかとん画像を切り替え

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):  # こうかとんRectと爆弾Rectが重なったら
            gameover(screen)
            return
        screen.blit(bg_img, [0, 0]) 
        screen.blit(bg_img, [0, 0]) 
        if check_bound(kk_rct) != (True, True):   # 練習問題03 / 画面外に出たら元に戻す
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
    
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]  # 横方向の移動量
                sum_mv[1] += mv[1]  # 縦方向の移動量
        
        kk_img = kk_dict[tuple(sum_mv)]
            
        kk_rct.move_ip(sum_mv)
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy) 

        avx = vx*bb_accs[tmr//250]  # 演習02 / 爆弾の加速
        avy = vy*bb_accs[tmr//250]
        bb_img = bb_imgs[min(tmr//100, 9)]
        bb_rct.move_ip(avx, avy) 
        bb_rct.width = bb_img.get_rect().width
        bb_rct.height = bb_img.get_rect().height
        bb_img.set_colorkey((0, 0, 0))

        yoko , tate = check_bound(bb_rct)   # 練習問題03 / 爆弾が画面外に出たら跳ね返る
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
