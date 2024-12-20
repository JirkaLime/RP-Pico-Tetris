# TETRIS
import LCD_lib as lcd
from machine import Pin, PWM
from ulab import numpy as np
import random
import time

keyA = Pin(15,Pin.IN,Pin.PULL_UP)
keyB = Pin(17,Pin.IN,Pin.PULL_UP)
keyX = Pin(19 ,Pin.IN,Pin.PULL_UP)
keyY= Pin(21 ,Pin.IN,Pin.PULL_UP)
left = Pin(16,Pin.IN,Pin.PULL_UP)
right = Pin(20,Pin.IN,Pin.PULL_UP)

last_frame_time = time.time()
frame_interval = 0.1

PWM(Pin(13)).freq(1000)
PWM(Pin(13)).duty_u16(32768)     #max jas - 65535

LCD = lcd.LCD_1inch3()
display = 240
offset_x = 24
block_size = 12
skibidi = -1
t_color = random.randint(0, 6)
t_rot = 0
t_type = random.randint(0, 6)
t_hor = 3
score = 0
key_timers = {"A": 0, "LEFT": 0, "RIGHT": 0}
debounce_interval = 0.2
board = np.zeros((20, 10), dtype=np.uint8)

BLOCK_TEXTURES = {
    0: np.array([[0, 0, 2, 2, 18407], [2, 0, 8, 2, 10079], [0, 2, 2, 8, 10079], [2, 2, 8, 8, 50236], [0, 10, 2, 2, 50236], [10, 0, 2, 2, 50236], [10, 2, 2, 8, 24858], [2, 10, 8, 2, 24858], [10, 10, 2, 2, 0]], dtype=np.uint16),
    1: np.array([[0, 0, 2, 2, 23783], [2, 0, 8, 2, 7389], [0, 2, 2, 8, 7389], [2, 2, 8, 8, 54234], [0, 10, 2, 2, 54234], [10, 0, 2, 2, 54234], [10, 2, 2, 8, 57736], [2, 10, 8, 2, 57736], [10, 10, 2, 2, 0]], dtype=np.uint16),
    2: np.array([[0, 0, 2, 2, 23783], [2, 0, 8, 2, 15463], [0, 2, 2, 8, 15463], [2, 2, 8, 8, 56388], [0, 10, 2, 2, 56388], [10, 0, 2, 2, 56388], [10, 2, 2, 8, 7200], [2, 10, 8, 2, 7200], [10, 10, 2, 2, 0]], dtype=np.uint16),
    3: np.array([[0, 0, 2, 2, 23783], [2, 0, 8, 2, 56388], [0, 2, 2, 8, 56388], [2, 2, 8, 8, 7200], [0, 10, 2, 2, 7200], [10, 0, 2, 2, 7200], [10, 2, 2, 8, 0], [2, 10, 8, 2, 0], [10, 10, 2, 2, 0]], dtype=np.uint16),
    4: np.array([[0, 0, 2, 2, 23783], [2, 0, 8, 2, 18407], [0, 2, 2, 8, 18407], [2, 2, 8, 8, 1501], [0, 10, 2, 2, 1501], [10, 0, 2, 2, 1501], [10, 2, 2, 8, 50130], [2, 10, 8, 2, 50130], [10, 10, 2, 2, 33489]], dtype=np.uint16),
    5: np.array([[0, 0, 2, 2, 18407], [2, 0, 8, 2, 1501], [0, 2, 2, 8, 1501], [2, 2, 8, 8, 33489], [0, 10, 2, 2, 33489], [10, 0, 2, 2, 33489], [10, 2, 2, 8, 57736], [2, 10, 8, 2, 57736], [10, 10, 2, 2, 0]], dtype=np.uint16),
    6: np.array([[0, 0, 2, 2, 18407], [2, 0, 8, 2, 23783], [0, 2, 2, 8, 23783], [2, 2, 8, 8, 18407], [0, 10, 2, 2, 1501], [10, 0, 2, 2, 1501], [10, 2, 2, 8, 50130], [2, 10, 8, 2, 50130], [10, 10, 2, 2, 57736]], dtype=np.uint16),
}

