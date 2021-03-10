import pygame
import numpy as np

pygame.init()


class SpriteButton:
    def __init__(self, x, y, width, height, gpx=1, gpy=1, texture=pygame.transform.scale(pygame.image.load("images/costyl.png"), (100, 100))):
        super().__init__()
        self.x = x
        self.y = y
        self.game_pos_x = gpx
        self.game_pos_y = gpy
        self.size = (width, height)
        self.texture = pygame.transform.scale(texture, self.size)
        self.rect = self.texture.get_rect(topleft=(x, y))


class Game:
    def __init__(self):
        super().__init__()
        self.is_running = True
        self.screen = pygame.display.set_mode((340, 500))
        pygame.display.set_caption("Cross zeros")
        self.font = pygame.font.SysFont('Arial Black', 20)
        self.screen.fill((255, 255, 255))
        pygame.display.flip()
        self.clock = pygame.time.Clock()
        self.buttons_list = []
        self.back_surf = pygame.Surface((320, 320))
        self.back_surf.fill((0, 0, 0))
        self.back_rect = pygame.Rect((10, 10, 230, 230))
        self.queue_state = 0
        self.cross_sprite = pygame.image.load("images/cross.png")
        self.zero_sprite = pygame.image.load("images/zero.png")
        self.retry = pygame.image.load("images/retry.png")
        self.costyl = pygame.image.load("images/costyl.png")
        self.main_matrix = np.ndarray(shape=(3, 3), dtype=int, buffer=np.asarray([0 for i in range(10)]))
        self.replace_dict = {"1": "x", "2": "o", "0": " "}
        self.is_victory = False

    def get_matrix(self):
        game = f" {self.main_matrix[0][0]} | {self.main_matrix[0][1]} | {self.main_matrix[0][2]} \n" \
               f"-----------\n" \
               f" {self.main_matrix[1][0]} | {self.main_matrix[1][1]} | {self.main_matrix[1][2]} \n" \
               f"-----------\n" \
               f" {self.main_matrix[2][0]} | {self.main_matrix[2][1]} | {self.main_matrix[2][2]} "
        for i in self.replace_dict.keys():
            game = game.replace(i, self.replace_dict[i])
        return game

    def get_victory(self, matrix):
        counter = 0
        for i in matrix:
            if 1 in i and 0 not in i and 2 not in i:
                return True
            elif 2 in i and 0 not in i and 1 not in i:
                return True
            elif matrix[0][counter] == matrix[1][counter] == matrix[2][counter] != 0:
                return True
            counter += 1
        if matrix[0][0] == matrix[1][1] == matrix[2][2] != 0:
            return True
        if matrix[0][2] == matrix[1][1] == matrix[2][0] != 0:
            return True
        return False

    def show_button(self, button):
        self.screen.blit(button.texture, button.rect)

    def reset_game(self):
        return np.ndarray(shape=(3, 3), dtype=int, buffer=np.asarray([0 for i in range(10)]))

    def game(self):
        count_x = 10
        count_gpx = 1
        count_y = 10
        count_gpy = 1
        while count_y <= 240:
            while count_x <= 240:
                self.buttons_list.append(SpriteButton(count_x, count_y, 100, 100, count_gpx, count_gpy))
                count_gpx += 1
                count_x += 110
            count_x = 10
            count_gpx = 1
            count_gpy += 1
            count_y += 110
        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                if not self.is_victory:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for button in self.buttons_list:
                            if button.rect.collidepoint(event.pos):
                                if self.queue_state == 0:
                                    if self.main_matrix[button.game_pos_y - 1][button.game_pos_x - 1] == 0:
                                        self.main_matrix[button.game_pos_y - 1][button.game_pos_x - 1] = 1
                                        button.texture = pygame.transform.scale(self.cross_sprite, button.size)
                                        self.queue_state = 1
                                    if self.get_victory(self.main_matrix):
                                        victory_text = self.font.render('Выиграл крестик', False, (0, 255, 0))
                                        self.screen.blit(victory_text, (75, 350))
                                        self.is_victory = True
                                else:
                                    if self.main_matrix[button.game_pos_y - 1][button.game_pos_x - 1] == 0:
                                        self.main_matrix[button.game_pos_y - 1][button.game_pos_x - 1] = 2
                                        button.texture = pygame.transform.scale(self.zero_sprite, button.size)
                                        self.queue_state = 0
                                    if self.get_victory(self.main_matrix):
                                        victory_text = self.font.render('Выиграл нолик', False, (0, 255, 0))
                                        self.screen.blit(victory_text, (75, 350))
                                        self.is_victory = True
                else:
                    retry_button = SpriteButton(150, 400, 50, 50, texture=self.retry)
                    self.show_button(retry_button)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if retry_button.rect.collidepoint(event.pos):
                            self.main_matrix = self.reset_game()
                            for button in self.buttons_list:
                                button.texture = pygame.transform.scale(self.costyl, button.size)
                            self.is_victory = False
                            self.queue_state = 0
                            self.screen.fill((255, 255, 255))
            self.screen.blit(self.back_surf, self.back_rect)
            for button in self.buttons_list:
                self.show_button(button)
            pygame.display.update()
            self.clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    Game().game()
