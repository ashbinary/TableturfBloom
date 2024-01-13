import byml
import zstd
import argparse
import os
import pyglet
import mmh3

argParser = argparse.ArgumentParser(description="A GUI tool for making Tableturf Battle cards.")

argParser.add_argument("-n", "-name", nargs="?", dest="name", help='input for the Tableturf card\'s internal name', required=True)
argParser.add_argument("-num", "-number", nargs="?", dest="number", help='input for the Tableturf card\'s number (defaults to the byml\'s length)')
argParser.add_argument("-t", "-type", nargs="?", dest="type", default="WeaponMain", help='input for the Tableturf card\'s category')
argParser.add_argument("-r", "-rarity", nargs="?", dest="rare", default="Common", help='input for the Tableturf card\'s rarity ("Common", "Rare", or "Fresh")')

args = argParser.parse_args()

cardRequest = "MiniGame_" + args.name

cardInfo_filename = [filename for filename in os.listdir('.') if filename.startswith("MiniGameCardInfo")]
with open(cardInfo_filename[0], "rb") as file:
    cardInfo_zstd = zstd.decompress(file.read())
cardInfo = byml.Byml(cardInfo_zstd).parse()

cardIndex = 0

try:
    cardIndex = [index for (index, item) in enumerate(cardInfo) if item['__RowId'] == cardRequest][0]
    print("Found card index - loading card!")
    card = cardInfo[cardIndex]
except IndexError:
    print("Could not find card index - creating new card.")
    cardNum = (args.number if args.number != None else len(cardInfo))

    card = {
        "Category": args.type,
        "Name": args.name,
        "NameHash": byml.UInt(int(mmh3.hash(args.name, signed = False))),
        "Number": byml.Int(cardNum),
        "Rarity": args.rare,
        "Season": byml.Int(1),
        "SpecialCost": byml.Int(3),
        "Square": ["Empty"] * 64,
        "SquareSortOffset": byml.Int(0),
        "__RowId": "MiniGame_" + args.name
    }
    cardInfo.append(card)
    cardIndex = card["Number"]
    

note_sprites = []
window = pyglet.window.Window(width=800, height=480)

# Used to store the static text graphics in the GUI
text_data = []
text_list = [
    ["Card: " + card["Name"] + " [#" + str(card["Number"]) + "]", 475, 380],
    ["Hash: " + str(card["NameHash"]), 475, 360, (255,255,255,128)],
    ["Special Cost: " + str(card["SpecialCost"]) + " blocks", 475, 320],
    ["Rarity: " + card["Rarity"], 475, 300],
    ["Category: " + card["Category"], 475, 280],
    ["Exit the program to Save", 554, 200],
    ["Change Sp. Cost with ← and →", 514, 180],
    ["L-Click to Swap Empty and Fill", 497, 140],
    ["R-Click to Add Special", 575, 120],
    ["--------- TableturfBloom --------", 470, 240, (255,255,255,128)],
]

text_batch = pyglet.graphics.Batch()

# Used to store the Tableturf blocks
minigame_grid = {}
block_batch = pyglet.graphics.Batch()

for text in text_list:
    text_data.append(
        pyglet.text.Label(
            text[0], font_name = 'Courier New', font_size = 12, 
            color = (text[3] if len(text) == 4 else (255, 255, 255, 255)), 
            x = text[1], y = text[2], 
            batch=text_batch))

for yr in range(0, 8):
    for xr in range(0, 8):
        size = 55
        minigame_grid[round(xr + (yr * 8))] = pyglet.sprite.Sprite(
                                                pyglet.image.load('asset/' + card['Square'][round(xr + (yr * 8))].lower() + '.png'), 
                                                y = (20 + (size * yr)), x = 20 + (size * xr), 
                                                batch=block_batch)

def swapBlockType(brick, button):
    if button == pyglet.window.mouse.LEFT:
        if card['Square'][brick] == 'Empty':
            minigame_grid[brick].image = pyglet.image.load('asset/fill.png')
            card['Square'][brick] = 'Fill'
        else:
            minigame_grid[brick].image = pyglet.image.load('asset/empty.png')
            card['Square'][brick] = 'Empty'
    elif pyglet.window.mouse.RIGHT:
        minigame_grid[brick].image = pyglet.image.load('asset/special.png')
        card['Square'][brick] = 'Special'

@window.event   
def on_mouse_press(x, y, button, modifiers):
    print("x: " + str(x) + ", y: " + str(y))
    if (20 < x < 460) and (20 < y < 520):
        brick_x = round((x - 47) / 55)
        brick_y = 7 - round((435 - y) / 55)
        swapBlockType(brick_x + (brick_y * 8), button)

@window.event
def on_key_press(symbol, modifiers):
    match symbol:
        case 65361 | 65363: #key.LEFT, #key.RIGHT
            card["SpecialCost"] -= 65362 - symbol # This was so funny to me I'm sorry I had to
            text_data[1].text = "Special Cost: " + str(card["SpecialCost"]) + " blocks"

@window.event
def on_draw():
    window.clear()
    block_batch.draw()
    text_batch.draw()

if __name__ == "__main__":
    pyglet.app.run()

# Saving functionality
card["SpecialCost"] = byml.Int(card["SpecialCost"])
cardInfo[cardIndex] = card

with open(cardInfo_filename[0], 'wb') as file:
    file.write(zstd.compress(byml.Writer(cardInfo, be=False, version=7).get_bytes()))