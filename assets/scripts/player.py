import pygame

import assets.scripts.entity as entity
import assets.scripts.inventory as inventory
import assets.scripts.weapon as weapon

# player class
class Player(entity.Entity):
    def __init__(self, state, keys):
        super().__init__(0, 0, 64, 64, 10, 100, "player.png")
        self.state = "active"
        self.attack = False
        self.pickup = False
        self.switched = True
        self.inventory = inventory.Inventory()
        if state != "lobby":
            self.inventory.hotbar[0] = "sword"
            self.inventory.hotbar[1] = "bow"
        self.active_item = self.inventory.hotbar[self.inventory.active_slot]
        self.item_picked_up = "empty"
        self.keys = keys

    def move(self, dt, rooms, enemies, scroll):
        super().move(dt, rooms)
        for item in self.inventory.hotbar:
            if isinstance(item, list) and item[0] == "key" and item[1] not in self.keys:
                self.keys.append(item[1])
        for row in self.inventory.space:
            for item in row:
                if isinstance(item, list) and item[0] == "key" and item[1] not in self.keys:
                    self.keys.append(item[1])
        if self.switched:
            if self.inventory.hotbar[self.inventory.active_slot] == "sword":
                self.active_item = weapon.Sword(self, 30, 64)
            elif self.inventory.hotbar[self.inventory.active_slot] == "bow":
                self.active_item = weapon.Bow(self, 15, 20)
            else:
                self.active_item = "empty"
            self.switched = False
        if self.health < 100:
            self.health += 0.01
        self.check_damaged(enemies)
        if isinstance(self.active_item, weapon.Sword):
            self.attack = self.active_item.update(dt)
        elif isinstance(self.active_item, weapon.Bow):
            self.active_item.update(pygame.mouse.get_pos()[0] + scroll[0], pygame.mouse.get_pos()[1] + scroll[1], enemies, dt)

    def check_damaged(self, enemies):
        if self.immune:
            self.immune_timer -= 1
        if self.immune_timer <= 0 and self.immune:
            self.immune = False
            self.state = "active"
        for enemy in enemies:
            if self.rect.colliderect(enemy.weapon.rect) and enemy.attack and not self.immune:
                self.health -= enemy.weapon.damage
                self.state = "stunned"
                self.knockback_direction = enemy.direction
                self.immune = True
                self.immune_timer = 15

        if self.health <= 0:
            self.alive = False


    def draw(self, screen, scroll):
        super().draw(screen, scroll)
        if self.active_item != "empty":
            self.active_item.draw(screen, scroll)
