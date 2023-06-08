import json
import pygame
import random


class GameInitializer:
    def __init__(self, screen_width, screen_height):
        # Initialize the game
        pygame.init()

        # Set up the display
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Spaceship Game")

        # Define colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)

        # Load images
        self.spaceship_img = pygame.image.load("spaceship.png").convert_alpha()
        self.spaceship_width, self.spaceship_height = self.spaceship_img.get_size()
        self.spaceship_width = int(self.spaceship_width * 0.3)  # Reduce width by 70%
        self.spaceship_height = int(self.spaceship_height * 0.3)  # Reduce height by 70%
        self.spaceship_img = pygame.transform.scale(self.spaceship_img, (self.spaceship_width, self.spaceship_height))

        self.asteroid_img = pygame.image.load("asteroid.png")
        self.powerup_gem_img = pygame.image.load("gem.png")
        self.powerup_power_img = pygame.image.load("power.png")
        self.powerup_weapon_img = pygame.image.load("weapon.png")
        self.shield_img = pygame.image.load("shield.png")

        # Set up the spaceship
        self.spaceship_x = self.screen_width // 2 - self.spaceship_width // 2
        self.spaceship_y = self.screen_height - self.spaceship_height - 10
        self.spaceship_speed = 5

        # Set up asteroids
        self.n_asteroids = 0
        self.asteroids = []
        self.asteroid_speed = 2
        self.asteroid_spawn_delay = 60  # Increase this value to decrease the frequency of asteroid spawns
        self.max_asteroid_size = min(self.screen_width, self.screen_height) // 3  # Maximum asteroid size is 30% of the screen size

        # bullet sound
        # bullet_sound = pygame.mixer.Sound("bullet_sound.wav")
        self.bullets = []

        # Set up power-ups
        self.powerups = []
        self.powerup_spawn_delay = 600  # Increase this value to decrease the frequency of power-up spawns
        self.max_powerup_size = min(self.screen_width, self.screen_height) // 2  # Maximum power-up size is 50% of the screen size

        # Define initial power and power increment
        self.power = 100
        self.power_increment = 50

        # Set up shields
        self.shielded = False
        self.shield_duration = 5 * 60  # 5 seconds at 60 FPS
        self.shield_time = 0

        # Set up weapons
        self.weapons = []
        self.weapon_levels = {
            1: {"image": pygame.image.load("weapon_level1.png"), "damage": 3, "timer": 5 * 60},  # 5 seconds at 60 FPS
            2: {"image": pygame.image.load("weapon_level2.png"), "damage": 2, "timer": 5 * 60},
            3: {"image": pygame.image.load("weapon_level3.png"), "damage": 1, "timer": 10 * 60}  # 10 seconds at 60 FPS
        }
        self.current_weapon_level = 0
        self.weapon_timer = 0

        # Game variables
        self.score = 0
        self.score_timer = 0
        self.game_over = False
        self.game_running = False

        self.clock = pygame.time.Clock()

        # Load weapon images
        self.weapon_level1_img = pygame.image.load("weapon_level1.png")
        self.weapon_level2_img = pygame.image.load("weapon_level2.png")
        self.weapon_level3_img = pygame.image.load("weapon_level3.png")

        self.weapon_width = 50  # Set the desired width of the weapon images
        self.weapon_height = 50  # Set the desired height of the weapon images
        # Scale weapon images
        self.weapon_level1_img = pygame.transform.scale(self.weapon_level1_img, (self.weapon_width, self.weapon_height))
        self.weapon_level2_img = pygame.transform.scale(self.weapon_level2_img, (self.weapon_width, self.weapon_height))
        self.weapon_level3_img = pygame.transform.scale(self.weapon_level3_img, (self.weapon_width, self.weapon_height))

        # Create a list of weapon images
        self.weapon_imgs = [self.weapon_level1_img, self.weapon_level2_img, self.weapon_level3_img]


class GameStateManager:
    def save_game_state(self, file_path):
        state = {
            "asteroids": self.n_asteroids,
            "powerups": self.powerups,
            "weapons": self.weapons,
            "score": self.score,
            "current_weapon_level": self.current_weapon_level
        }
        with open(file_path, "w") as file:
            json.dump(state, file)

    def load_game_state(self, file_path):
        try:
            with open(file_path, "r") as file:
                state = json.load(file)
            self.asteroids = state["asteroids"]
            self.powerups = state["powerups"]
            self.weapons = state["weapons"]
            self.score = state["score"]
            self.current_weapon_level = state["current_weapon_level"]
        except FileNotFoundError:
            # Handle the case when the file doesn't exist or cannot be loaded
            print("Game state file not found. Starting a new game.")


