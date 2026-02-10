# Cavern - Game Logic
# Core game state and update logic

from random import randint, shuffle

from constants import (
    WIDTH, HEIGHT, NUM_ROWS, NUM_COLUMNS,
    LEVEL_X_OFFSET, GRID_BLOCK_SIZE, LEVELS
)
from actors import Robot, Fruit, Pop


class Game:
    """
    Core game state and logic.
    
    Manages the level grid, all game entities, and game progression.
    This class is owned by screen objects, not global scope.
    """
    
    def __init__(self, player=None):
        """
        Initialize a new game.
        
        Args:
            player: Player object to use, or None for menu background
        """
        self.player = player
        self.level_colour = -1
        self.level = -1
        
        # Entity lists
        self.fruits = []
        self.bolts = []
        self.enemies = []
        self.pops = []
        self.orbs = []
        self.pending_enemies = []
        self.grid = []
        self.timer = -1
        
        self.next_level()
    
    def fire_probability(self):
        """
        Calculate the probability of robots firing each frame.
        
        Returns:
            Float probability (increases with level)
        """
        return 0.001 + (0.0001 * min(100, self.level))
    
    def max_enemies(self):
        """
        Calculate maximum enemies on screen at once.
        
        Returns:
            Integer max enemies (increases with level)
        """
        return min((self.level + 6) // 2, 8)
    
    def next_level(self):
        """Advance to the next level."""
        self.level_colour = (self.level_colour + 1) % 4
        self.level += 1
        
        # Set up grid (copy to avoid modifying LEVELS)
        self.grid = LEVELS[self.level % len(LEVELS)] + [LEVELS[self.level % len(LEVELS)][0]]
        
        self.timer = -1
        
        if self.player:
            self.player.reset()
        
        # Clear all entities
        self.fruits = []
        self.bolts = []
        self.enemies = []
        self.pops = []
        self.orbs = []
        
        # Create pending enemies list
        num_enemies = 10 + self.level
        num_strong_enemies = 1 + int(self.level / 1.5)
        num_weak_enemies = num_enemies - num_strong_enemies
        
        self.pending_enemies = (num_strong_enemies * [Robot.TYPE_AGGRESSIVE] + 
                               num_weak_enemies * [Robot.TYPE_NORMAL])
        shuffle(self.pending_enemies)
        
        self.play_sound("level", 1)
    
    def get_robot_spawn_x(self):
        """
        Find a spawn location for a robot.
        
        Returns:
            X coordinate for spawning
        """
        r = randint(0, NUM_COLUMNS - 1)
        
        for i in range(NUM_COLUMNS):
            grid_x = (r + i) % NUM_COLUMNS
            if self.grid[0][grid_x] == ' ':
                return GRID_BLOCK_SIZE * grid_x + LEVEL_X_OFFSET + 12
        
        return WIDTH / 2
    
    def update(self, input_state):
        """
        Update all game entities.
        
        Args:
            input_state: InputState object (can be None for menu background)
        """
        self.timer += 1
        
        # Update all entities
        for fruit in self.fruits:
            fruit.update()
        
        for bolt in self.bolts:
            bolt.update()
        
        for enemy in self.enemies:
            enemy.update()
        
        for pop in self.pops:
            pop.update()
        
        for orb in self.orbs:
            orb.update()
        
        if self.player and input_state:
            self.player.update(input_state)
        
        # Remove dead entities
        self.fruits = [f for f in self.fruits if f.time_to_live > 0]
        self.bolts = [b for b in self.bolts if b.active]
        self.enemies = [e for e in self.enemies if e.alive]
        self.pops = [p for p in self.pops if p.timer < 12]
        self.orbs = [o for o in self.orbs if o.timer < 250 and o.y > -40]
        
        # Spawn random fruit
        if self.timer % 100 == 0 and len(self.pending_enemies + self.enemies) > 0:
            self.fruits.append(Fruit((randint(70, 730), randint(75, 400)), self))
        
        # Spawn enemies
        if (self.timer % 81 == 0 and 
            len(self.pending_enemies) > 0 and 
            len(self.enemies) < self.max_enemies()):
            robot_type = self.pending_enemies.pop()
            pos = (self.get_robot_spawn_x(), -30)
            self.enemies.append(Robot(pos, robot_type, self))
        
        # Check for level complete
        if len(self.pending_enemies + self.fruits + self.enemies + self.pops) == 0:
            if len([orb for orb in self.orbs if orb.trapped_enemy_type is not None]) == 0:
                self.next_level()
    
    def draw(self, screen):
        """
        Draw the game state.
        
        Args:
            screen: Pygame Zero screen object
        """
        # Draw background
        screen.blit("bg%d" % self.level_colour, (0, 0))
        
        # Draw blocks
        block_sprite = "block" + str(self.level % 4)
        for row_y in range(NUM_ROWS):
            row = self.grid[row_y]
            if len(row) > 0:
                x = LEVEL_X_OFFSET
                for block_char in row:
                    if block_char != ' ':
                        screen.blit(block_sprite, (x, row_y * GRID_BLOCK_SIZE))
                    x += GRID_BLOCK_SIZE
        
        # Draw all entities
        all_objs = self.fruits + self.bolts + self.enemies + self.pops + self.orbs
        if self.player:
            all_objs.append(self.player)
        
        for obj in all_objs:
            obj.draw()
    
    def play_sound(self, name, count=1):
        """
        Play a sound effect.
        
        Args:
            name: Base name of the sound file
            count: Number of variants to randomly choose from
        """
        if self.player:
            try:
                # Access sounds through pgzero's builtins
                from pgzero import loaders
                sounds = loaders.sounds
                sound = getattr(sounds, name + str(randint(0, count - 1)))
                sound.play()
            except Exception as e:
                print(f"Sound error: {e}")