BLOCK_POSITIONS = {
    0: np.array([[5, 6, 9, 10]], dtype=np.uint8),
    1: np.array([[8, 9, 10, 11], [2, 6, 10, 14]], dtype=np.uint8),
    2: np.array([[4, 5, 6, 10], [1, 5, 9, 8], [0, 4, 5, 6], [1, 2, 5, 9]], dtype=np.uint8),
    3: np.array([[4, 5, 6, 8], [0, 1, 5, 9], [2, 4, 5, 6], [1, 5, 9, 10]], dtype=np.uint8),
    4: np.array([[5, 6, 8, 9], [1, 5, 6, 10]], dtype=np.uint8),
    5: np.array([[4, 5, 6, 9], [1, 4, 5, 9], [1, 4, 5, 6], [1, 5, 6, 9]], dtype=np.uint8),
    6: np.array([[4, 5, 9, 10], [2, 5, 6, 9]], dtype=np.uint8),
}

BLOCK_VECTORS = np.array([[0, 0], [1, 0], [2, 0], [3, 0],
                         [0, 1], [1, 1], [2, 1], [3, 1],
                         [0, 2], [1, 2], [2, 2], [3, 2],
                         [0, 3], [1, 3], [2, 3], [3, 3]], dtype=np.uint8)


def block_rotate(t_hor, t_type, t_rot):
    next_rot = (t_rot + 1) % len(BLOCK_POSITIONS[t_type])
    
    block_positions = BLOCK_POSITIONS[t_type][next_rot]
    
    for block_index in block_positions:
        cur_vector = BLOCK_VECTORS[block_index]
        block_x = cur_vector[0] + t_hor

        if block_x < 0 or block_x > 9:
            return t_rot
    
    t_rot = next_rot
    
    return t_rot


def block_move(t_hor, t_type, t_rot, wish_dir):
    block_positions = BLOCK_POSITIONS[t_type][t_rot]
    
    max_x = max(BLOCK_VECTORS[block_index][0] + t_hor for block_index in block_positions)
    min_x = min(BLOCK_VECTORS[block_index][0] + t_hor for block_index in block_positions)
    
    if wish_dir == 1 and max_x < 9:
        t_hor += 1
    elif wish_dir == -1 and min_x > 0:
        t_hor -= 1

    return t_hor

def block_texture(num, x, y):
    for rect in BLOCK_TEXTURES[num]:
        offset_x, offset_y, width, height, color = rect
        LCD.fill_rect(x + offset_x, y + offset_y, width, height, color)
        
def draw_block(pos_x, pos_y, block_type, block_rotation, block_color, offset_x, BLOCK_POSITIONS):
    for i in range(4):
        sub_array = BLOCK_POSITIONS[block_type][block_rotation]
        block_index = sub_array[i]
        
        cur_vector = BLOCK_VECTORS[block_index]
        
        block_x = block_size * cur_vector[0] + (12 * pos_x) + offset_x
        block_y = block_size * cur_vector[1] + (12 * pos_y)

        block_texture(block_color, block_x, block_y)

while True:
    current_time = time.time()

    if keyA.value() == 0 and current_time - key_timers["A"] >= debounce_interval:
        t_rot = block_rotate(t_hor, t_type, t_rot)
        key_timers["A"] = current_time

    elif left.value() == 0 and current_time - key_timers["LEFT"] >= debounce_interval:
        t_hor = block_move(t_hor, t_type, t_rot, -1)
        key_timers["LEFT"] = current_time

    elif right.value() == 0 and current_time - key_timers["RIGHT"] >= debounce_interval:
        t_hor = block_move(t_hor, t_type, t_rot, 1)
        key_timers["RIGHT"] = current_time


    if current_time - last_frame_time >= frame_interval:
        last_frame_time = current_time 
        print("!INFO: Vykreslovani...")
        skibidi += 1
        if (skibidi >= 18):
            skibidi = -1
            score += 1
            t_color = random.randint(0, 6)
            t_type = random.randint(0, 6)
            t_hor = 3
            t_rot = 0
        
        LCD.fill(0)
        LCD.fill_rect(23, 0, 1, 240, 0xffff)
        LCD.fill_rect(144, 0, 1, 240, 0xffff)
        LCD.text(f"SKORE: {score}", 160, 20, 0xffff)
        draw_block(t_hor, skibidi, t_type, t_rot, t_color, offset_x, BLOCK_POSITIONS)
        LCD.show()
    time.sleep(0.01)