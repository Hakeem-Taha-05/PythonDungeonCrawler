import globals
import math as m
import sprites 

class Entity:
    def __init__(self, type, x, y):
        self.type = type
        self.x = x
        self.y = y
        self.sprite = sprites.default
        self.height = len(self.sprite)
        self.width = len(self.sprite[0])
        
    def __str__(self):
        return f"type = {self.type}, x = {self.x}, y = {self.y}"
    
    def update_position(self, move):
        self.x += move.dx
        self.y += move.dy
    
    def is_colliding_with(self, other):
        if other in globals.entities or other in globals.projectiles:
            return (
                self.x < other.x + other.width and      #self's LEFT side is to the LEFT of other's RIGHT side
                self.x + self.width > other.x and       #self's RIGHT side is to the RIGHT of other's LEFT side
                self.y < other.y + other.height and     #self's TOP is ABOVE other's BOTTOM
                self.y + self.height > other.y          #self's BOTTOM is BELOW other's TOP
                )
        elif other in globals.tiles:
            return (
                other.x < self.x + self.width and
                other.x >= self.x and
                other.y < self.y + self.height and
                other.y >= self.y 
                )

class Node:
    def __init__(self, x, y, parent, is_visited, direction_from_parent):
        self.x = x
        self.y = y
        self.parent = parent
        self.is_visited = is_visited

class Player(Entity):
    def __init__(self, type, x, y, health,):
        super().__init__(type, x, y)
        self.health = health
        self.is_alive = True
        self.facing_direction = up
        self.sprite = sprites.player
        self.height = len(self.sprite)
        self.width = len(self.sprite[0])
        self.ammo = 5
        
    def __str__(self):
        return f"type = {self.type}, x = {self.x}, y = {self.y}, dir = {self.facing_direction}, health = {self.health}"
        
    def move(self, move):
        self.facing_direction = move
        self.update_position(move)
        for tile in globals.tiles:
            if tile.type =="#" and self.is_colliding_with(tile) :
                globals.message = "Can't move"
                self.update_position(move.reverse())
                return 1
        for entity in globals.entities:
            if entity.type =="o" and self.is_colliding_with(entity):
                self.update_position(move.reverse())
                self.health -= entity.damage
                globals.message = f"Taken {entity.damage} damage"

