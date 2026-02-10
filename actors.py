# Cavern - Actor Classes
# All game entities with dependency injection for game reference

from random import choice, randint, random
from pgzero.actor import Actor

from constants import (
    WIDTH, HEIGHT, ANCHOR_CENTRE, ANCHOR_CENTRE_BOTTOM, GRID_BLOCK_SIZE
)
from utils import block, sign


class CollideActor(Actor):
    """
    Base actor class with collision detection.
    
    Provides pixel-by-pixel movement with block collision checking.
    All actors that need collision detection should inherit from this.
    """
    
    def __init__(self, pos, game, anchor=ANCHOR_CENTRE):
        """
        Initialize a CollideActor.
        
        Args:
            pos: Initial (x, y) position
            game: Reference to the Game instance
            anchor: Anchor point for the sprite
        """
        super().__init__("blank", pos, anchor)
        self.game = game
    
    def move(self, dx, dy, speed):
        """
        Move the actor with collision detection.
        
        Movement is done 1 pixel at a time to prevent embedding in walls.
        
        Args:
            dx: X direction (-1, 0, or 1)
            dy: Y direction (-1, 0, or 1)
            speed: Number of pixels to move
        
        Returns:
            True if collision occurred, False otherwise
        """
        new_x, new_y = int(self.x), int(self.y)
        
        for i in range(speed):
            new_x, new_y = new_x + dx, new_y + dy
            
            # Check level boundaries
            if new_x < 70 or new_x > 730:
                return True
            
            # Check block collisions based on movement direction
            if ((dy > 0 and new_y % GRID_BLOCK_SIZE == 0 or
                 dx > 0 and new_x % GRID_BLOCK_SIZE == 0 or
                 dx < 0 and new_x % GRID_BLOCK_SIZE == GRID_BLOCK_SIZE - 1)
                and block(new_x, new_y, self.game.grid)):
                return True
            
            self.pos = new_x, new_y
        
        return False


class GravityActor(CollideActor):
    """
    Actor with gravity physics.
    
    Extends CollideActor to add falling behavior with landing detection.
    Used for Player, Robots, and Fruits.
    """
    
    MAX_FALL_SPEED = 10
    
    def __init__(self, pos, game):
        """
        Initialize a GravityActor.
        
        Args:
            pos: Initial (x, y) position
            game: Reference to the Game instance
        """
        super().__init__(pos, game, ANCHOR_CENTRE_BOTTOM)
        self.vel_y = 0
        self.landed = False
    
    def update(self, detect=True):
        """
        Apply gravity and handle falling/landing.
        
        Args:
            detect: If True, check for block collisions while falling.
                   Set to False when player is dying to fall through.
        """
        # Apply gravity
        self.vel_y = min(self.vel_y + 1, GravityActor.MAX_FALL_SPEED)
        
        if detect:
            if self.move(0, sign(self.vel_y), abs(self.vel_y)):
                # Landed on a block
                self.vel_y = 0
                self.landed = True
            
            if self.top >= HEIGHT:
                # Fell off bottom - reappear at top
                self.y = 1
        else:
            # No collision detection - just fall
            self.y += self.vel_y


