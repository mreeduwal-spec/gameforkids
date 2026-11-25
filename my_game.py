# file: my_game.py

import pgzrun
import random
import time #จับเวลาถอยหลังของเกม


WIDTH = 700  # ความกว้างหน้าจอ
HEIGHT = 500 # ความสูงหน้าจอ
player = Actor('zabiq', (WIDTH // 2, HEIGHT - 50))
coins = Actor('coins', (WIDTH // 2, 0+50))
score = 0 #คะแนนเริ่มต้นเป็น ศูนย์
lives = 5    #พลังชีวิต เริ่มต้นเป็น 5
game_over = False  #ตั้งค่าสถานะ game_over เป็นเท็จ
GAME_DURATION = 30 #จับเวลาถอยหลังของเกม กำหนดช่วงเวลาเป็น 10 วินาที
start_time = time.monotonic() #จับเวลาถอยหลังของเกม


def draw(): #;ฟังก์ชันสำหรับวาดภาพบนหน้าจอ
    screen.clear() #;ล้างหน้าจอ
    screen.fill((0, 0, 0)) #;กำหนดสีพื้นหลังเป็นสีดำ
    #แสดงเวลานับถอยหลัง
    remaining = max(0, int(GAME_DURATION - (time.monotonic() - start_time)))
    minutes = remaining // 60
    seconds = remaining % 60 
    screen.draw.text(
        f"{minutes:02}:{seconds:02}", #แสดงเวลานับถอยหลังในรูปแบบ นาที:วินาที
        center=(WIDTH // 2,25), #แสดงเวลานับถอยหลังตรงกลางหน้าจอด้านบน
        color="white",
        fontsize=40
    )     #แสดงเวลานับถอยหลัง
    if game_over == False: # หรือ lives > 0 แสดงว่า เกมยังไม่จบ
        #แสดงคะแนนบนจอที่ตำแหน่ง (10,10) ด้วยตัวอักษรสีขาว ขนาด 30 หน่วย
        screen.draw.text(f"Score: {score}", (10, 10), color="white", fontsize=30)
        #แสดงพลังชีวิตบนจอที่ตำแหน่ง (WIDTH - 150,10) ด้วยตัวอักษรสีขาว ขนาด 30 หน่วย
        screen.draw.text(f"Lives: {lives}", (WIDTH-150, 10), color="white", fontsize=30)
        player.draw() #วาดตัวละคร player บนหน้าจอ
        coins.draw() #วาดเหรียญ coins บนหน้าจอ
    else: #จบเกม
        screen.draw.text("Game Over", (150, 100), color="red", fontsize=100)
    
def update(): #ฟังก์ชันสำหรับอัปเดตสถานะของเกม
    global score,lives 
    global game_over

    remaining = GAME_DURATION - (time.monotonic() - start_time) #จับเวลาถอยหลังของเกม
    if remaining <= 0:
        game_over = True #การตรวจสอบเวลา
    if lives > 0: #จำนวนตัวเลขชีวิตมากกว่า 0 แสดงว่า เกมยังไม่จบ
        # เคลื่อนที่ player ตามปุ่มลูกศร
        if keyboard.left:   #กดแป้นพิมพ์ลูกศรซ้าย
            player.x -= 15	#ลดค่าแกน x ลง 5 หน่วย เพิ่มลด ความเร็วของการเคลื่อนที่ของ player ได้ตามต้องการ
        if keyboard.right:  #กดแป้นพิมพ์ลูกศรซ้าย
            player.x += 15	#เพิ่มค่าแกน x ลง 5 หน่วย

        # จำกัดไม่ให้ออกนอกขอบจอ
        if player.x < 0: #จำกัดไม่ให้ออกนอกขอบจอด้านซ้าย
            player.x = 0 # กำหนดค่าแกน x ให้เท่ากับ 0
        if player.x > WIDTH: #จำกัดไม่ให้ออกนอกขอบจอด้านขวา
            player.x = WIDTH # กำหนดค่าแกน x ให้เท่ากับ WIDTH

        # ให้เหรียญตกลงมาต่อเนื่อง (เพิ่มค่า y ทีละ 2 หน่วย)
        coins.y += 7 #เพิ่มค่าแกน y(การลงของcoins) ของเหรียญลง 5 หน่วย
        if coins.y > HEIGHT: #ตรวจสอบว่าเหรียญตกลงไปถึงขอบล่างของหน้าจอหรือไม่
            coins.x = random.randint(50, WIDTH-50) 
            coins.y = 50 
            lives -= 1
            sounds.misscoin.play() 
        #ตรวจสอบว่าเก็บเหรียญได้หรือไม่
        if player.colliderect(coins): 
            score +=1
            coins.x = random.randint(50, WIDTH-50)
            coins.y = 50
            sounds.getcoin.play()

    #ถ้าพลังชีวิตมีค่าเท่ากับ 0 แสดงข้อความจบเกม
    elif lives == 0:
        game_over = True    #ตั้งค่าสถานะให้เป็นจบเกม
        sounds.gameover.play()
        lives = -1
        return game_over
pgzrun.go() #ลูปเกม / เริ่มต้นเกมใหม่


