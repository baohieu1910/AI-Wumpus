import pygame

from constants import *
import sys

class Menu():
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(CAPTION)
        self.font = pygame.font.Font(FONT_MRSMONSTER, 30)
        self.bg = pygame.image.load('../Assets/bg.jpg').convert()
        self.bg = pygame.transform.scale(self.bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.state = HOME

    def draw_button(self, surf, rect, button_color, text_color, text):
        pygame.draw.rect(surf, button_color, rect)
        text_surf = self.font.render(text, True, text_color)
        text_rect = text_surf.get_rect()
        text_rect.center = rect.center
        self.screen.blit(text_surf, text_rect)

    def draw_info(self, text, text_color, rect):
        text_surf = self.font.render(text, True, text_color)
        text_rect = text_surf.get_rect()
        text_rect.center = rect.center
        self.screen.blit(text_surf, text_rect)

    def home_draw(self):
        self.screen.blit(self.bg, (0, 0))

    def home_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.mouse = pygame.mouse.get_pos()

            if self.state == HOME:
                if 235 <= self.mouse[0] <= 735 and 250 <= self.mouse[1] <= 330:
                    self.draw_button(self.screen, PLAY_POS, BRONZE, WHITE, "PLAY")
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.state = SELECT_MAP  # Chuyển sang trạng thái chọn map
                else:
                    self.draw_button(self.screen, PLAY_POS, BROWN, BLACK, "PLAY")

                if 235 <= self.mouse[0] <= 735 and 350 <= self.mouse[1] <= 430:
                    self.draw_button(self.screen, ABOUT_US, BRONZE, WHITE, "ABOUT US")
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.state = ABOUT_US
                else:
                    self.draw_button(self.screen, ABOUT_US, BROWN, BLACK, "ABOUT US")

                if 235 <= self.mouse[0] <= 735 and 450 <= self.mouse[1] <= 530:
                    self.draw_button(self.screen, EXIT_POS, BRONZE, WHITE, "EXIT")
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.quit()
                        sys.exit()
                else:
                    self.draw_button(self.screen, EXIT_POS, BROWN, BLACK, "EXIT")
            elif self.state == SELECT_MAP:
                if 235 <= self.mouse[0] <= 735 and 200 <= self.mouse[1] <= 250:
                    self.draw_button(self.screen, LEVEL_1_POS, BRONZE, WHITE, "MAP 1")
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.state = MAP_STATE_LIST[0]
                else:
                    self.draw_button(self.screen, LEVEL_1_POS, BROWN, BLACK, "MAP 1")
                if 235 <= self.mouse[0] <= 735 and 280 <= self.mouse[1] <= 330:
                    self.draw_button(self.screen, LEVEL_2_POS, BRONZE, WHITE, "MAP 2")
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.state = MAP_STATE_LIST[1]
                else:
                    self.draw_button(self.screen, LEVEL_2_POS, BROWN, BLACK, "MAP 2")
                if 235 <= self.mouse[0] <= 735 and 360 <= self.mouse[1] <= 410:
                    self.draw_button(self.screen, LEVEL_3_POS, BRONZE, WHITE, "MAP 3")
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.state = MAP_STATE_LIST[2]
                else:
                    self.draw_button(self.screen, LEVEL_3_POS, BROWN, BLACK, "MAP 3")
                if 235 <= self.mouse[0] <= 735 and 440 <= self.mouse[1] <= 490:
                    self.draw_button(self.screen, LEVEL_4_POS, BRONZE, WHITE, "MAP 4")
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.state = MAP_STATE_LIST[3]
                else:
                    self.draw_button(self.screen, LEVEL_4_POS, BROWN, BLACK, "MAP 4")
                if 235 <= self.mouse[0] <= 735 and 520 <= self.mouse[1] <= 570:
                    self.draw_button(self.screen, LEVEL_5_POS, BRONZE, WHITE, "MAP 5")
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.state = MAP_STATE_LIST[4]
                else:
                    self.draw_button(self.screen, LEVEL_5_POS, BROWN, BLACK, "MAP 5")
                if 235 <= self.mouse[0] <= 735 and 600 <= self.mouse[1] <= 650:
                    self.draw_button(self.screen, BACK_POS, BRONZE, WHITE, "BACK")
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.state = HOME
                else:
                    self.draw_button(self.screen, BACK_POS, BROWN, BLACK, "BACK")

            elif self.state == ABOUT_US:
                self.screen.fill(WHITE)
                self.screen.blit(self.bg, (0, 0))
                self.draw_info('GROUP MEMBERS', BLACK, TITLE_POS)
                self.draw_info('21120407 - Tran Phan Phuc An', BLACK, MEMBER_1_POS)
                self.draw_info('21120409 - Nguyen Duc Duy Anh', BLACK, MEMBER_2_POS)
                self.draw_info('21120423 - Pham Manh Cuong', BLACK, MEMBER_3_POS)
                self.draw_info('21120451 - Le Bao Hieu', BLACK, MEMBER_4_POS)
                self.draw_info('21120539 - Tran Minh Quang', BLACK, MEMBER_5_POS)
                if 235 <= self.mouse[0] <= 735 and 470 <= self.mouse[1] <= 520:
                    self.draw_button(self.screen, MEMBER_BACK_POS, BRONZE, WHITE, "BACK")
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.state = HOME
                else:
                    self.draw_button(self.screen, MEMBER_BACK_POS, BROWN, BLACK, "BACK")

            pygame.display.update()
    def run(self):
        while True:
            if self.state == HOME or self.state == ABOUT_US or self.state == SELECT_MAP:
                self.home_draw()
                self.home_event()
            else:
                break
        pygame.quit()
        return self.state

