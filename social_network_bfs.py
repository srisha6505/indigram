import pygame
import math
import random
import time
from collections import deque, defaultdict
from dataclasses import dataclass
from typing import List, Dict, Set, Optional, Tuple

# Initialize Pygame
pygame.init()

# Get screen dimensions for fullscreen support
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

# Constants - Use fullscreen dimensions
WIDTH = SCREEN_WIDTH
HEIGHT = SCREEN_HEIGHT
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Indigram - Indian Social Network Visualization")

# Colors - Modern and vibrant Indian-inspired
BACKGROUND = (8, 10, 20)
USER_COLOR = (255, 140, 0)  # Saffron
SELECTED_USER = (255, 50, 50)  # Bright red
TARGET_USER = (50, 255, 100)  # Green
CONNECTION_COLOR = (40, 40, 60)
PATH_COLOR = (255, 215, 0)  # Gold
HIGHLIGHT_PATH = (255, 20, 147)  # Deep pink
TEXT_COLOR = (255, 255, 255)
PANEL_COLOR = (20, 25, 35)
BUTTON_COLOR = (138, 43, 226)  # Blue violet
BUTTON_HOVER = (75, 0, 130)  # Indigo
EXIT_BUTTON_COLOR = (220, 20, 60)  # Crimson
EXIT_BUTTON_HOVER = (255, 69, 0)  # Red orange

# Fonts
FONT_SMALL = pygame.font.Font(None, 16)
FONT_MEDIUM = pygame.font.Font(None, 20)
FONT_LARGE = pygame.font.Font(None, 28)
FONT_TITLE = pygame.font.Font(None, 36)

@dataclass
class User:
    id: int
    name: str
    x: float
    y: float
    connections: Set[int]
    color: Tuple[int, int, int] = USER_COLOR
    radius: int = 8
    is_selected: bool = False
    is_target: bool = False
    pulse_phase: float = 0.0
    
    def __post_init__(self):
        self.connections = set()
        
    def add_connection(self, user_id: int):
        self.connections.add(user_id)
    
    def distance_to(self, other_x: float, other_y: float) -> float:
        return math.sqrt((self.x - other_x) ** 2 + (self.y - other_y) ** 2)
    
    def update_animation(self, dt: float):
        self.pulse_phase += dt * 3
        if self.pulse_phase > 2 * math.pi:
            self.pulse_phase = 0

