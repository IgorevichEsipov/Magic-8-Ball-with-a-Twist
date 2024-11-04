import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Set up display with larger dimensions
width, height = 1000, 1000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Magic 8-Ball")

# Responses
positive_responses = [
    "Yes", "Definitely", "Absolutely", "Maybe", "It is certain",
    "Yes, in due time", "Yes, definitely"
]

mean_responses = [
    "You’ve got a better chance of winning the lottery.",
    "Wow, really? Just... no.",
    "Not even in a million years.",
    "How about a nice, big 'NOPE'?",
    "I'd say yes, but that'd be a total lie.",
    "You must be joking. Not a chance.",
    "Please, as if that’s going to happen.",
    "Are you dreaming? Because that’s the only place this is real.",
    "You'd have to be incredibly lucky. Spoiler: you’re not.",
    "Yeah, no. Try again in another life.",
    "Don't hold your breath on that one.",
    "You actually think that’s possible? Hilarious.",
    "Asking me again won’t change reality.",
    "Here’s an idea: stop asking dumb questions.",
    "Sure, and pigs might fly while they're at it.",
    "Absolutely… not.",
    "Let’s not kid ourselves here. It’s a solid no.",
    "Ha! Good one. Next question?",
    "Right. And I’m the Queen of England."
]

# Font setup with larger sizes
font = pygame.font.Font(None, 36)
mode_font = pygame.font.Font(None, 34)

# Game state
honest_mode = False  # Start in "Nice" mode

def draw_background():
    """Draws a gradient background with noise."""
    for y in range(height):
        # Create a gradient from light blue to darker blue with subtle noise
        color_value = 135 + (70 * y) // height
        color = (color_value, color_value + 50, 235)
        noisy_color = tuple(min(255, max(0, c + random.randint(-10, 10))) for c in color)
        pygame.draw.line(screen, noisy_color, (0, y), (width, y))

def draw_8ball(offset=(0, 0)):
    # Draw textured background
    draw_background()

    # Draw the black "ball" with a subtle blue radial gradient for texture
    center_x = width // 2 + offset[0]
    center_y = height // 2 + offset[1]
    radius = 300

    for i in range(radius, 0, -1):
        # Create a blue gradient effect
        color_intensity = max(0, 30 + int((radius - i) * 1.1))  # Base intensity
        blue_value = min(color_intensity, 255)  # Ensure blue value is within range
        color = (0, 0, blue_value)  # Set to a blue gradient

        # Draw the circle with the calculated color
        pygame.draw.circle(screen, color, (center_x, center_y), i)

    # Draw the blue triangle in the center
    triangle_color = (0, 0, 255)  # Blue color
    triangle_size = 140

    # Calculate the points of an equilateral triangle
    point1 = (center_x, center_y - triangle_size)
    point2 = (center_x - triangle_size * math.sin(math.radians(60)), center_y + triangle_size // 2)
    point3 = (center_x + triangle_size * math.sin(math.radians(60)), center_y + triangle_size // 2)
    pygame.draw.polygon(screen, triangle_color, [point1, point2, point3])


def shake_ball():
    shake_offsets = [(-20, -5), (20, 5), (-20, -5), (20, 5), (0, 0)]
    for offset in shake_offsets:
        draw_8ball(offset)
        pygame.display.flip()
        pygame.time.delay(50)

def display_response(response, mode_text):
    shake_ball()  # Perform the shake animation before showing the response
    draw_8ball()  # Draw the 8-ball background in the final position

    # Display the response text centered within the blue triangle
    text = font.render(response, True, (255, 255, 255))  # White text color
    text_rect = text.get_rect(center=(width // 2, height // 2))
    screen.blit(text, text_rect)

    # Display the current mode at the top
    mode_display = mode_font.render(f"Mode: {mode_text}", True, (0, 0, 0))
    mode_rect = mode_display.get_rect(center=(width // 2, 50))
    screen.blit(mode_display, mode_rect)

    pygame.display.flip()

def main():
    global honest_mode
    response = ""
    mode_text = "Nice"  # Default mode text

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Toggle between "Nice" and "Honest" modes
                    honest_mode = not honest_mode
                    mode_text = "Honest" if honest_mode else "Nice"
                    print(f"{mode_text} mode activated.")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    # Generate a response based on the mode
                    if honest_mode:
                        response = random.choice(mean_responses)
                    else:
                        response = random.choice(positive_responses)
                    display_response(response, mode_text)

        # Draw the 8-ball background with the current mode text (initial state)
        if not response:
            draw_8ball()
            # Display mode text at the top
            mode_display = mode_font.render(f"Mode: {mode_text}", True, (0, 0, 0))
            mode_rect = mode_display.get_rect(center=(width // 2, 50))
            screen.blit(mode_display, mode_rect)
            pygame.display.flip()

if __name__ == "__main__":
    main()
