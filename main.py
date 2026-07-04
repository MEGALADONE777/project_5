import pygame as pg
import sys
import math
import random
import time
from config import *
from board import Board


class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Connect 4 Game")

        self.width = COLUMNS * DISC_SIZE
        self.height = (ROWS + 1) * DISC_SIZE
        self.screen = pg.display.set_mode((self.width, self.height))
        self.font = pg.font.SysFont("Calibri", 45)
        self.btn_font = pg.font.SysFont("Calibri", 28)

        self.btn_width = 130
        self.btn_height = 40
        self.btn_x = self.width - self.btn_width - 10
        self.btn_y = (DISC_SIZE - self.btn_height) // 2

        self.reset_game()

    def reset_game(self):
        self.board = Board()
        self.turn = random.randint(REAL_PLAYER, AI_PLAYER)
        self.game_over = False

    def draw_reset(self):
        pg.draw.rect(self.screen, BLUE, (self.btn_x, self.btn_y, self.btn_width, self.btn_height), border_radius=5)
        text = self.btn_font.render("New Game", True, WHITE)
        text_rect = text.get_rect(center=(self.btn_x + self.btn_width // 2, self.btn_y + self.btn_height // 2))
        self.screen.blit(text, text_rect)

    def draw(self):

        if not self.game_over:
            pg.draw.rect(self.screen, WHITE, (0, 0, self.width, DISC_SIZE))


        for c in range(COLUMNS):
            for r in range(ROWS):
                pg.draw.rect(self.screen, BLUE, (c * DISC_SIZE, r * DISC_SIZE + DISC_SIZE, DISC_SIZE, DISC_SIZE))
                pg.draw.circle(self.screen, WHITE,
                               (int(c * DISC_SIZE + DISC_SIZE / 2), int(r * DISC_SIZE + DISC_SIZE + DISC_SIZE / 2)),
                               DISC_RADIUS)


        for c in range(COLUMNS):
            for r in range(ROWS):
                if self.board.board[r][c] == REAL_PLAYER_PIECE:
                    pg.draw.circle(self.screen, RED, (int(c * DISC_SIZE + DISC_SIZE / 2),
                                                      self.height - int(r * DISC_SIZE + DISC_SIZE / 2)), DISC_RADIUS)
                elif self.board.board[r][c] == AI_PLAYER_PIECE:
                    pg.draw.circle(self.screen, YELLOW, (int(c * DISC_SIZE + DISC_SIZE / 2),
                                                         self.height - int(r * DISC_SIZE + DISC_SIZE / 2)), DISC_RADIUS)


        self.draw_reset()
        pg.display.update()

    def display_winner(self, message, color):

        pg.draw.rect(self.screen, WHITE, (0, 0, self.btn_x - 10, DISC_SIZE))


        label_main = self.font.render(message, True, color)
        self.screen.blit(label_main, (10, 5))


        label_sub = self.btn_font.render("Play again? (Press Enter)", True, BLACK)
        self.screen.blit(label_sub, (15, 50))

        self.game_over = True
        self.draw_reset()
        pg.display.update()

    def play(self):
        self.draw()

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        sys.exit()

                    if self.game_over and event.key == pg.K_RETURN:
                        self.reset_game()
                        self.draw()

                if event.type == pg.MOUSEBUTTONDOWN:
                    pos_x, pos_y = event.pos

                    if self.btn_x <= pos_x <= self.btn_x + self.btn_width and self.btn_y <= pos_y <= self.btn_y + self.btn_height:
                        self.reset_game()
                        self.draw()
                        continue


                if self.game_over:
                    continue

                if event.type == pg.MOUSEMOTION:
                    pg.draw.rect(self.screen, WHITE, (0, 0, self.width, DISC_SIZE))
                    pos_x = event.pos[0]
                    if self.turn == REAL_PLAYER:
                        pg.draw.circle(self.screen, RED, (pos_x, int(DISC_SIZE / 2)), DISC_RADIUS)
                    self.draw_reset()
                    pg.display.update()

                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.turn == REAL_PLAYER:
                        pos_x = event.pos[0]
                        col = int(math.floor(pos_x / DISC_SIZE))

                        if 0 <= col < COLUMNS and self.board.is_valid_pos(col):
                            row = self.board.get_next_free_row(col)
                            self.board.drop_piece(row, col, REAL_PLAYER_PIECE)

                            if self.board.check_win(REAL_PLAYER_PIECE):
                                self.display_winner("ВЫ ПОБЕДИЛИ!", RED)
                            else:
                                self.turn = AI_PLAYER

                            self.draw()


            if self.turn == AI_PLAYER and not self.game_over:
                time.sleep(0.6)
                valid_columns = self.board.get_valid_pos()

                if valid_columns:
                    col = random.choice(valid_columns)
                    row = self.board.get_next_free_row(col)
                    self.board.drop_piece(row, col, AI_PLAYER_PIECE)

                    if self.board.check_win(AI_PLAYER_PIECE):
                        self.display_winner("ИИ ПОБЕДИЛ!", YELLOW)
                    elif len(self.board.get_valid_pos()) == 0:
                        self.display_winner("НИЧЬЯ!", BLACK)
                    else:
                        self.turn = REAL_PLAYER

                    self.draw()


if __name__ == "__main__":
    game = Game()
    game.play()
    pg.quit()











































































