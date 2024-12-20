## RP-Pico-Tetris
### Použil jsem:
#### Waveshare Pico LCD 1.3: <https://www.waveshare.com/wiki/Pico-LCD-1.3>
#### Raspberry Pi Pico: <https://www.raspberrypi.com/products/raspberry-pi-pico>
#### Firmware: <https://github.com/v923z/micropython-ulab>
> Firmware ulab jsem zvolil z důvodu potřeby knihovny numpy, která bohužel není součástí základního MicroPython firmwaru pro Pi Pico.
### **Zdroje:**
#### Tetris in Python: <https://www.youtube.com/watch?v=nF_crEtmpBo&t>
#### Tetris Moves: <https://codegolf.stackexchange.com/questions/90255/given-a-list-of-tetris-moves-return-the-number-of-completed-lines>
#### Tetris Rotation: <https://harddrop.com/wiki/Nintendo_Rotation_System>
#### Tetris Wiki: <https://tetris.fandom.com/wiki/SRS>
### **Překlad barev:**
#### Displej který jsem použil nepužívá normální formát pro zobrazení barev jako je HEX [[1]](https://en.wikipedia.org/wiki/Web_colors) nebo RGB [[2]](https://en.wikipedia.org/wiki/RGB_color_model).
#### Proto jsem si napsal jednoduchý program v Pythonu na konvertování barev z PNG obrázků, což mi velmi usnadnilo manipulaci s barvami textur.


### Jak to vypadá?
![Tetromina](https://github.com/JirkaLime/RP-Pico-Tetris/blob/main/Obrazky/gp01.avifs?raw=true)

### Co to umí?
#### Program umí plně pohyovat s Tetrominy [[3]](https://en.wikipedia.org/wiki/Tetromino), umí s nimi rotovat a bere v potaz kolize,
#### okolního prostředí. Bloky mají 7 barevných provedení, 7 růných tvarů a každý z nich může rotovat. 
> V této verzi program nejeví žádné chyby a vše funguje jak má.
##### Barevné provedení, Typy a možné rotace Tetromin
![Tetromina](https://github.com/JirkaLime/RP-Pico-Tetris/blob/main/tetris_sheet.png?raw=true)
