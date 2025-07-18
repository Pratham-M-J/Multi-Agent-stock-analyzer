import cv2
import mediapipe as mp
import pygame
import random
import sys

# Game parameters
WIDTH, HEIGHT = 640, 480
GRAVITY = 0.6
FLAP_STRENGTH = -10
PIPE_WIDTH = 60
PIPE_GAP = 250        
PIPE_SPEED = 4
SPAWN_EVENT = pygame.USEREVENT + 1
SPAWN_MS = 2000       

# Mediapipe Pose setup
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.7)
cap = cv2.VideoCapture(0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

class Bird:
    def __init__(self):
        self.x = WIDTH // 4
        self.y = HEIGHT // 2
        self.vel = 0
        self.w = self.h = 32
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
    def update(self, flap):
        self.vel += GRAVITY
        if flap:
            self.vel = FLAP_STRENGTH
        self.y += self.vel
        self.rect.y = int(self.y)
    def draw(self, surf):
        pygame.draw.rect(surf, (255, 220, 0), self.rect)

class Pipe:
    def __init__(self):
        self.x = WIDTH
        gap_y = random.randint(100, HEIGHT - 100)
        self.top = pygame.Rect(self.x, 0, PIPE_WIDTH, gap_y - PIPE_GAP // 2)
        self.bot = pygame.Rect(self.x, gap_y + PIPE_GAP // 2,
                               PIPE_WIDTH, HEIGHT - (gap_y + PIPE_GAP // 2))
    def update(self):
        self.x -= PIPE_SPEED
        self.top.x = self.bot.x = self.x
    def off_screen(self):
        return self.x + PIPE_WIDTH < 0
    def draw(self, surf):
        pygame.draw.rect(surf, (0, 200, 0), self.top)
        pygame.draw.rect(surf, (0, 200, 0), self.bot)

def get_both_hands_flap():
    """
    Returns True only if both wrists move up quickly at the same time.
    Uses y-speed of left (15) and right (16) wrists from Mediapipe Pose.
    """
    global prev_lw_y, prev_rw_y, flap_cooldown
    ret, frame = cap.read()
    if not ret:
        return False
    frame_flipped = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame_flipped, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)
    flap = False
    if results.pose_landmarks:
        lm = results.pose_landmarks.landmark
        h, w, _ = frame_flipped.shape

        lw = lm[15]  # left wrist
        rw = lm[16]  # right wrist
        lw_y = int(lw.y * h)
        rw_y = int(rw.y * h)

        # Show wrists
        cv2.circle(frame_flipped, (int(lw.x*w), lw_y), 12, (0,255,0), -1)
        cv2.circle(frame_flipped, (int(rw.x*w), rw_y), 12, (0,255,0), -1)

        # Calculate velocities
        lv = lw_y - prev_lw_y if prev_lw_y is not None else 0
        rv = rw_y - prev_rw_y if prev_rw_y is not None else 0

   
        if (prev_lw_y is not None and prev_rw_y is not None
            and lv < -25 and rv < -25 and flap_cooldown == 0):
            flap = True
            flap_cooldown = 5  

        prev_lw_y = lw_y
        prev_rw_y = rw_y
        flap_cooldown = max(0, flap_cooldown - 1)
    else:
        prev_lw_y = None
        prev_rw_y = None

    cv2.imshow("Webcam (q=quit)", frame_flipped)
    return flap

def reset():
    global bird, pipes, score, game_over
    bird = Bird()
    pipes = []
    score = 0
    game_over = False
    pygame.time.set_timer(SPAWN_EVENT, SPAWN_MS)

prev_lw_y = None
prev_rw_y = None
flap_cooldown = 0

bird = Bird()
pipes = []
score = 0
game_over = True

while True:
    flap = get_both_hands_flap()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            cap.release()
            cv2.destroyAllWindows()
            pygame.quit()
            sys.exit()
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            cap.release()
            cv2.destroyAllWindows()
            pygame.quit()
            sys.exit()
        if e.type == SPAWN_EVENT and not game_over:
            pipes.append(Pipe())
        if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE and game_over:
            reset()

    if not game_over:
        bird.update(flap)
        for p in pipes:
            p.update()
            if p.off_screen():
                pipes.remove(p)
                score += 1
        for p in pipes:
            if bird.rect.colliderect(p.top) or bird.rect.colliderect(p.bot):
                game_over = True
        if bird.rect.top < 0 or bird.rect.bottom > HEIGHT:
            game_over = True

    screen.fill((135, 206, 235))
    bird.draw(screen)
    for p in pipes:
        p.draw(screen)
    msg = f"Score: {score}" if not game_over else f"Score: {score}   SPACE to restart"
    screen.blit(font.render(msg, True, (0, 0, 0)), (10, 10))
    pygame.display.flip()
    clock.tick(60)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.quit()
