import sys
from random import randint
import pygame
from pygame.locals import QUIT, Rect, KEYDOWN, K_SPACE

pygame.init()   # pygame 초기화
pygame.key.set_repeat(5,5)  # 키의 반복 기능을 설정하는 pygame 메소드

SURFACE = pygame.display.set_mode((800,600))    # 윈도 화면 크기 설정
FPSCLOCK = pygame.time.Clock()     # 프레임 레이트 조정용의 타이머

def main():
    """main routine"""
    walls = 80  # 직사각형의 수
    ship_y = 250    # 캐릭터의 Y 좌표
    velocity = 0    # 캐릭터의 상하 이동 속도
    score = 0   # 점수
    slope = randint(1,6)    # 동굴의 기울기
    sysfont = pygame.font.SysFont(None,36)
    ship_image = pygame.image.load("C:/Users/가은/Desktop/Ga-Eun/Python/PyGame-Games/ship.png")
    bang_image = pygame.image.load("C:/Users/가은/Desktop/Ga-Eun/Python/PyGame-Games/bang.png")
    holes = []  # 직사각형을 저장하는 배열
    for xpos in range(walls):   # x축 방향으로 10씩 비키면서 walls개 만듬, 만든 직사각형 리스트 holes에 추가
        holes.append(Rect(xpos*10, 100, 10, 400))   # Rect클래스 Rect(x좌표,y좌표,폭,높이)
    game_over = False   # 게임 오버 여부 플래그

    """main rope"""
    while True:
        is_space_down = False   # 루프 시작할 때마다 is_space_down을 False로 초기화 
        for event in pygame.event.get():    # 이번트 큐에서 이벤트 취득
            if event.type == QUIT:  # QUIT이면 게임 종료
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN: # 이벤트 유형이 KEYDOWN
                if event.key == K_SPACE:    # 키 코드가 K_SPACE이면
                    is_space_down = True    # is_space_down을 True

        # 캐릭터 이동
        if not game_over:   # 게임오버가 아닐 때
            score += 10 # 점수 10증가
            velocity += -3 if is_space_down else 3  # 스페이스 키 입력 상태에 따라 속도 -3(상승) 또는 +3(하강)
            ship_y += velocity

            # 동굴 스크롤
            edge = holes[-1].copy() # 오른쪽 끝의 직사각형을 복사해서 변수 edge에 저장, 마지막 요소 취득
            test = edge.move(0, slope)  # 새로 만든 직사각형을 이동시켜 바닥에 부딪히지 않는지 검출
            if test.top <= 0 or test.bottom >= 600:
                slope = randint(1,6) * (-1 if slope > 0 else 1)
                edge.inflate_ip(0, -20)
            edge.move_ip(10, slope)
            holes.append(edge)
            del holes[0]
            holes = [x.move(-10, 0) for x in holes]

            # 충돌
            if holes[0].top > ship_y or \
                holes[0].bottom < ship_y + 80:
                game_over = True
        
        # 그리기
        SURFACE.fill((0, 255, 0))
        for hole in holes:
            pygame.draw.rect(SURFACE, (0,0,0), hole)
        SURFACE.blit(ship_image, (0, ship_y))
        score_image = sysfont.render("score is {}".format(score), True, (0,0,255))
        SURFACE.blit(score_image, (600,20))

        if game_over:
            SURFACE.blit(bang_image, (0, ship_y-40))
        
        pygame.display.update()
        FPSCLOCK.tick(15)

if __name__ == "__main__":
    main()