from gradio_client import Client, file

# Initialize Pygame
pygame.init()

# Set up display dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Custom Writing System Converter")

# Define node patterns for each letter
node_patterns = {
    'A': [(0, 0), (0, 50), (50, 0)],
    'S': [(0, 25), (25, 0), (50, 25), (25, 50)],
    # Define patterns for other letters
}

def get_nodes_for_text(text):
    nodes_list = []
    for char in text:
        char_upper = char.upper()
        if char_upper in node_patterns:
            nodes_list.append(node_patterns[char_upper])
    return nodes_list

def draw_nodes_and_connections_with_breaks(nodes_list):
    for nodes in nodes_list:
        for i in range(len(nodes) - 1):
            pygame.draw.line(screen, (0, 0, 0), nodes[i], nodes[i+1], 2)
            
            # Draw breaks
            if i > 0:
                midpoint = ((nodes[i][0] + nodes[i-1][0]) // 2, (nodes[i][1] + nodes[i-1][1]) // 2)
                pygame.draw.line(screen, (0, 0, 0), midpoint, (midpoint[0] + 10, midpoint[1]), 2)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    text = "AS"  # Your input text
    nodes_list = get_nodes_for_text(text)
    
    screen.fill((255, 255, 255))  # Clear the screen
    draw_nodes_and_connections_with_breaks(nodes_list)  # Draw nodes, connections, and breaks
    
    pygame.display.update()
