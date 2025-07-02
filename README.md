# इंडिग्राम (Indigram) - Social Network BFS Visualization

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://python.org)
[![Pygame](https://img.shields.io/badge/Pygame-2.0%2B-green.svg)](https://pygame.org)

**Indigram** is an interactive social network visualization tool that demonstrates the **Breadth-First Search (BFS)** algorithm in action. Built with Python and Pygame, it creates a beautiful, educational visualization of how social networks connect people and how the BFS algorithm finds the shortest path between any two users.

## Features

### Interactive BFS Visualization
- **Step-by-step BFS exploration**: Watch the algorithm explore nodes level by level
- **Color-coded states**: 
  - Yellow: Currently exploring nodes
  - Blue: Already visited nodes  
  - Gold: Final shortest path
- **Vanishing animation**: Non-path nodes disappear with sparkle effects after BFS completion
- **Real-time progress indicator**: Shows current BFS level and progress percentage

### Realistic Social Network
- **300 Indian users** with authentic Indian names
- **Diverse connectivity patterns**: 4 regions with different connection densities
- **Guaranteed path diversity**: Ensures 1-4 degrees of separation between users
- **Smart grid layout**: Optimal node distribution across the screen

### Interactive Controls
- **Click-to-explore**: Select start and target users with mouse clicks
- **Random demo mode**: Automatically selects random user pairs
- **Real-time path finding**: Instant BFS visualization between any two users
- **Multiple UI controls**: Buttons and keyboard shortcuts

### Modern UI/UX
- **Fullscreen support**: F11 toggle and resizable windows
- **Indian-themed design**: Saffron color scheme inspired by Indian culture
- **Comprehensive information panel**: Shows network statistics, user details, and path information
- **Smooth animations**: Pulse effects, ripples, and gradient backgrounds
- **Responsive design**: Adapts to different screen sizes

## Installation Guide

### Prerequisites
- **Python 3.7 or higher**
- **pip** (Python package installer)

### Step 1: Clone or Download
```bash
# Option 1: If you have the files
cd /path/to/indigram

# Option 2: Or download the files to a new directory
mkdir indigram
cd indigram
# Copy social_network_bfs.py to this directory
```

### Step 2: Install Dependencies
```bash
# Install pygame
pip install pygame

# Or if you use conda
conda install pygame
```

### Step 3: Run the Application
```bash
python social_network_bfs.py
```

### Alternative Installation (Virtual Environment)
```bash
# Create virtual environment
python -m venv indigram_env

# Activate virtual environment
# On Linux/Mac:
source indigram_env/bin/activate
# On Windows:
# indigram_env\Scripts\activate

# Install dependencies
pip install pygame

# Run the application
python social_network_bfs.py
```

## How to Use

### Basic Usage
1. **Launch the application**: Run `python social_network_bfs.py`
2. **Select start user**: Click on any user node (turns red)
3. **Select target user**: Click on another user node (turns green)
4. **Watch BFS in action**: The algorithm will automatically visualize the shortest path

### Controls

#### Mouse Controls
- **Left Click on user**: Select start point, then target point
- **Left Click on buttons**: Use panel buttons for various actions

#### Keyboard Shortcuts
- **R**: Reset current selection
- **Space**: Random demo (selects random start and target)
- **F11**: Toggle fullscreen mode
- **ESC**: Exit application

#### Panel Buttons
- **Reset**: Clear current selection
- **Random Demo**: Automatically select random users
- **Regenerate Network**: Create a new random network
- **Toggle Fullscreen**: Switch between windowed and fullscreen
- **Exit Indigram**: Close the application

## How It Works

### The BFS Algorithm
**Breadth-First Search (BFS)** is a graph traversal algorithm that explores nodes level by level, guaranteeing the shortest path in unweighted graphs.

#### Algorithm Steps:
1. **Initialize**: Start with the source node in a queue
2. **Explore Level**: Process all nodes at current distance
3. **Mark Visited**: Track explored nodes to avoid cycles
4. **Expand**: Add unvisited neighbors to queue
5. **Repeat**: Continue until target is found or queue is empty

#### Visualization Process:
1. **Yellow Phase**: Shows nodes currently being explored
2. **Blue Phase**: Shows nodes that have been visited
3. **Vanishing Phase**: Non-path nodes disappear with effects
4. **Gold Phase**: Final shortest path highlighted

### Network Generation
The social network is designed to create realistic connection patterns:

- **Dense Region** (Top-left): Highly connected users (1-2 degrees separation)
- **Medium Region** (Center): Moderately connected users (2-3 degrees)
- **Sparse Region** (Outer areas): Lightly connected users (3-4 degrees)
- **Isolated Region** (Edges): Minimally connected users (4+ degrees)

## Technical Specifications

### Performance
- **Network Size**: 300 users with ~2,000 total connections
- **Frame Rate**: 60 FPS smooth animations
- **Memory Usage**: Approximately 50-100 MB
- **Algorithm Complexity**: O(V + E) where V = vertices, E = edges

### Compatibility
- **Operating Systems**: Windows, macOS, Linux
- **Python Versions**: 3.7, 3.8, 3.9, 3.10, 3.11, 3.12
- **Screen Resolutions**: Automatically adapts to screen size
- **Display Modes**: Windowed and fullscreen support

### Dependencies
```
pygame >= 2.0.0
```

## Visual Features

### Color Scheme
- **Background**: Deep space gradient (Indian night sky inspired)
- **Primary**: Saffron orange (Indian flag color)
- **Users**: Various states with appropriate colors
- **Connections**: Subtle gray with golden highlights for paths
- **UI**: Modern dark theme with colorful accents

### Animations
- **Pulse Effects**: Selected and target users pulse gently
- **Ripple Effects**: Exploring nodes show expanding ripples
- **Sparkle Effects**: Vanishing nodes create sparkle animations
- **Gradient Backgrounds**: Smooth color transitions
- **Curved Connections**: Aesthetic curved lines between users

## Educational Value

### Computer Science Concepts
- **Graph Theory**: Understanding social networks as graphs
- **BFS Algorithm**: Visual demonstration of breadth-first search
- **Shortest Path**: Finding optimal connections between people
- **Network Analysis**: Understanding connectivity patterns
- **Algorithm Visualization**: Step-by-step algorithm execution

### Real-World Applications
- **Social Media**: How platforms suggest connections
- **Navigation Systems**: Finding shortest routes
- **Network Analysis**: Understanding information spread
- **Six Degrees of Separation**: Visualizing small-world phenomena

## Troubleshooting

### Common Issues

#### 1. "pygame not found" Error
```bash
# Solution: Install pygame
pip install pygame
```

#### 2. Performance Issues
- Close other applications to free memory
- Reduce window size if running slowly
- Ensure graphics drivers are updated

#### 3. Display Issues
- Try toggling fullscreen mode (F11)
- Resize window manually
- Check display settings

#### 4. Python Version Issues
```bash
# Check Python version
python --version

# Should be 3.7 or higher
```

### Getting Help
- Check that all dependencies are installed correctly
- Ensure you're running Python 3.7+
- Try running in a virtual environment
- Restart the application if it becomes unresponsive

## 🎓 Learning Resources

### Understanding BFS
- [Breadth-First Search - Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search)
- [Graph Algorithms Visualization](https://visualgo.net/en/graphds)

### Social Network Theory
- [Six Degrees of Separation](https://en.wikipedia.org/wiki/Six_degrees_of_separation)
- [Small World Networks](https://en.wikipedia.org/wiki/Small-world_network)

### Pygame Development
- [Pygame Documentation](https://www.pygame.org/docs/)
- [Python Game Development](https://realpython.com/pygame-a-primer/)

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 🙏 Acknowledgments

- **Indian Culture**: Color scheme and naming inspired by Indian heritage
- **Pygame Community**: For the excellent game development framework
- **Graph Theory**: Built on fundamental computer science concepts
- **Educational Purpose**: Designed to make algorithms accessible and visual

---

**Made with ❤️ for education and exploration of computer science concepts**

*🇮🇳 इंडिग्राम - Connecting minds through algorithms*