class Game(GameInitializer, GameStateManager):
    def __init__(self):
        super().__init__(800, 600)

    def start_game(self):
        self.power = 100
        self.game_running = True
        self.score = 0
        self.score_timer = 0
        self.game_over = False
        self.current_weapon_level = 0
        self.asteroids.clear()
        self.powerups.clear()
        self.weapons.clear()

        self.game_loop()

    def draw_power_meter(self):
        power_meter_width = 200
        power_meter_height = 20
        power_meter_x = self.screen_width // 2 - power_meter_width // 2
        power_meter_y = 10

        # Calculate the width of the power meter fill based on the current power value
        power_fill_width = int((self.power / 100) * power_meter_width)

        # Draw the power meter outline
        pygame.draw.rect(self.screen, self.WHITE, (power_meter_x, power_meter_y, power_meter_width, power_meter_height),
                         2)

        # Draw the power meter fill
        pygame.draw.rect(self.screen, self.GREEN, (power_meter_x, power_meter_y, power_fill_width, power_meter_height))

    def game_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.game_running:
                            self.start_game()
                        else:
                            self.start_game()
                    if event.key == pygame.K_SPACE:
                        if self.current_weapon_level > 0:
                            self.bullet_x = self.spaceship_x + self.spaceship_width // 2
                            self.bullet_y = self.spaceship_y
                            self.bullet_width = 5
                            self.bullet_height = 10
                            self.bullets.append([self.bullet_x, self.bullet_y, self.bullet_width, self.bullet_height])
                            # bullet_sound.play()

            if not self.game_running:
                self.screen.fill(self.BLACK)
                self.font = pygame.font.Font(None, 36)
                self.text = self.font.render("Press Enter to Start", True, self.WHITE)
                self.text_rect = self.text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
                self.screen.blit(self.text, self.text_rect)
                pygame.display.flip()
                continue

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_running = False

            self.keys = pygame.key.get_pressed()
            if self.keys[pygame.K_LEFT]:
                self.spaceship_x -= self.spaceship_speed
            if self.keys[pygame.K_RIGHT]:
                self.spaceship_x += self.spaceship_speed

            # Update the spaceship position
            if self.spaceship_x < 0:
                self.spaceship_x = 0
            elif self.spaceship_x > self.screen_width - self.spaceship_width:
                self.spaceship_x = self.screen_width - self.spaceship_width

            # Spawn asteroids
            if random.randint(0, self.asteroid_spawn_delay) == 0:
                self.asteroid_width = random.randint(10, self.max_asteroid_size)
                self.asteroid_height = self.asteroid_width
                self.asteroid_x = random.randint(0, self.screen_width - self.asteroid_width)
                self.asteroid_y = random.randint(-self.screen_height, -self.asteroid_height)
                self.asteroids.append([self.asteroid_x, self.asteroid_y, self.asteroid_width, self.asteroid_height])

            # Spawn power-ups
            if random.randint(0, self.powerup_spawn_delay) == 0:
                self.powerup_type = random.choice(["gem", "power", "weapon"])
                self.powerup_width = random.randint(10, self.max_powerup_size)
                self.powerup_height = self.powerup_width
                self.powerup_x = random.randint(0, self.screen_width - self.powerup_width)
                self.powerup_y = random.randint(-self.screen_height, -self.powerup_height)
                self.powerups.append(
                    [self.powerup_x, self.powerup_y, self.powerup_width, self.powerup_height, self.powerup_type])

            # Move and remove asteroids
            for asteroid in self.asteroids:
                asteroid[1] += self.asteroid_speed
                if asteroid[1] > self.screen_height:
                    self.asteroids.remove(asteroid)
                    self.score += 1
                    self.n_asteroids += 1

            # Move and remove weapons
            for weapon in self.weapons:
                weapon[1] -= self.asteroid_speed - 1
                if weapon[1] < -weapon[3]:
                    self.weapons.remove(weapon)

            # Check for collision between bullets and asteroids
            for bullet in self.bullets:
                bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet[2], bullet[3])
                for asteroid in self.asteroids:
                    asteroid_rect = pygame.Rect(asteroid[0], asteroid[1], asteroid[2], asteroid[3])
                    if bullet_rect.colliderect(asteroid_rect):
                        self.bullets.remove(bullet)
                        self.asteroids.remove(asteroid)
                        self.score += 10

            # Check for collision with asteroids
            for asteroid in self.asteroids:
                asteroid_rect = pygame.Rect(asteroid[0], asteroid[1], asteroid[2], asteroid[3])
                spaceship_rect = pygame.Rect(self.spaceship_x, self.spaceship_y, self.spaceship_width,
                                             self.spaceship_height)
                if spaceship_rect.colliderect(asteroid_rect):
                    if self.shielded:
                        self.asteroids.remove(asteroid)
                        self.score += 10
                        self.n_asteroids += 1
                    else:
                        self.power -= 50  # Decrease power by 100 for each asteroid collision
                        if self.power <= 0:
                            self.game_over = True
                            break

                # Check for collision with weapons
                for weapon in self.weapons:
                    weapon_rect = pygame.Rect(weapon[0], weapon[1], weapon[2], weapon[3])
                    if weapon_rect.colliderect(asteroid_rect):
                        self.weapons.remove(weapon)
                        asteroid[4] -= self.weapon_levels[self.current_weapon_level]["damage"]
                        if asteroid[4] <= 0:
                            self.asteroids.remove(asteroid)
                            self.score += 10

            # move and remove bullets
            for bullet in self.bullets:
                bullet[1] -= 5  # Adjust the bullet speed as needed
                if bullet[1] < -bullet[3]:
                    self.bullets.remove(bullet)

            # Move power-ups
            for powerup in self.powerups:
                powerup[1] += self.asteroid_speed

            # Check for collision with power-ups
            for powerup in self.powerups:
                powerup_rect = pygame.Rect(powerup[0], powerup[1], powerup[2], powerup[3])
                if (
                        self.spaceship_x < powerup[0] + powerup[2]
                        and self.spaceship_x + self.spaceship_width > powerup[0]
                        and self.spaceship_y < powerup[1] + powerup[3]
                        and self.spaceship_y + self.spaceship_height > powerup[1]
                ):
                    self.powerups.remove(powerup)
                    if powerup[4] == "gem":
                        self.score += 10
                        self.power += self.power_increment  # Increase power by power_increment when collecting a gem power-up
                    elif powerup[4] == "power":
                        self.shielded = True
                        self.shield_time = self.shield_duration
                    elif powerup[4] == "weapon":
                        if self.current_weapon_level == 0:
                            self.current_weapon_level = 1
                            self.weapon_timer = self.weapon_levels[self.current_weapon_level]["timer"]
                        else:
                            self.current_weapon_level = (self.current_weapon_level + 1) % len(self.weapon_levels)

                        if self.current_weapon_level > 3:
                            self.current_weapon_level = 1
                            self.weapon_timer = self.weapon_levels[self.current_weapon_level]["timer"]
                        else:
                            self.weapon_timer = self.weapon_levels[self.current_weapon_level]["timer"]

            # Update weapon timer
            if self.weapon_timer > 0:
                self.weapon_timer -= 1

            # Check if weapon timer has expired
            if self.weapon_timer == 0:
                self.current_weapon_level = 0

            # draw bullets on screen
            for bullet in self.bullets:
                bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet[2], bullet[3])
                pygame.draw.rect(self.screen, self.BLUE, bullet_rect)

            # Draw current weapon
            if self.current_weapon_level != 0:
                weapon_image = self.weapon_levels[self.current_weapon_level]["image"]
                weapon_rect = weapon_image.get_rect()
                weapon_rect.centerx = spaceship_rect.centerx
                weapon_rect.y = spaceship_rect.y
                self.screen.blit(weapon_image, weapon_rect)

            if self.current_weapon_level == 3 and len(self.asteroids) == 0:
                self.level = 1
                self.current_weapon_level = 3
                self.weapon_timer = self.weapon_levels[self.current_weapon_level]["timer"]
                self.asteroid_speed = 2
            # Draw on the screen
            self.screen.fill(self.BLACK)
            if self.shielded:
                self.screen.blit(self.shield_img, (self.spaceship_x - 10, self.spaceship_y - 10))
                shield_time_text = self.font.render(f"Shield Time: {int(self.shield_time / 60)}s", True, self.WHITE)
                self.screen.blit(shield_time_text, (10, 50))
            self.screen.blit(self.spaceship_img, (self.spaceship_x, self.spaceship_y))
            for asteroid in self.asteroids:
                asteroid_rect = pygame.Rect(asteroid[0], asteroid[1], asteroid[2], asteroid[3])
                asteroid_img_resized = pygame.transform.scale(self.asteroid_img, (asteroid[2], asteroid[3]))
                self.screen.blit(asteroid_img_resized, asteroid_rect)
            for powerup in self.powerups:
                powerup_rect = pygame.Rect(powerup[0], powerup[1], powerup[2], powerup[3])
                if powerup[4] == "gem":
                    powerup_img_resized = pygame.transform.scale(self.powerup_gem_img, (powerup[2], powerup[3]))
                elif powerup[4] == "power":
                    powerup_img_resized = pygame.transform.scale(self.powerup_power_img, (powerup[2], powerup[3]))
                elif powerup[4] == "weapon":
                    powerup_img_resized = pygame.transform.scale(self.powerup_weapon_img, (powerup[2], powerup[3]))
                self.screen.blit(powerup_img_resized, powerup_rect)

            # Draw the spaceship
            self.screen.blit(self.spaceship_img, (self.spaceship_x, self.spaceship_y))

            for bullet in self.bullets:
                bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet[2], bullet[3])
                pygame.draw.rect(self.screen, self.BLUE, bullet_rect)

            weapon_offset = self.spaceship_width  # Offset to position the collected weapons
            if self.current_weapon_level > 0:
                for weapon_level in range(self.current_weapon_level):
                    weapon_img = self.weapon_imgs[weapon_level]
                    weapon_width, weapon_height = weapon_img.get_size()
                    self.screen.blit(weapon_img, (self.spaceship_x + weapon_offset, self.spaceship_y))
                    weapon_offset += weapon_width

            # Draw weapons
            for weapon in self.weapons:
                weapon_rect = pygame.Rect(weapon[0], weapon[1], weapon[2], weapon[3])
                pygame.draw.rect(self.screen, self.RED, weapon_rect)

            # Display current weapon level and timer
            if self.current_weapon_level != 0:
                weapon_level_text = self.font.render("Weapon Level: " + str(self.current_weapon_level), True,
                                                     self.WHITE)
                self.screen.blit(weapon_level_text, (600, 10))
                if self.current_weapon_level != 0:
                    weapon_timer_text = self.font.render("Weapon Timer: " + str(self.weapon_timer // 60) + "s", True,
                                                         self.WHITE)
                    self.screen.blit(weapon_timer_text, (600, 50))

            # Update shield timer
            if self.shielded:
                self.shield_time -= 1
                if self.shield_time <= 0:
                    self.shielded = False

            # Display score
            self.font = pygame.font.Font(None, 36)
            score_text = self.font.render(f"Score: {self.score}", True, self.WHITE)
            self.screen.blit(score_text, (10, 10))

            # Render power meter
            self.draw_power_meter()

            pygame.display.update()
            self.clock.tick(60)  # Set the frame rate to 60

            # Game over logic
            if self.game_over:
                self.game_running = False
                self.screen.fill(self.BLACK)
                self.font = pygame.font.Font(None, 36)
                text = self.font.render(f"Game Over - Score: {self.score}", True, self.WHITE)
                text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
                self.screen.blit(text, text_rect)
                pygame.display.flip()
                pygame.time.wait(2000)  # Wait for 2 seconds before restarting the game
                self.save_game_state("game_state.json")


class SaveableGame(Game):
    def save_game_state(self, file_path):
        state = {
            "asteroids": self.n_asteroids,
            "powerups": self.powerups,
            "weapons": self.weapons,
            "score": self.score,
            "current_weapon_level": self.current_weapon_level
        }
        with open(file_path, "w") as file:
            json.dump(state, file)

    def load_game_state(self, file_path):
        try:
            with open(file_path, "r") as file:
                state = json.load(file)
            self.asteroids = state["asteroids"]
            self.powerups = state["powerups"]
            self.weapons = state["weapons"]
            self.score = state["score"]
            self.current_weapon_level = state["current_weapon_level"]
        except FileNotFoundError:
            # Handle the case when the file doesn't exist or cannot be loaded
            print("Game state file not found. Starting a new game.")


if __name__ == "__main__":
    game = SaveableGame()
    game.start_game()
    game.start_again()