class Enemy(Entity):
    def __init__(self, type, x, y):
        super().__init__(type, x, y)
        match self.type:
            case "^":
                self.direction = up
            case "V":
                self.direction = down
            case "<":
                self.direction = left
            case ">":
                self.direction = right
        self.range = 10
        self.player_in_range = False
        self.hit = False
        self.sprite = sprites.enemy
        self.height = len(self.sprite)
        self.width = len(self.sprite[0])
        self.damage = 1
        self.is_forward = True
        
    def __str__(self):
        return f"type = {self.type}, x = {self.x}, y = {self.y}, direction = {self.direction.dx}, {self.direction.dy}"
    
    @staticmethod
    def initialize_nodes():
        globals.nodes = [[None for _ in range(globals.cols + 1)] for _ in range(globals.rows)]
        for tile in globals.tiles:
            globals.nodes[tile.y][tile.x] = Node(tile.x, tile.y, None, False, None)
    
    @staticmethod
    def is_block_walkable(startX, startY, width, height):
        for y in range(height):
            for x in range(width):
                if not (0 <= startX + x < globals.cols and 0 <= startY + y < globals.rows):
                    return False
                if globals.tile_grid[startY + y][startX + x].type == "#":
                    return False
        return True
        
    def BFS(self, target):
        Enemy.initialize_nodes()
        start_node = globals.nodes[self.y][self.x]
        start_node.is_visited = True
        frontier = [start_node]
        
        while frontier:
            current_node = frontier.pop(0)
            if current_node.x == target.x and current_node.y == target.y:
                while current_node.parent.parent is not None:
                    #globals.display[current_node.y][current_node.x] = "*"
                    current_node = current_node.parent
                return current_node.direction_from_parent   
            
            else:
                for move in movements:
                    new_x = current_node.x + move.dx
                    new_y = current_node.y + move.dy
                    new_node = globals.nodes[new_y][new_x]
                    node_is_valid = Enemy.is_block_walkable(new_node.x, new_node.y, self.width, self.height)
                    
                    if not new_node.is_visited and node_is_valid:
                        new_node.parent = current_node
                        new_node.is_visited = True
                        new_node.direction_from_parent = move
                        frontier.append(new_node)
        return self.direction

    def move(self):
        forwards = self.direction
        backwards = self.direction.reverse()
        if self.is_forward:
            direction = forwards
        else:
            direction = backwards
        if self.player_in_range:
            direction = self.BFS(globals.player)
        self.try_move(direction)
    
    def check_box_within_range(self, entity):
        def clamp(value, min_value, max_value):
            return min(min_value, max(value, max_value))
        
        centerX = self.x + m.floor(entity.width/2)
        centerY = self.y + m.floor(entity.height/2)
        
        closest_x = clamp(centerX, entity.x, entity.x + entity.width)
        closest_y = clamp(centerY, entity.y, entity.y + entity.height)
        
        dx = centerX - closest_x
        dy = centerY - closest_y
        
        return round(m.sqrt(dx**2 + dy**2)) <= self.range
        
        
    def try_move(self, direction):
        self.update_position(direction)
        for tile in globals.tiles:
            if tile.type == "#" and self.is_colliding_with(tile):
                self.is_forward = not self.is_forward
                self.update_position(direction.reverse())
                self.update_position(direction.reverse())
                    
        for entity in globals.entities:
            if entity.type == "P" and self.is_colliding_with(entity):
                self.is_forward = not self.is_forward
                self.update_position(direction.reverse())
                self.update_position(direction.reverse())
                entity.health -= self.damage
                globals.message = f"Taken {self.damage} damage"
        if self.check_box_within_range(globals.player):
            self.player_in_range = True
        else:
            self.player_in_range = False
                    

class Projectile(Entity):
    def __init__(self, type, x, y, direction):
        super().__init__(type, x, y)
        self.direction = direction
        self.hit = False
        match direction.name:
            case "up":
                self.sprite = sprites.bullet_up
            case "down":
                self.sprite = sprites.bullet_down
            case "left":
                self.sprite = sprites.bullet_left
            case "right":
                self.sprite = sprites.bullet_right    
        self.height = len(self.sprite)
        self.width = len(self.sprite[0])
    
    def __str__(self):
        return f"Projectile({self.x}, {self.y}) dir({self.direction.dx}, {self.direction.dy}), hit = {self.hit}"
    
    def move(self):
        self.update_position(self.direction)
        for tile in globals.tiles:
            if tile.type != " " and self.is_colliding_with(tile):
                self.hit = True
        for entity in globals.entities:
            if entity.type == "o" and self.is_colliding_with(entity):
                self.hit = True
                entity.hit = True
'''
class LoopEnemy(Enemy):
    def __init__(self, type, x, y, direction, startX, startY, endX, endY):
        super().__init__(type, x, y, direction)
        self.startX = startX
        self.startY = startY
        self.endX = endX
        self.endY = endY
'''

class Movement:
    def __init__(self, name, key, dx, dy):
        self.name = name
        self.key = key
        self.dx = dx
        self.dy = dy

    def __str__(self):
        return f"{self.key}({self.dx}, {self.dy})"
    
    def reverse(self):
        return Movement(None ,None, -self.dx, -self.dy)

up = Movement("up", 'w', 0, -1)
down = Movement("down", 's', 0, 1)
left = Movement("left", 'a', -1, 0)
right = Movement("right", 'd', 1, 0)

movements = [up, down, left, right]