class SocialNetwork:
    def __init__(self, num_users: int = 300):
        self.users: Dict[int, User] = {}
        self.connections: Dict[int, Set[int]] = defaultdict(set)
        self.selected_user: Optional[int] = None
        self.target_user: Optional[int] = None
        self.current_path: List[int] = []
        self.bfs_animation: List[List[int]] = []
        self.animation_step = 0
        self.animation_speed = 0.3  # Slower for better visibility
        self.last_animation_time = 0
        self.path_found = False
        self.degrees_of_separation = 0
        
        # BFS visualization states
        self.bfs_visited_nodes: Set[int] = set()
        self.current_exploring_nodes: Set[int] = set()
        self.is_animating_bfs = False
        self.bfs_complete = False
        self.vanishing_nodes: Dict[int, float] = {}  # node_id: vanish_start_time
        self.vanish_delay = 1.0  # Delay before starting vanish animation
        self.vanish_duration = 2.0  # Duration of vanish animation
        self.show_final_path_time = 0
        
        self.generate_network(num_users)
        
    def generate_network(self, num_users: int):
        """Generate a realistic social network with small-world properties and diverse separation degrees"""
        # Extended list of Indian names for more users
        indian_names = [
            "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Reyansh", "Muhammad", "Sai", "Krishna", "Atharv",
            "Ishaan", "Shaurya", "Dhruv", "Aryan", "Yuvraj", "Harsh", "Dev", "Arnav", "Shivansh", "Kartik",
            "Ananya", "Fatima", "Aadhya", "Diya", "Saanvi", "Myra", "Sara", "Aanya", "Pari", "Kavya",
            "Priya", "Shreya", "Kiara", "Arya", "Riya", "Tara", "Zara", "Avni", "Ira", "Mahira",
            "Rohan", "Ayaan", "Karan", "Kabir", "Om", "Ritik", "Tanishq", "Rudra", "Riaan", "Arman",
            "Nisha", "Meera", "Rahul", "Vikram", "Amit", "Suresh", "Rajesh", "Neha", "Pooja", "Sunita",
            "Aditi", "Sita", "Geeta", "Maya", "Kiran", "Ravi", "Ajay", "Vijay", "Sanjay", "Deepak",
            "Kavita", "Mala", "Lata", "Rekha", "Shanti", "Gouri", "Kamala", "Radha", "Lakshmi", "Durga",
            "Ganesh", "Shiva", "Rama", "Hanuman", "Bharath", "Ashwin", "Varun", "Surya", "Chandra", "Indra",
            "Anjali", "Divya", "Sonal", "Preeti", "Vandana", "Monika", "Rashmi", "Swati", "Pallavi", "Madhuri",
            "Akash", "Nikhil", "Tarun", "Manish", "Sachin", "Rohit", "Abhishek", "Vishal", "Sandeep", "Manoj",
            "Sneha", "Manisha", "Shweta", "Jyoti", "Smita", "Renu", "Deepika", "Karishma", "Sapna", "Nidhi",
            "Raman", "Prakash", "Mahesh", "Dinesh", "Naresh", "Mukesh", "Ramesh", "Yogesh", "Rajesh", "Sunil",
            "Sonia", "Meena", "Kiran", "Usha", "Poonam", "Neeta", "Seema", "Geeta", "Rita", "Anita",
            "Gaurav", "Sourav", "Ashish", "Nitish", "Harish", "Girish", "Jagdish", "Umesh", "Lokesh", "Rakesh",
            "Kavitha", "Sangita", "Sunitha", "Mamta", "Pushpa", "Sharda", "Leela", "Veena", "Geetha", "Sita"
        ]
        
        # Create a large grid layout for better spread
        grid_cols = int(math.sqrt(num_users)) + 2
        grid_rows = int(math.ceil(num_users / grid_cols))
        
        # Calculate spacing with panel width consideration
        panel_width = 450  # Increased panel width
        usable_width = WIDTH - panel_width - 200  # Leave margins
        usable_height = HEIGHT - 200  # Leave top/bottom margins
        
        cell_width = usable_width / grid_cols
        cell_height = usable_height / grid_rows
        
        # Define regions for different connection densities (to create diverse degrees of separation)
        regions = {
            'dense': [],      # Highly connected (1-2 degrees)
            'medium': [],     # Medium connected (2-3 degrees)
            'sparse': [],     # Lightly connected (3-4 degrees)
            'isolated': []    # Very few connections (4+ degrees)
        }
        
        user_id = 0
        for row in range(grid_rows):
            for col in range(grid_cols):
                if user_id >= num_users:
                    break
                
                # Calculate base position in grid
                base_x = 100 + col * cell_width + cell_width / 2
                base_y = 100 + row * cell_height + cell_height / 2
                
                # Add randomization within cell for natural look
                x = base_x + random.uniform(-cell_width * 0.3, cell_width * 0.3)
                y = base_y + random.uniform(-cell_height * 0.3, cell_height * 0.3)
                
                # Ensure bounds
                x = max(80, min(usable_width + 80, x))
                y = max(80, min(HEIGHT - 80, y))
                
                # Get Indian name
                if user_id < len(indian_names):
                    name = indian_names[user_id]
                else:
                    base_name = random.choice(indian_names)
                    name = f"{base_name}{user_id - len(indian_names) + 1}"
                
                user = User(user_id, name, x, y, set())
                user.radius = random.randint(8, 12)
                self.users[user_id] = user
                
                # Assign users to regions based on position for diverse connectivity
                if row < grid_rows * 0.3 and col < grid_cols * 0.3:
                    regions['dense'].append(user_id)
                elif row < grid_rows * 0.6 and col < grid_cols * 0.6:
                    regions['medium'].append(user_id)
                elif row < grid_rows * 0.8 and col < grid_cols * 0.8:
                    regions['sparse'].append(user_id)
                else:
                    regions['isolated'].append(user_id)
                
                user_id += 1
        
        # Create connections based on regions to ensure diverse degrees of separation
        self.create_diverse_connections(regions)
    
    def create_diverse_connections(self, regions: Dict[str, List[int]]):
        """Create connections to ensure diverse degrees of separation (1-4)"""
        
        # Dense region: High connectivity (1-2 degrees of separation)
        for user_id in regions['dense']:
            user = self.users[user_id]
            # Connect to many nearby users and some random ones
            distances = []
            for other_id, other_user in self.users.items():
                if other_id != user_id:
                    dist = user.distance_to(other_user.x, other_user.y)
                    distances.append((dist, other_id))
            
            distances.sort()
            # High connectivity: 8-15 connections
            num_connections = random.randint(8, 15)
            for _, neighbor_id in distances[:num_connections]:
                self.add_connection(user_id, neighbor_id)
            
            # Add random long-range connections within dense region
            for _ in range(random.randint(3, 6)):
                if regions['dense']:
                    random_user = random.choice(regions['dense'])
                    if random_user != user_id and random_user not in user.connections:
                        self.add_connection(user_id, random_user)
        
        # Medium region: Medium connectivity (2-3 degrees of separation)
        for user_id in regions['medium']:
            user = self.users[user_id]
            distances = []
            for other_id, other_user in self.users.items():
                if other_id != user_id:
                    dist = user.distance_to(other_user.x, other_user.y)
                    distances.append((dist, other_id))
            
            distances.sort()
            # Medium connectivity: 5-10 connections
            num_connections = random.randint(5, 10)
            for _, neighbor_id in distances[:num_connections]:
                self.add_connection(user_id, neighbor_id)
            
            # Some connections to dense region
            if random.random() < 0.6 and regions['dense']:
                random_dense = random.choice(regions['dense'])
                if random_dense not in user.connections:
                    self.add_connection(user_id, random_dense)
        
        # Sparse region: Low connectivity (3-4 degrees of separation)
        for user_id in regions['sparse']:
            user = self.users[user_id]
            distances = []
            for other_id, other_user in self.users.items():
                if other_id != user_id:
                    dist = user.distance_to(other_user.x, other_user.y)
                    distances.append((dist, other_id))
            
            distances.sort()
            # Low connectivity: 3-6 connections
            num_connections = random.randint(3, 6)
            for _, neighbor_id in distances[:num_connections]:
                self.add_connection(user_id, neighbor_id)
            
            # Occasional bridge to medium region
            if random.random() < 0.4 and regions['medium']:
                random_medium = random.choice(regions['medium'])
                if random_medium not in user.connections:
                    self.add_connection(user_id, random_medium)
        
        # Isolated region: Very low connectivity (4+ degrees of separation)
        for user_id in regions['isolated']:
            user = self.users[user_id]
            distances = []
            for other_id, other_user in self.users.items():
                if other_id != user_id:
                    dist = user.distance_to(other_user.x, other_user.y)
                    distances.append((dist, other_id))
            
            distances.sort()
            # Very low connectivity: 1-4 connections
            num_connections = random.randint(1, 4)
            for _, neighbor_id in distances[:num_connections]:
                self.add_connection(user_id, neighbor_id)
            
            # Rare bridge to sparse region
            if random.random() < 0.3 and regions['sparse']:
                random_sparse = random.choice(regions['sparse'])
                if random_sparse not in user.connections:
                    self.add_connection(user_id, random_sparse)
        
        # Add some cross-region bridges to ensure connectivity
        self.add_cross_region_bridges(regions)
    
    def add_cross_region_bridges(self, regions: Dict[str, List[int]]):
        """Add strategic bridges between regions to ensure network connectivity"""
        region_pairs = [
            ('dense', 'medium', 0.7),    # 70% chance
            ('medium', 'sparse', 0.5),   # 50% chance  
            ('sparse', 'isolated', 0.3), # 30% chance
            ('dense', 'sparse', 0.2),    # 20% chance (long bridge)
            ('medium', 'isolated', 0.1)  # 10% chance (very long bridge)
        ]
        
        for region1, region2, probability in region_pairs:
            if regions[region1] and regions[region2]:
                # Add multiple bridges based on region sizes
                num_bridges = max(1, min(len(regions[region1]), len(regions[region2])) // 10)
                
                for _ in range(num_bridges):
                    if random.random() < probability:
                        user1 = random.choice(regions[region1])
                        user2 = random.choice(regions[region2])
                        if user2 not in self.users[user1].connections:
                            self.add_connection(user1, user2)
    
    def add_connection(self, user1_id: int, user2_id: int):
        """Add bidirectional connection between two users"""
        self.users[user1_id].add_connection(user2_id)
        self.users[user2_id].add_connection(user1_id)
        self.connections[user1_id].add(user2_id)
        self.connections[user2_id].add(user1_id)
    
    def bfs_shortest_path(self, start_id: int, target_id: int) -> Tuple[List[int], List[List[int]]]:
        """Find shortest path using BFS and return path + animation steps with detailed exploration"""
        if start_id == target_id:
            return [start_id], [[start_id]]
        
        queue = deque([(start_id, [start_id])])
        visited = {start_id}
        animation_steps = []
        
        # Add start node as first step
        animation_steps.append([start_id])
        
        while queue:
            current_level_nodes = []
            next_queue = deque()
            
            # Process all nodes at current level
            while queue:
                current_id, path = queue.popleft()
                
                # Explore all neighbors of current node
                for neighbor_id in self.users[current_id].connections:
                    if neighbor_id not in visited:
                        new_path = path + [neighbor_id]
                        current_level_nodes.append(neighbor_id)
                        visited.add(neighbor_id)
                        
                        if neighbor_id == target_id:
                            # Target found! Add this level and return
                            animation_steps.append(current_level_nodes)
                            return new_path, animation_steps
                        
                        next_queue.append((neighbor_id, new_path))
            
            # Add current level to animation if we explored any nodes
            if current_level_nodes:
                animation_steps.append(current_level_nodes[:])
            
            queue = next_queue
        
        return [], animation_steps  # No path found
    
    def start_bfs_animation(self):
        """Start BFS animation between selected users"""
        if self.selected_user is not None and self.target_user is not None:
            # Reset animation state
            self.bfs_visited_nodes.clear()
            self.current_exploring_nodes.clear()
            self.vanishing_nodes.clear()
            self.is_animating_bfs = True
            self.bfs_complete = False
            self.show_final_path_time = 0
            
            self.current_path, self.bfs_animation = self.bfs_shortest_path(
                self.selected_user, self.target_user
            )
            self.animation_step = 0
            self.last_animation_time = time.time()
            self.path_found = len(self.current_path) > 0
            self.degrees_of_separation = len(self.current_path) - 1 if self.path_found else -1
    
    def update_animation(self, current_time: float):
        """Update BFS animation with enhanced visualization"""
        if not self.is_animating_bfs or not self.bfs_animation:
            return
            
        # Check if we should advance to next animation step
        if (self.animation_step < len(self.bfs_animation) and
            current_time - self.last_animation_time > self.animation_speed):
            
            # Add current level nodes to exploring set
            current_level = self.bfs_animation[self.animation_step]
            for node_id in current_level:
                self.current_exploring_nodes.add(node_id)
                self.bfs_visited_nodes.add(node_id)
            
            self.animation_step += 1
            self.last_animation_time = current_time
            
            # Check if BFS animation is complete
            if self.animation_step >= len(self.bfs_animation):
                self.bfs_complete = True
                self.show_final_path_time = current_time
                
                if self.path_found:
                    # Start vanishing animation after delay
                    vanish_start_time = current_time + self.vanish_delay
                    
                    # Schedule vanishing for all visited nodes except the path
                    for node_id in self.bfs_visited_nodes:
                        if node_id not in self.current_path:
                            # Add staggered delay based on distance from start
                            start_node = self.users[self.selected_user]
                            node = self.users[node_id]
                            distance = start_node.distance_to(node.x, node.y)
                            stagger_delay = (distance / 1000) * 0.5  # Max 0.5s stagger
                            self.vanishing_nodes[node_id] = vanish_start_time + stagger_delay
        
        # Update vanishing animation
        if self.vanishing_nodes:
            nodes_to_remove = []
            for node_id, vanish_start in self.vanishing_nodes.items():
                if current_time >= vanish_start + self.vanish_duration:
                    # Node has finished vanishing
                    nodes_to_remove.append(node_id)
                    self.bfs_visited_nodes.discard(node_id)
                    self.current_exploring_nodes.discard(node_id)
            
            for node_id in nodes_to_remove:
                del self.vanishing_nodes[node_id]
            
            # Check if all nodes have vanished
            if not self.vanishing_nodes and self.bfs_complete:
                self.is_animating_bfs = False
    
    def get_user_at_position(self, x: float, y: float) -> Optional[int]:
        """Find user at given position"""
        for user_id, user in self.users.items():
            if user.distance_to(x, y) <= user.radius + 5:
                return user_id
        return None
    
    def select_user(self, user_id: int):
        """Select a user as start point"""
        # Reset previous selections
        for user in self.users.values():
            user.is_selected = False
            user.is_target = False
            
        self.selected_user = user_id
        self.users[user_id].is_selected = True
        self.target_user = None
        self.current_path = []
        self.bfs_animation = []
        self.animation_step = 0
        self.path_found = False
    
    def select_target(self, user_id: int):
        """Select a user as target point"""
        if self.selected_user is not None and user_id != self.selected_user:
            # Reset previous target
            for user in self.users.values():
                user.is_target = False
                
            self.target_user = user_id
            self.users[user_id].is_target = True
            self.start_bfs_animation()
    
    def reset_selection(self):
        """Reset all selections"""
        for user in self.users.values():
            user.is_selected = False
            user.is_target = False
        self.selected_user = None
        self.target_user = None
        self.current_path = []
        self.bfs_animation = []
        self.animation_step = 0
        self.path_found = False
        
        # Reset BFS visualization state
        self.bfs_visited_nodes.clear()
        self.current_exploring_nodes.clear()
        self.vanishing_nodes.clear()
        self.is_animating_bfs = False
        self.bfs_complete = False
        self.show_final_path_time = 0

class UI:
    def __init__(self):
        self.panel_width = 450  # Increased for larger screens
        self.panel_rect = pygame.Rect(WIDTH - self.panel_width, 0, self.panel_width, HEIGHT)
        
        # Buttons with better spacing for larger screens
        button_width = 160
        button_height = 50
        button_margin = 20
        
        self.reset_button = pygame.Rect(WIDTH - self.panel_width + 20, HEIGHT - 140, button_width, button_height)
        self.random_button = pygame.Rect(WIDTH - self.panel_width + 200, HEIGHT - 140, button_width, button_height)
        self.regenerate_button = pygame.Rect(WIDTH - self.panel_width + 20, HEIGHT - 200, button_width * 2 + button_margin, button_height)
        self.exit_button = pygame.Rect(WIDTH - self.panel_width + 20, HEIGHT - 80, button_width * 2 + button_margin, button_height)
        self.fullscreen_button = pygame.Rect(WIDTH - self.panel_width + 20, HEIGHT - 260, button_width * 2 + button_margin, button_height)
        
        self.mouse_over_reset = False
        self.mouse_over_random = False
        self.mouse_over_exit = False
        self.mouse_over_regenerate = False
        self.mouse_over_fullscreen = False
    
    def handle_mouse_hover(self, mouse_pos: Tuple[int, int]):
        """Handle mouse hover effects"""
        self.mouse_over_reset = self.reset_button.collidepoint(mouse_pos)
        self.mouse_over_random = self.random_button.collidepoint(mouse_pos)
        self.mouse_over_exit = self.exit_button.collidepoint(mouse_pos)
        self.mouse_over_regenerate = self.regenerate_button.collidepoint(mouse_pos)
        self.mouse_over_fullscreen = self.fullscreen_button.collidepoint(mouse_pos)
    
    def draw_panel(self, win: pygame.Surface, network: SocialNetwork):
        """Draw the information panel"""
        # Panel background with gradient effect
        pygame.draw.rect(win, PANEL_COLOR, self.panel_rect)
        pygame.draw.rect(win, (40, 45, 60), self.panel_rect, 3)
        
        # Add decorative border
        pygame.draw.line(win, (255, 140, 0), (WIDTH - self.panel_width, 0), 
                        (WIDTH - self.panel_width, HEIGHT), 4)
        
        y_offset = 30
        
        # Title with Indian flag colors accent
        title = FONT_TITLE.render("इंडिग्राम", True, (255, 140, 0))
        win.blit(title, (WIDTH - self.panel_width + 30, y_offset))
        y_offset += 35
        
        subtitle = FONT_MEDIUM.render("Indigram - Social Network BFS", True, TEXT_COLOR)
        win.blit(subtitle, (WIDTH - self.panel_width + 30, y_offset))
        y_offset += 50
        
        # Instructions with better formatting
        instructions = [
            "🎯 Instructions:",
            "• Click a user to select start point",
            "• Click another user to find path",
            "• Watch BFS algorithm visualize",
            "• Yellow: Currently exploring",
            "• Blue: Already visited",
            "• Gold: Final path",
            "• Use buttons below for actions",
            "",
            "📊 Network Statistics:",
            f"• कुल उपयोगकर्ता: {len(network.users)}",
            f"• Total Connections: {sum(len(connections) for connections in network.connections.values()) // 2}",
            f"• Average Connections: {sum(len(connections) for connections in network.connections.values()) // len(network.users):.1f}",
            "",
            "🎮 Keyboard Shortcuts:",
            "• R: Reset selection",
            "• Space: Random demo",
            "• F11: Toggle fullscreen",
            "• ESC: Exit",
            "",
        ]
        
        for instruction in instructions:
            if instruction.startswith("🎯") or instruction.startswith("📊"):
                text = FONT_MEDIUM.render(instruction, True, (255, 215, 0))
            elif instruction.startswith("•"):
                text = FONT_SMALL.render(instruction, True, (220, 220, 220))
            else:
                text = FONT_SMALL.render(instruction, True, TEXT_COLOR)
            win.blit(text, (WIDTH - self.panel_width + 30, y_offset))
            y_offset += 22
        
        # Current selection info with enhanced styling
        if network.selected_user is not None:
            user = network.users[network.selected_user]
            
            # Selected user box
            info_rect = pygame.Rect(WIDTH - self.panel_width + 20, y_offset - 5, self.panel_width - 40, 90)
            pygame.draw.rect(win, (40, 20, 60), info_rect)
            pygame.draw.rect(win, SELECTED_USER, info_rect, 2)
            
            text = FONT_MEDIUM.render("🎯 Selected User:", True, SELECTED_USER)
            win.blit(text, (WIDTH - self.panel_width + 25, y_offset))
            y_offset += 25
            
            text = FONT_SMALL.render(f"• नाम: {user.name}", True, TEXT_COLOR)
            win.blit(text, (WIDTH - self.panel_width + 25, y_offset))
            y_offset += 18
            
            text = FONT_SMALL.render(f"• ID: {user.id}", True, TEXT_COLOR)
            win.blit(text, (WIDTH - self.panel_width + 25, y_offset))
            y_offset += 18
            
            text = FONT_SMALL.render(f"• Connections: {len(user.connections)}", True, TEXT_COLOR)
            win.blit(text, (WIDTH - self.panel_width + 25, y_offset))
            y_offset += 25
        
        # Path information with enhanced styling
        if network.target_user is not None:
            target_user = network.users[network.target_user]
            
            # Target user box
            info_rect = pygame.Rect(WIDTH - self.panel_width + 20, y_offset - 5, self.panel_width - 40, 90)
            pygame.draw.rect(win, (20, 40, 20), info_rect)
            pygame.draw.rect(win, TARGET_USER, info_rect, 2)
            
            text = FONT_MEDIUM.render("🎯 Target User:", True, TARGET_USER)
            win.blit(text, (WIDTH - self.panel_width + 25, y_offset))
            y_offset += 25
            
            text = FONT_SMALL.render(f"• नाम: {target_user.name}", True, TEXT_COLOR)
            win.blit(text, (WIDTH - self.panel_width + 25, y_offset))
            y_offset += 20
            
            if network.path_found:
                # Success box
                success_rect = pygame.Rect(WIDTH - self.panel_width + 20, y_offset - 5, self.panel_width - 40, 120)
                pygame.draw.rect(win, (20, 40, 20), success_rect)
                pygame.draw.rect(win, PATH_COLOR, success_rect, 2)
                
                text = FONT_MEDIUM.render("✅ Path Found!", True, PATH_COLOR)
                win.blit(text, (WIDTH - self.panel_width + 25, y_offset))
                y_offset += 25
                
                text = FONT_SMALL.render(f"🔗 Degrees of Separation: {network.degrees_of_separation}", True, (255, 215, 0))
                win.blit(text, (WIDTH - self.panel_width + 25, y_offset))
                y_offset += 20
                
                text = FONT_SMALL.render(f"📏 Path Length: {len(network.current_path)} users", True, TEXT_COLOR)
                win.blit(text, (WIDTH - self.panel_width + 25, y_offset))
                y_offset += 20
                
                # BFS Animation Status
                if network.is_animating_bfs:
                    if not network.bfs_complete:
                        status_text = f"🔍 Exploring Level {network.animation_step}/{len(network.bfs_animation)}"
                        text = FONT_SMALL.render(status_text, True, (255, 255, 0))
                    else:
                        if network.vanishing_nodes:
                            status_text = f"✨ Nodes vanishing... ({len(network.vanishing_nodes)} left)"
                            text = FONT_SMALL.render(status_text, True, (255, 150, 255))
                        else:
                            status_text = "🎉 BFS Complete!"
                            text = FONT_SMALL.render(status_text, True, (100, 255, 100))
                    win.blit(text, (WIDTH - self.panel_width + 25, y_offset))
                    y_offset += 20
                
                # Show path
                if len(network.current_path) <= 8:  # Only show if path is not too long
                    text = FONT_SMALL.render("🛤️ Path:", True, (255, 255, 100))
                    win.blit(text, (WIDTH - self.panel_width + 25, y_offset))
                    y_offset += 18
                    
                    for i, user_id in enumerate(network.current_path):
                        user_name = network.users[user_id].name
                        if len(user_name) > 12:
                            user_name = user_name[:12] + "..."
                        connector = " → " if i < len(network.current_path) - 1 else ""
                        text = FONT_SMALL.render(f"{user_name}{connector}", True, PATH_COLOR)
                        win.blit(text, (WIDTH - self.panel_width + 25, y_offset))
                        y_offset += 16
                y_offset += 10
            elif network.degrees_of_separation == -1:
                # Error box
                error_rect = pygame.Rect(WIDTH - self.panel_width + 20, y_offset - 5, self.panel_width - 40, 40)
                pygame.draw.rect(win, (40, 20, 20), error_rect)
                pygame.draw.rect(win, (255, 100, 100), error_rect, 2)
                
                text = FONT_MEDIUM.render("❌ No Path Found!", True, (255, 100, 100))
                win.blit(text, (WIDTH - self.panel_width + 25, y_offset))
                y_offset += 40
        
        # Buttons with enhanced styling
        reset_color = BUTTON_HOVER if self.mouse_over_reset else BUTTON_COLOR
        random_color = BUTTON_HOVER if self.mouse_over_random else BUTTON_COLOR
        exit_color = EXIT_BUTTON_HOVER if self.mouse_over_exit else EXIT_BUTTON_COLOR
        regenerate_color = BUTTON_HOVER if self.mouse_over_regenerate else BUTTON_COLOR
        fullscreen_color = BUTTON_HOVER if self.mouse_over_fullscreen else BUTTON_COLOR
        
        # Fullscreen Toggle button
        pygame.draw.rect(win, fullscreen_color, self.fullscreen_button, border_radius=8)
        pygame.draw.rect(win, TEXT_COLOR, self.fullscreen_button, 3, border_radius=8)
        fullscreen_text = FONT_MEDIUM.render("🖥️ Toggle Fullscreen (F11)", True, TEXT_COLOR)
        fullscreen_rect = fullscreen_text.get_rect(center=self.fullscreen_button.center)
        win.blit(fullscreen_text, fullscreen_rect)
        
        # Regenerate Network button
        pygame.draw.rect(win, regenerate_color, self.regenerate_button, border_radius=8)
        pygame.draw.rect(win, TEXT_COLOR, self.regenerate_button, 3, border_radius=8)
        regenerate_text = FONT_MEDIUM.render("🔄 Regenerate Network", True, TEXT_COLOR)
        regenerate_rect = regenerate_text.get_rect(center=self.regenerate_button.center)
        win.blit(regenerate_text, regenerate_rect)
        
        # Reset button
        pygame.draw.rect(win, reset_color, self.reset_button, border_radius=8)
        pygame.draw.rect(win, TEXT_COLOR, self.reset_button, 3, border_radius=8)
        reset_text = FONT_MEDIUM.render("🔄 Reset", True, TEXT_COLOR)
        reset_rect = reset_text.get_rect(center=self.reset_button.center)
        win.blit(reset_text, reset_rect)
        
        # Random Demo button
        pygame.draw.rect(win, random_color, self.random_button, border_radius=8)
        pygame.draw.rect(win, TEXT_COLOR, self.random_button, 3, border_radius=8)
        random_text = FONT_MEDIUM.render("🎲 Random Demo", True, TEXT_COLOR)
        random_rect = random_text.get_rect(center=self.random_button.center)
        win.blit(random_text, random_rect)
        
        # Exit button
        pygame.draw.rect(win, exit_color, self.exit_button, border_radius=8)
        pygame.draw.rect(win, TEXT_COLOR, self.exit_button, 3, border_radius=8)
        exit_text = FONT_MEDIUM.render("🚪 Exit Indigram", True, TEXT_COLOR)
        exit_rect = exit_text.get_rect(center=self.exit_button.center)
        win.blit(exit_text, exit_rect)

def draw_network(win: pygame.Surface, network: SocialNetwork, current_time: float):
    """Draw the entire social network with enhanced BFS visualization"""
    # Create gradient background
    for y in range(0, HEIGHT, 4):
        gradient_color = (
            int(8 + (y / HEIGHT) * 12),
            int(10 + (y / HEIGHT) * 15),
            int(20 + (y / HEIGHT) * 25)
        )
        pygame.draw.rect(win, gradient_color, (0, y, WIDTH, 4))
    
    # Draw connections first (so they appear behind users)
    for user_id, user in network.users.items():
        for connected_id in user.connections:
            if user_id < connected_id:  # Draw each connection only once
                connected_user = network.users[connected_id]
                
                # Determine connection color and style
                color = CONNECTION_COLOR
                width = 2
                
                # Highlight path connections with animated effect
                if (network.current_path and 
                    user_id in network.current_path and 
                    connected_id in network.current_path):
                    
                    user_index = network.current_path.index(user_id)
                    connected_index = network.current_path.index(connected_id)
                    
                    if abs(user_index - connected_index) == 1:
                        # Animated path connection
                        pulse = math.sin(current_time * 3) * 0.3 + 0.7
                        color = tuple(int(c * pulse) for c in HIGHLIGHT_PATH)
                        width = 4
                
                # Dim connections to vanishing nodes
                user_vanishing = user_id in network.vanishing_nodes
                connected_vanishing = connected_id in network.vanishing_nodes
                
                if user_vanishing or connected_vanishing:
                    vanish_progress = 0
                    if user_vanishing:
                        vanish_start = network.vanishing_nodes[user_id]
                        vanish_progress = max(vanish_progress, 
                            min(1.0, (current_time - vanish_start) / network.vanish_duration))
                    if connected_vanishing:
                        vanish_start = network.vanishing_nodes[connected_id]
                        vanish_progress = max(vanish_progress,
                            min(1.0, (current_time - vanish_start) / network.vanish_duration))
                    
                    # Fade out the connection
                    alpha = 1.0 - vanish_progress
                    color = tuple(int(c * alpha) for c in color)
                    width = max(1, int(width * alpha))
                
                # Draw connection with slight curve for better visual appeal
                start_pos = (user.x, user.y)
                end_pos = (connected_user.x, connected_user.y)
                
                # Calculate control point for curve
                curve_offset = 10 if width > 2 else 5
                
                # Simple curved line approximation using multiple segments
                segments = 8
                for i in range(segments):
                    t1 = i / segments
                    t2 = (i + 1) / segments
                    
                    x1 = user.x * (1-t1) + connected_user.x * t1
                    y1 = user.y * (1-t1) + connected_user.y * t1 + math.sin(t1 * math.pi) * curve_offset
                    
                    x2 = user.x * (1-t2) + connected_user.x * t2
                    y2 = user.y * (1-t2) + connected_user.y * t2 + math.sin(t2 * math.pi) * curve_offset
                    
                    if width > 0:
                        pygame.draw.line(win, color, (x1, y1), (x2, y2), width)
    
    # Draw users with enhanced styling and BFS visualization
    for user in network.users.values():
        user.update_animation(current_time)
        
        # Determine user color and size
        color = USER_COLOR
        radius = user.radius
        alpha = 1.0
        
        # Check if node is vanishing
        if user.id in network.vanishing_nodes:
            vanish_start = network.vanishing_nodes[user.id]
            if current_time >= vanish_start:
                vanish_progress = min(1.0, (current_time - vanish_start) / network.vanish_duration)
                alpha = 1.0 - vanish_progress
                
                # Add sparkle effect during vanishing
                if vanish_progress < 0.8:
                    sparkle_radius = int(radius * (1 + vanish_progress * 2))
                    sparkle_alpha = int(100 * (1 - vanish_progress))
                    for i in range(8):
                        angle = (i / 8) * 2 * math.pi + current_time * 5
                        sparkle_x = user.x + math.cos(angle) * sparkle_radius
                        sparkle_y = user.y + math.sin(angle) * sparkle_radius
                        sparkle_color = (*PATH_COLOR, sparkle_alpha)
                        s = pygame.Surface((6, 6), pygame.SRCALPHA)
                        pygame.draw.circle(s, sparkle_color, (3, 3), 3)
                        win.blit(s, (sparkle_x - 3, sparkle_y - 3))
        
        # Skip drawing if completely vanished
        if alpha <= 0:
            continue
        
        # BFS visualization states
        if user.is_selected:
            color = SELECTED_USER
            # Pulsing effect
            pulse = math.sin(user.pulse_phase) * 0.4 + 1.2
            radius = int(user.radius * pulse)
            
        elif user.is_target:
            color = TARGET_USER
            # Pulsing effect
            pulse = math.sin(user.pulse_phase) * 0.4 + 1.2
            radius = int(user.radius * pulse)
            
        elif user.id in network.current_exploring_nodes and network.is_animating_bfs:
            # Currently being explored by BFS
            color = (255, 255, 0)  # Yellow for active exploration
            pulse = math.sin(current_time * 8) * 0.3 + 1.1
            radius = int(user.radius * pulse)
            
            # Add exploration ripple effect
            ripple_radius = int(radius + (math.sin(current_time * 6) * 10 + 10))
            ripple_alpha = int(50 * (1 + math.sin(current_time * 6)) / 2)
            ripple_color = (*color, ripple_alpha)
            s = pygame.Surface((ripple_radius * 2, ripple_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, ripple_color, (ripple_radius, ripple_radius), ripple_radius, 3)
            win.blit(s, (user.x - ripple_radius, user.y - ripple_radius))
            
        elif user.id in network.bfs_visited_nodes and network.is_animating_bfs:
            # Already visited by BFS
            color = (100, 200, 255)  # Light blue for visited
            radius = user.radius + 2
            
        elif (network.current_path and user.id in network.current_path and 
              network.bfs_complete):
            # Final path node
            color = PATH_COLOR
            radius = user.radius + 3
            
            # Subtle glow for path users
            for glow_radius in range(radius + 8, radius, -2):
                glow_alpha = max(0, int(30 * alpha) - (glow_radius - radius) * 4)
                glow_color = (*PATH_COLOR, glow_alpha)
                s = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, glow_color, (glow_radius, glow_radius), glow_radius)
                win.blit(s, (user.x - glow_radius, user.y - glow_radius))
        
        # Apply alpha for vanishing effect
        if alpha < 1.0:
            color = tuple(int(c * alpha) for c in color)
        
        # Draw glow effect for special users
        if user.is_selected or user.is_target:
            for glow_radius in range(radius + 15, radius, -3):
                glow_alpha = max(0, int(50 * alpha) - (glow_radius - radius) * 3)
                glow_color = (*color, glow_alpha)
                s = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, glow_color, (glow_radius, glow_radius), glow_radius)
                win.blit(s, (user.x - glow_radius, user.y - glow_radius))
        
        # Draw user circle with gradient effect
        pygame.draw.circle(win, color, (int(user.x), int(user.y)), radius)
        
        # Add inner highlight
        highlight_color = tuple(min(255, int(c + 50 * alpha)) for c in color)
        pygame.draw.circle(win, highlight_color, (int(user.x - 2), int(user.y - 2)), max(1, radius - 3))
        
        # Draw border
        border_color = tuple(int(c * alpha) for c in TEXT_COLOR)
        pygame.draw.circle(win, border_color, (int(user.x), int(user.y)), radius, 2)
        
        # Draw user name for selected/target users with better styling
        if (user.is_selected or user.is_target) and alpha > 0.5:
            # Background for text
            text = FONT_SMALL.render(user.name, True, TEXT_COLOR)
            text_rect = text.get_rect(center=(user.x, user.y - radius - 20))
            
            # Draw text background
            bg_rect = text_rect.inflate(8, 4)
            bg_color = tuple(int(c * alpha) for c in (0, 0, 0)) + (int(180 * alpha),)
            s = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
            pygame.draw.rect(s, bg_color, (0, 0, bg_rect.width, bg_rect.height), border_radius=4)
            pygame.draw.rect(s, tuple(int(c * alpha) for c in color), 
                           (0, 0, bg_rect.width, bg_rect.height), 2, border_radius=4)
            win.blit(s, bg_rect.topleft)
            
            # Draw text with alpha
            text_color = tuple(int(c * alpha) for c in TEXT_COLOR)
            text_surface = FONT_SMALL.render(user.name, True, text_color)
            win.blit(text_surface, text_rect)
    
    # Draw BFS progress indicator
    if network.is_animating_bfs and network.bfs_animation:
        progress = network.animation_step / len(network.bfs_animation)
        progress_text = f"BFS Progress: {int(progress * 100)}% (Level {network.animation_step}/{len(network.bfs_animation)})"
        
        text_surface = FONT_MEDIUM.render(progress_text, True, (255, 255, 0))
        text_rect = text_surface.get_rect()
        text_rect.centerx = WIDTH // 4
        text_rect.y = 30
        
        # Background for progress text
        bg_rect = text_rect.inflate(20, 10)
        pygame.draw.rect(win, (0, 0, 0, 150), bg_rect, border_radius=5)
        pygame.draw.rect(win, (255, 255, 0), bg_rect, 2, border_radius=5)
        
        win.blit(text_surface, text_rect)

