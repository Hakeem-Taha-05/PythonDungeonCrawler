import globals
from classes import *
import math as m

up = Movement("up", 'w', 0, -1)
down = Movement("down", 's', 0, 1)
left = Movement("left", 'a', -1, 0)
right = Movement("right", 'd', 1, 0)

movements = [up, down, left, right]
char_type = {
    "#": Entity,
    "+": Entity,
    " ": Entity,
    "P": Player,
    "^": Enemy,
    "V": Enemy,
    "<": Enemy,
    ">": Enemy
}

def update_tiles():
    globals.display = [[' ' for _ in range(globals.cols)] for _ in range(globals.rows)]
    globals.tile_grid = [[' ' for _ in range(globals.cols)] for _ in range(globals.rows)]
    
    for tile in globals.tiles:
        if 0 <= tile.x < globals.cols and 0 <= tile.y < globals.rows:
            globals.display[tile.y][tile.x] = tile.type
            globals.tile_grid[tile.y][tile.x] = tile
    
    for entity in globals.entities:
        if entity.type == "o":
            for y in range(entity.height):
                for x in range(entity.width):
                    if entity.sprite[y][x] != " ":
                        globals.display[entity.y + y][entity.x + x] = entity.sprite[y][x]
            for tile in globals.tiles:
                dx = entity.x + m.floor(entity.width/2) - tile.x
                dy = entity.y + m.floor(entity.height/2) - tile.y
                if tile.type == " " and round(m.sqrt(dx**2 + dy**2)) == entity.range and 0 <= tile.x < globals.cols and 0 <= tile.y < globals.rows:
                    globals.display[tile.y][tile.x] = "'"
                    
    for projectile in globals.projectiles:
        for y in range(projectile.height):
            for x in range(projectile.width):
                globals.display[projectile.y + y][projectile.x + x] = projectile.sprite[y][x]
                
    for entity in globals.entities:
        if entity.type == "P":
            for y in range(entity.height):
                for x in range(entity.width):
                    if entity.sprite[y][x] != " " and 0 <= entity.x + x < globals.cols and 0 <= entity.y + y < globals.rows:
                        globals.display[entity.y + y][entity.x + x] = entity.sprite[y][x]            
                
def append_entity(type, x, y):
    cls = char_type.get(type, Entity)
    if cls is Player:
        globals.tiles.append(Entity(" ", x, y))
        globals.player = Player(type, x, y, 3)
        globals.entities.append(globals.player)
    elif cls is Enemy:
        enemy = cls(type, x, y)
        enemy.type = "o"
        globals.tiles.append(Entity(" ", x, y))
        globals.entities.append(enemy)
        globals.enemy_count += 1
    else:
        entity = cls(type, x, y)
        globals.tiles.append(entity)
    
def load_level(level_name):
    is_in_tile = False
    with open(level_name) as file:
        for line in file:
            if "MAP" in line:
                row = line[4:].strip().split(" ")
                globals.rows = int(row[0])
                globals.cols = int(row[1])
                is_in_tile = True
                current_row = 0
                continue
            if is_in_tile:
                current_col = 0
                if current_row == globals.rows:
                    is_in_tile = False
                    continue
                for char in line.strip():
                    append_entity(char, current_col, current_row)
                    current_col += 1
                current_row += 1
                update_tiles()
                
def print_tiles():
    for i, row in enumerate(globals.display):
        if i == 0:
            print(" ".join(row), end ="")
            print(" ", globals.message)
        elif i == 2:
            print(" ".join(row), end ="")
            print("  Ammo =", globals.player.ammo)
        elif i == 4:
            print(" ".join(row), end ="")
            print("  Health =", globals.player.health)
        elif i == 6:
            print(" ".join(row), end ="")
            print("  Facing direction =", globals.player.facing_direction.name)
        elif i == 8:
            print(" ".join(row), end ="")
            print("  Enemies remaining = ", globals.enemy_count)
        else:
            print(" ".join(row))
    globals.message = ""
    
def spawn_bullet(entity, direction):
    if direction == None:
        return 1
    else:
        bullet = Projectile("x", entity.x + m.floor(entity.width/2), entity.y + m.floor(entity.height/2), direction)
        globals.projectiles.append(bullet)
        
def delete_entity(deleted_entity):
    if deleted_entity in globals.entities:
            globals.entities.remove(deleted_entity)
    if deleted_entity in globals.tiles:
            globals.tiles.remove(deleted_entity)
    if deleted_entity in globals.projectiles:
            globals.projectiles.remove(deleted_entity)
    
def main():
    level_name = input("Enter level name: ")
    load_level(level_name)
    
    is_running = True
    while is_running:
        print_tiles()
        #Player movement
        key = input("Enter a direction (w/a/s/d) : ")
        for move in movements:
            if move.key == key:
                globals.player.move(move)
        if key == "f":
            if globals.player.ammo:
                spawn_bullet(globals.player, globals.player.facing_direction)
                globals.player.ammo -= 1
            else:
                globals.message = "You have no ammo left"
        
        #Projectile movement
        for projectile in globals.projectiles.copy():
            projectile.move()
            
        #Enemy movement
        for enemy in globals.entities:
            if enemy.type == "o":
                enemy.move()
                
            
        #Enemy and projectiles deletion
        hit_projectiles = [p for p in globals.projectiles if p.hit]
        hit_enemies = [e for e in globals.entities if e.type == "o" and e.hit]
        for projectile in hit_projectiles:
            delete_entity(projectile)
        for enemy in hit_enemies:
            delete_entity(enemy)
            globals.enemy_count -= 1
        
        #Exit conditions check
        if globals.player.health <= 0:
            globals.player.is_alive = False
            print("YOU DIED")
            is_running = True
        if globals.enemy_count == 0:
            print("YOU WON")
            is_running = False
        #print_tiles()
        update_tiles()
        

#For debugging
'''
print(rows, cols)

print(player)

for row in tiles:
    for char in row:
        print(char, end="")
    print()

print(f"player within enemy({enemy.x}, {enemy.y}) range = {enemy.player_in_range}")

print(projectile)

all_entities = globals.entities + globals.enemies + globals.projectiles
for entity in all_entities:
    print(entity)

for tile in globals.tiles:
    if player.is_colliding_with(tile):
        print("collided with tile", end="")
        print(tile)
            
'''

if __name__ == "__main__":
    main()