class Orb(CollideActor):
    """
    Player's bubble projectile.
    
    Orbs are blown horizontally, then float upward.
    They can trap enemies and pop after a timer expires.
    """
    
    MAX_TIMER = 250
    
    def __init__(self, pos, dir_x, game):
        """
        Initialize an Orb.
        
        Args:
            pos: Initial (x, y) position
            dir_x: Direction (-1 for left, 1 for right)
            game: Reference to the Game instance
        """
        super().__init__(pos, game)
        self.direction_x = dir_x
        self.floating = False
        self.trapped_enemy_type = None
        self.timer = -1
        self.blown_frames = 6
    
    def hit_test(self, bolt):
        """
        Check for collision with a bolt.
        
        Args:
            bolt: Bolt object to check collision with
        
        Returns:
            True if collision occurred
        """
        collided = self.collidepoint(bolt.pos)
        if collided:
            self.timer = Orb.MAX_TIMER - 1
        return collided
    
    def update(self):
        """Update orb position and state."""
        self.timer += 1
        
        if self.floating:
            # Float upwards with slight randomness
            self.move(0, -1, randint(1, 2))
        else:
            # Move horizontally
            if self.move(self.direction_x, 0, 4):
                self.floating = True
        
        if self.timer == self.blown_frames:
            self.floating = True
        elif self.timer >= Orb.MAX_TIMER or self.y <= -40:
            # Pop the orb
            self.game.pops.append(Pop(self.pos, 1, self.game))
            if self.trapped_enemy_type is not None:
                self.game.fruits.append(Fruit(self.pos, self.game, self.trapped_enemy_type))
            self.game.play_sound("pop", 4)
        
        # Update sprite image
        if self.timer < 9:
            self.image = "orb" + str(self.timer // 3)
        else:
            if self.trapped_enemy_type is not None:
                self.image = "trap" + str(self.trapped_enemy_type) + str((self.timer // 4) % 8)
            else:
                self.image = "orb" + str(3 + (((self.timer - 9) // 8) % 4))


class Bolt(CollideActor):
    """
    Enemy laser projectile.
    
    Bolts travel horizontally and can damage the player or pop orbs.
    """
    
    SPEED = 7
    
    def __init__(self, pos, dir_x, game):
        """
        Initialize a Bolt.
        
        Args:
            pos: Initial (x, y) position
            dir_x: Direction (-1 for left, 1 for right)
            game: Reference to the Game instance
        """
        super().__init__(pos, game)
        self.direction_x = dir_x
        self.active = True
    
    def update(self):
        """Update bolt position and check collisions."""
        if self.move(self.direction_x, 0, Bolt.SPEED):
            self.active = False
        else:
            # Check collision with orbs and player
            for obj in self.game.orbs + [self.game.player]:
                if obj and obj.hit_test(self):
                    self.active = False
                    break
        
        # Update sprite image
        direction_idx = "1" if self.direction_x > 0 else "0"
        anim_frame = str((self.game.timer // 4) % 2)
        self.image = "bolt" + direction_idx + anim_frame


class Pop(Actor):
    """
    Pop animation effect.
    
    Displayed when orbs burst or fruits are collected.
    """
    
    def __init__(self, pos, pop_type, game):
        """
        Initialize a Pop animation.
        
        Args:
            pos: Position (x, y)
            pop_type: Animation type (0 or 1)
            game: Reference to the Game instance
        """
        super().__init__("blank", pos)
        self.type = pop_type
        self.timer = -1
        self.game = game
    
    def update(self):
        """Update pop animation frame."""
        self.timer += 1
        self.image = "pop" + str(self.type) + str(self.timer // 2)


class Fruit(GravityActor):
    """
    Collectible pickup.
    
    Can be regular fruit (score), extra health, or extra life.
    """
    
    # Fruit types
    APPLE = 0
    RASPBERRY = 1
    LEMON = 2
    EXTRA_HEALTH = 3
    EXTRA_LIFE = 4
    
    def __init__(self, pos, game, trapped_enemy_type=0):
        """
        Initialize a Fruit.
        
        Args:
            pos: Position (x, y)
            game: Reference to the Game instance
            trapped_enemy_type: Type of enemy that spawned this fruit
        """
        super().__init__(pos, game)
        
        # Determine fruit type based on enemy type
        if trapped_enemy_type == Robot.TYPE_NORMAL:
            self.type = choice([Fruit.APPLE, Fruit.RASPBERRY, Fruit.LEMON])
        else:
            # Aggressive enemies can drop power-ups
            types = 10 * [Fruit.APPLE, Fruit.RASPBERRY, Fruit.LEMON]
            types += 9 * [Fruit.EXTRA_HEALTH]
            types += [Fruit.EXTRA_LIFE]
            self.type = choice(types)
        
        self.time_to_live = 500
    
    def update(self):
        """Update fruit position and check for player collection."""
        super().update()
        
        if self.game.player and self.game.player.collidepoint(self.center):
            if self.type == Fruit.EXTRA_HEALTH:
                self.game.player.health = min(3, self.game.player.health + 1)
                self.game.play_sound("bonus")
            elif self.type == Fruit.EXTRA_LIFE:
                self.game.player.lives += 1
                self.game.play_sound("bonus")
            else:
                self.game.player.score += (self.type + 1) * 100
                self.game.play_sound("score")
            self.time_to_live = 0
        else:
            self.time_to_live -= 1
        
        if self.time_to_live <= 0:
            self.game.pops.append(Pop((self.x, self.y - 27), 0, self.game))
        
        # Update sprite animation
        anim_frame = str([0, 1, 2, 1][(self.game.timer // 6) % 4])
        self.image = "fruit" + str(self.type) + anim_frame


class Player(GravityActor):
    """
    The player character.
    
    Can move, jump, and fire orbs to trap enemies.
    """
    
    def __init__(self, game):
        """
        Initialize the Player.
        
        Args:
            game: Reference to the Game instance (can be None initially)
        """
        super().__init__((0, 0), game)
        self.lives = 2
        self.score = 0
    
    def reset(self):
        """Reset player state for a new level or respawn."""
        self.pos = (WIDTH / 2, 100)
        self.vel_y = 0
        self.direction_x = 1
        self.fire_timer = 0
        self.hurt_timer = 100  # Invulnerability frames
        self.health = 3
        self.blowing_orb = None
    
    def hit_test(self, bolt):
        """
        Check for collision with a bolt.
        
        Args:
            bolt: Bolt object to check collision with
        
        Returns:
            True if hit and damaged
        """
        if self.collidepoint(bolt.pos) and self.hurt_timer < 0:
            self.hurt_timer = 200
            self.health -= 1
            self.vel_y = -12
            self.landed = False
            self.direction_x = bolt.direction_x
            
            if self.health > 0:
                self.game.play_sound("ouch", 4)
            else:
                self.game.play_sound("die")
            return True
        return False
    
    def update(self, input_state):
        """
        Update player state based on input.
        
        Args:
            input_state: InputState object with current input
        """
        # Apply gravity (no collision detection if dead)
        super().update(self.health > 0)
        
        self.fire_timer -= 1
        self.hurt_timer -= 1
        
        if self.landed:
            self.hurt_timer = min(self.hurt_timer, 100)
        
        # Track movement direction for sprite selection
        dx = 0
        
        if self.hurt_timer > 100:
            # Being knocked back or dying
            if self.health > 0:
                self.move(self.direction_x, 0, 4)
            else:
                if self.top >= HEIGHT * 1.5:
                    self.lives -= 1
                    self.reset()
        else:
            # Normal movement
            if input_state.left:
                dx = -1
            elif input_state.right:
                dx = 1
            
            if dx != 0:
                self.direction_x = dx
                if self.fire_timer < 10:
                    self.move(dx, 0, 4)
            
            # Fire orb
            if input_state.fire_pressed and self.fire_timer <= 0 and len(self.game.orbs) < 5:
                x = min(730, max(70, self.x + self.direction_x * 38))
                y = self.y - 35
                self.blowing_orb = Orb((x, y), self.direction_x, self.game)
                self.game.orbs.append(self.blowing_orb)
                self.game.play_sound("blow", 4)
                self.fire_timer = 20
            
            # Jump
            if input_state.up and self.vel_y == 0 and self.landed:
                self.vel_y = -16
                self.landed = False
                self.game.play_sound("jump")
        
        # Continue blowing orb while holding fire
        if input_state.fire_held:
            if self.blowing_orb:
                self.blowing_orb.blown_frames += 4
                if self.blowing_orb.blown_frames >= 120:
                    self.blowing_orb = None
        else:
            self.blowing_orb = None
        
        # Update sprite image
        self.image = "blank"
        if self.hurt_timer <= 0 or self.hurt_timer % 2 == 1:
            dir_index = "1" if self.direction_x > 0 else "0"
            if self.hurt_timer > 100:
                if self.health > 0:
                    self.image = "recoil" + dir_index
                else:
                    self.image = "fall" + str((self.game.timer // 4) % 2)
            elif self.fire_timer > 0:
                self.image = "blow" + dir_index
            elif dx == 0:
                self.image = "still"
            else:
                self.image = "run" + dir_index + str((self.game.timer // 8) % 4)


class Robot(GravityActor):
    """
    Enemy robot.
    
    Moves around the level and fires bolts at the player.
    Can be trapped in orbs.
    """
    
    TYPE_NORMAL = 0
    TYPE_AGGRESSIVE = 1
    
    def __init__(self, pos, robot_type, game):
        """
        Initialize a Robot.
        
        Args:
            pos: Position (x, y)
            robot_type: TYPE_NORMAL or TYPE_AGGRESSIVE
            game: Reference to the Game instance
        """
        super().__init__(pos, game)
        self.type = robot_type
        self.speed = randint(1, 3)
        self.direction_x = 1
        self.alive = True
        self.change_dir_timer = 0
        self.fire_timer = 100
    
    def update(self):
        """Update robot movement and firing behavior."""
        super().update()
        
        self.change_dir_timer -= 1
        self.fire_timer += 1
        
        # Move and turn on wall collision
        if self.move(self.direction_x, 0, self.speed):
            self.change_dir_timer = 0
        
        # Randomly change direction, biased toward player
        if self.change_dir_timer <= 0:
            directions = [-1, 1]
            if self.game.player:
                directions.append(sign(self.game.player.x - self.x))
            self.direction_x = choice(directions)
            self.change_dir_timer = randint(100, 250)
        
        # Aggressive robots target orbs
        if self.type == Robot.TYPE_AGGRESSIVE and self.fire_timer >= 24:
            for orb in self.game.orbs:
                if orb.y >= self.top and orb.y < self.bottom and abs(orb.x - self.x) < 200:
                    self.direction_x = sign(orb.x - self.x)
                    self.fire_timer = 0
                    break
        
        # Fire at player
        if self.fire_timer >= 12:
            fire_probability = self.game.fire_probability()
            if self.game.player and self.top < self.game.player.bottom and self.bottom > self.game.player.top:
                fire_probability *= 10
            if random() < fire_probability:
                self.fire_timer = 0
                self.game.play_sound("laser", 4)
        elif self.fire_timer == 8:
            self.game.bolts.append(Bolt((self.x + self.direction_x * 20, self.y - 38), 
                                        self.direction_x, self.game))
        
        # Check for orb collision
        for orb in self.game.orbs:
            if orb.trapped_enemy_type is None and self.collidepoint(orb.center):
                self.alive = False
                orb.floating = True
                orb.trapped_enemy_type = self.type
                self.game.play_sound("trap", 4)
                break
        
        # Update sprite image
        direction_idx = "1" if self.direction_x > 0 else "0"
        image = "robot" + str(self.type) + direction_idx
        if self.fire_timer < 12:
            image += str(5 + (self.fire_timer // 4))
        else:
            image += str(1 + ((self.game.timer // 4) % 4))
        self.image = image