def main():
    try:
        clock = pygame.time.Clock()
        network = SocialNetwork(300)
        ui = UI()
        running = True
        is_fullscreen = False
        
        print("🇮🇳 इंडिग्राम - Indigram Social Network Visualization")
        print("Click on users to explore their connections using BFS algorithm!")
        print(f"Generated network with {len(network.users)} users")
        print("Controls:")
        print("- Left click: Select start user, then target user")
        print("- R key: Reset selection")
        print("- Space key: Random demo")
        print("- F11: Toggle fullscreen")
        print("- Use buttons in panel for actions")
        print("- Click 'Exit Indigram' button to quit")
    except Exception as e:
        print(f"Error initializing: {e}")
        return
    
    def toggle_fullscreen():
        nonlocal is_fullscreen, ui, network
        global WIN, WIDTH, HEIGHT
        
        is_fullscreen = not is_fullscreen
        
        if is_fullscreen:
            WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            WIDTH = WIN.get_width()
            HEIGHT = WIN.get_height()
        else:
            info = pygame.display.Info()
            WIDTH = min(1600, info.current_w - 100)
            HEIGHT = min(1000, info.current_h - 100)
            WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        
        # Recreate UI with new dimensions
        ui = UI()
        # Regenerate network positions for new screen size
        network = SocialNetwork(len(network.users))
        print(f"Screen mode: {'Fullscreen' if is_fullscreen else 'Windowed'} ({WIDTH}x{HEIGHT})")
    
    while running:
        try:
            current_time = time.time()
            mouse_pos = pygame.mouse.get_pos()
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Don't quit on window close, only on exit button
                    pass
                
                elif event.type == pygame.VIDEORESIZE:
                    if not is_fullscreen:
                        global WIDTH, HEIGHT, WIN
                        WIDTH, HEIGHT = event.w, event.h
                        WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                        ui = UI()
                        network = SocialNetwork(len(network.users))
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        if ui.reset_button.collidepoint(mouse_pos):
                            network.reset_selection()
                            print("Selection reset")
                        elif ui.random_button.collidepoint(mouse_pos):
                            # Random demo - select two random users
                            user_ids = list(network.users.keys())
                            start_id = random.choice(user_ids)
                            network.select_user(start_id)
                            
                            # Select target that's not the same as start
                            target_id = random.choice([uid for uid in user_ids if uid != start_id])
                            network.select_target(target_id)
                            print(f"Random demo: {network.users[start_id].name} → {network.users[target_id].name}")
                            if network.path_found:
                                print(f"Degrees of separation: {network.degrees_of_separation}")
                        elif ui.exit_button.collidepoint(mouse_pos):
                            print("Indigram exited by user")
                            running = False
                        elif ui.regenerate_button.collidepoint(mouse_pos):
                            print("Regenerating network...")
                            network = SocialNetwork(300)
                            print(f"New network generated with {len(network.users)} users")
                        elif ui.fullscreen_button.collidepoint(mouse_pos):
                            toggle_fullscreen()
                        else:
                            # Check if clicking on a user
                            clicked_user = network.get_user_at_position(mouse_pos[0], mouse_pos[1])
                            if clicked_user is not None and mouse_pos[0] < WIDTH - ui.panel_width:
                                if network.selected_user is None:
                                    network.select_user(clicked_user)
                                    print(f"Selected start user: {network.users[clicked_user].name}")
                                else:
                                    network.select_target(clicked_user)
                                    if network.path_found:
                                        print(f"Path found! Degrees of separation: {network.degrees_of_separation}")
                                    else:
                                        print("No path found between selected users")
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        network.reset_selection()
                        print("Selection reset")
                    elif event.key == pygame.K_SPACE:
                        # Random demo
                        user_ids = list(network.users.keys())
                        start_id = random.choice(user_ids)
                        network.select_user(start_id)
                        
                        target_id = random.choice([uid for uid in user_ids if uid != start_id])
                        network.select_target(target_id)
                        print(f"Random demo: {network.users[start_id].name} → {network.users[target_id].name}")
                        if network.path_found:
                            print(f"Degrees of separation: {network.degrees_of_separation}")
                    elif event.key == pygame.K_F11:
                        toggle_fullscreen()
                    elif event.key == pygame.K_ESCAPE:
                        print("Indigram exited with ESC key")
                        running = False
            
            # Update
            ui.handle_mouse_hover(mouse_pos)
            network.update_animation(current_time)
            
            # Draw
            draw_network(WIN, network, current_time)
            ui.draw_panel(WIN, network)
            
            pygame.display.flip()
            clock.tick(60)
        except Exception as e:
            print(f"Error in main loop: {e}")
            break
    
    pygame.quit()
    print("🇮🇳 इंडिग्राम समाप्त - Indigram visualization ended.")

if __name__ == "__main__":
    main()
