import sys
from random import randint
import time
import pygame as pg

WIDTH, HEIGHT = 1600, 900

delta = { # 練習3 : 移動量の設定 
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0)
}


def check_bound(rct):# 練習4 : はみ出さないように修正
    """
    オブジェクトが画面外を判定し、真理値タプルを返す関数
    引数 rct:こうかとんor爆弾SurfaceのRect
    戻り値:横方向,縦方向はみだし判定結果(画面内: True/画面外: False)
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img2 = pg.image.load("ex02/fig/3.png")
    kk_img2 = pg.transform.flip(kk_img2,True, False)
    kk_img_over = pg.image.load("ex02/fig/6.png")
    kk_img_over = pg.transform.rotozoom(kk_img_over, 0, 2.0)
    kk_imgs = { # 追加要素1 : こうかとんの向き(画像追加)
        pg.K_UP:pg.transform.rotozoom(kk_img, 270, 2.0),
        pg.K_DOWN:pg.transform.rotozoom(kk_img, 90, 2.0),
        pg.K_LEFT:pg.transform.rotozoom(kk_img, 0, 2.0),
        pg.K_RIGHT:pg.transform.rotozoom(kk_img2, 0, 2.0)
    }
    current_img = kk_imgs[pg.K_LEFT]
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bb_img = pg.Surface((20,20)) # 練習1 : 透明のSurfaceを作る
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0,0,0)) # 練習1 : 黒い部分を透明にする
    bb_rct = bb_img.get_rect() # 練習1 : 爆弾SurfaceのRectを抽出する
    bb_rct.centerx = randint(0, WIDTH)
    bb_rct.centery = randint(0, HEIGHT)
    vx, vy = +5, +5 # 練習2 : 爆弾の速度

    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bb_rct): # 練習5 : 衝突判定
            screen.blit(bg_img, [0, 0])
            screen.blit(kk_img_over, kk_rct) # 追加要素2 : Game Over時こうかとんの画像を変更
            pg.display.update()
            delay = 1
            time.sleep(delay)
            screen.blit(bg_img, [0, 0])
            screen.blit(kk_img_over, kk_rct)
            fonto = pg.font.Font(None, 80)
            txt = fonto.render("Game Over", True, (255, 0, 0)) # 追加要素3 : Game Overと画面に表示
            screen.blit(txt, [300, 200])
            pg.display.update()
            delay = 1
            time.sleep(delay)
            print("Game Over")
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        
        for k, tpl in delta.items():
            if key_lst[k]: #　キーが押されたら
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
                current_img = kk_imgs.get(k)

        screen.blit(bg_img, [0, 0])
        kk_rct.move_ip(sum_mv[0], sum_mv[1])
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(current_img, kk_rct)
        bb_rct.move_ip(vx, vy) #　練習2 : 爆弾を移動させる
        yoko, tate = check_bound(bb_rct)
        if not yoko: #　横方向にはみ出たら
            vx *= -1
        if not tate:
            vy *= -1 # 縦方向にはみ出たら
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()