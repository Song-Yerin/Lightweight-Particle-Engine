import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import math

# Pygame 초기화
pygame.init()
screen = pygame.display.set_mode((1200, 600), pygame.OPENGL | pygame.DOUBLEBUF)
pygame.display.set_caption("Custom Firework Colors")
clock = pygame.time.Clock()

# OpenGL 초기화
glClearColor(0.1, 0.1, 0.1, 1.0)
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_PROJECTION)
gluPerspective(45, (1200 / 600), 0.1, 100.0)
glMatrixMode(GL_MODELVIEW)

# 폭죽 속성
firework_speed = 1.0  # Z: 속도
firework_spread = 1.0  # X: 분산
firework_size = 0.1  # C: 크기
firework_color_index = 0  # V: 색상 (총 5가지)
selected_property = "z"  # 기본 선택 속성

# 색상 목록
FIREWORK_COLORS = [
    (255, 100, 100),  # 빨간색
    (100, 255, 100),  # 초록색
    (100, 100, 255),  # 파란색
    (255, 255, 100),  # 노란색
    (255, 100, 255),  # 보라색
]

# 사용자 정의 색상 조정 변수
custom_color = [255, 255, 255]  # 초기값: 흰색
is_customizing_color = False  # 색상 조정 모드 활성화 상태
adjusting_color_channel = "r"  # 기본 조정 채널 (R)

# 파티클 클래스
class Particle:
    def __init__(self, x, y, z, vx, vy, vz, lifetime, color, size):
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.lifetime = lifetime
        self.color = color
        self.size = size

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz
        self.vz -= 0.005  # 중력 효과
        self.lifetime -= 1

    def is_alive(self):
        return self.lifetime > 0

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glColor3f(self.color[0] / 255.0, self.color[1] / 255.0, self.color[2] / 255.0)
        draw_sphere(self.size, 10, 10)
        glPopMatrix()

# Sphere 그리기 함수
def draw_sphere(radius, slices, stacks):
    quadric = gluNewQuadric()
    gluSphere(quadric, radius, slices, stacks)
    gluDeleteQuadric(quadric)

# 파티클 시스템
fireworks = []

# 폭죽 생성 함수
def create_firework():
    x, y, z = random.uniform(-5, 5), -5, random.uniform(-5, 5)
    for _ in range(100):
        angle = random.uniform(0, 2 * math.pi)
        vx = math.cos(angle) * random.uniform(-firework_spread, firework_spread) * firework_speed
        vy = math.sin(angle) * random.uniform(-firework_spread, firework_spread) * firework_speed
        vz = random.uniform(-firework_spread, firework_spread) * firework_speed
        color = FIREWORK_COLORS[firework_color_index]
        fireworks.append(Particle(x, y, z, vx, vy, vz, 100, color, firework_size))

# 색상 추가 함수
def add_custom_color():
    global custom_color, FIREWORK_COLORS
    FIREWORK_COLORS.append(tuple(custom_color))

# 속성 조정 함수
def handle_property_adjustment():
    global firework_speed, firework_spread, firework_size, firework_color_index, selected_property, custom_color, is_customizing_color, adjusting_color_channel

    keys = pygame.key.get_pressed()

    # 색상 조정 모드
    if is_customizing_color:
        # 채널 선택
        if keys[pygame.K_r]:
            adjusting_color_channel = "r"
        elif keys[pygame.K_g]:
            adjusting_color_channel = "g"
        elif keys[pygame.K_b]:
            adjusting_color_channel = "b"

        # 값 증가/감소
        if keys[pygame.K_UP]:
            if adjusting_color_channel == "r":
                custom_color[0] = min(255, custom_color[0] + 1)
            elif adjusting_color_channel == "g":
                custom_color[1] = min(255, custom_color[1] + 1)
            elif adjusting_color_channel == "b":
                custom_color[2] = min(255, custom_color[2] + 1)
        elif keys[pygame.K_DOWN]:
            if adjusting_color_channel == "r":
                custom_color[0] = max(0, custom_color[0] - 1)
            elif adjusting_color_channel == "g":
                custom_color[1] = max(0, custom_color[1] - 1)
            elif adjusting_color_channel == "b":
                custom_color[2] = max(0, custom_color[2] - 1)

        # 색상 추가 완료
        if keys[pygame.K_RETURN]:
            add_custom_color()
            is_customizing_color = False

    # 속성 조정
    else:
        if keys[pygame.K_z]:
            selected_property = "z"
        elif keys[pygame.K_x]:
            selected_property = "x"
        elif keys[pygame.K_c]:
            selected_property = "c"
        elif keys[pygame.K_v]:
            selected_property = "v"

        # 속성 값 조정
        if keys[pygame.K_UP]:
            if selected_property == "z":
                firework_speed += 0.1
            elif selected_property == "x":
                firework_spread += 0.1
            elif selected_property == "c":
                firework_size += 0.01
            elif selected_property == "v":
                firework_color_index = (firework_color_index + 1) % len(FIREWORK_COLORS)
        elif keys[pygame.K_DOWN]:
            if selected_property == "z":
                firework_speed = max(0.1, firework_speed - 0.1)
            elif selected_property == "x":
                firework_spread = max(0.1, firework_spread - 0.1)
            elif selected_property == "c":
                firework_size = max(0.01, firework_size - 0.01)
            elif selected_property == "v":
                firework_color_index = (firework_color_index - 1) % len(FIREWORK_COLORS)

        # 색상 조정 모드 시작
        if keys[pygame.K_b]:
            is_customizing_color = True
            custom_color = [255, 255, 255]  # 초기값 설정

# 메인 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 폭죽 생성
    if pygame.time.get_ticks() % 2000 < 16:  # 2초마다 폭죽 생성
        create_firework()

    handle_property_adjustment()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 0, -20)

    # 파티클 업데이트 및 그리기
    for firework in fireworks:
        firework.update()
        firework.draw()
    fireworks = [f for f in fireworks if f.is_alive()]  # 살아있는 파티클만 유지

    pygame.display.flip()
    clock.tick(60)

pygame.quit()