import pygame

class Gun:
    def __init__(self, name, ammo, damage, speed, reload_time, gun_sprite):
        """
        Initialize the Gun object.

        :param name: Name of the gun (e.g., "Pistol", "Rifle").
        :param ammo: Total ammo available for the gun.
        :param damage: Damage dealt by the gun per shot.
        :param speed: Speed of the bullets fired by the gun.
        :param reload_time: Time (in seconds) required to reload the gun.
        :param gun_sprite: The image of the gun.
        """
        self.name = name
        self.ammo = ammo
        self.damage = damage
        self.speed = speed
        self.reload_time = reload_time
        self.current_ammo = ammo  # Ammo currently loaded in the gun
        self.image = pygame.transform.scale(gun_sprite, (gun_sprite.get_width() * 2, gun_sprite.get_height() * 2))  # Resize the gun sprite
        self.rect = self.image.get_rect()
        self.bullets = []  # List to store bullets

    def update_position(self, player_rect, flipped):
        """
        Update the gun's position based on the player's position.
        :param player_rect: The player's rectangle.
        :param flipped: Whether the player is facing left or right.
        """
        # Adjust the gun's position closer to the player's body
        offset_x = -5 if flipped else 5  # Reduced horizontal offset to bring the gun closer
        offset_y = 0  # Align the gun vertically with the player's body
        if flipped:
            self.rect.midright = (player_rect.left + offset_x, player_rect.centery + offset_y)
        else:
            self.rect.midleft = (player_rect.right + offset_x, player_rect.centery + offset_y)

    def shoot(self, flipped):
        """
        Create a bullet and add it to the bullets list.
        :param flipped: Whether the player is facing left or right.
        """
        if self.current_ammo > 0:
            self.current_ammo -= 1
            direction = -1 if flipped else 1
            bullet = pygame.Rect(self.rect.centerx, self.rect.centery, 10, 5)  # Bullet size
            self.bullets.append((bullet, direction))
            print(f"{self.name} fired! Ammo left: {self.current_ammo}")
        else:
            print(f"{self.name} is out of ammo! Reload required.")

    def reload(self):
        """
        Reload the gun to its full ammo capacity.
        """
        print(f"Reloading {self.name}...")
        self.current_ammo = self.ammo
        print(f"{self.name} reloaded. Ammo: {self.current_ammo}")

    def update_bullets(self):
        """
        Update the position of all bullets and remove bullets that go off-screen.
        """
        for bullet in self.bullets[:]:
            bullet[0].x += self.speed * bullet[1]  # Move the bullet
            if bullet[0].right < 0 or bullet[0].left > 800:  # Assuming screen width is 800
                self.bullets.remove(bullet)  # Remove bullets off-screen

    def draw(self, screen):
        """
        Draw the gun and its bullets.
        """
        screen.blit(self.image, self.rect.topleft)  # Draw the gun
        for bullet, _ in self.bullets:
            pygame.draw.rect(screen, (255, 255, 0), bullet)  # Draw bullets (yellow rectangles)

    def __str__(self):
        """
        Return a string representation of the gun's current state.
        """
        return f"Gun: {self.name}, Ammo: {self.current_ammo}/{self.ammo}, Damage: {self.damage}, Speed: {self.speed}, Reload Time: {self.reload_time}s"


# Specific gun classes
class AK47(Gun):
    def __init__(self, gun_sprite):
        super().__init__(name="AK47", ammo=30, damage=35, speed=20, reload_time=2.5, gun_sprite=gun_sprite)


class Rifle(Gun):
    def __init__(self, gun_sprite):
        # Scale the rifle sprite to make it smaller
        scaled_sprite = pygame.transform.scale(gun_sprite, (int(gun_sprite.get_width() * 1), int(gun_sprite.get_height() * 1)))
        super().__init__(name="Rifle", ammo=30, damage=25, speed=15, reload_time=2, gun_sprite=scaled_sprite)


class Pistol(Gun):
    def __init__(self, gun_sprite):
        # Scale the pistol sprite to make it slightly larger
        scaled_sprite = pygame.transform.scale(gun_sprite, (int(gun_sprite.get_width() * 1.8), int(gun_sprite.get_height() * 1.8)))
        super().__init__(name="Pistol", ammo=12, damage=15, speed=10, reload_time=1.5, gun_sprite=scaled_sprite)


def take_damage(self, amount, knockback_direction):
    """
    Reduce the player's health and apply knockback.
    :param amount: The amount of damage to reduce from the player's health.
    :param knockback_direction: -1 for left, 1 for right.
    """
    if not self.invincible:  # Only take damage if not invincible
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            print("Player is dead!")
        else:
            self.knockback_direction = knockback_direction
            self.knockback_timer = self.knockback_frames  # Start knockback animation
            self.invincible = True  # Make the player invincible
            self.invincibility_timer = 60  # Set invincibility duration (e.g., 1 second at 60 FPS)


