import os
import sys
import random
import numpy as np

# 设置环境变量来隐藏pygame的欢迎消息
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from pygame import mixer

class SnakeGame:
    def __init__(self, seed=0, board_size=12, silent_mode=True):
        # 游戏板的基本设置
        self.board_size = board_size
        self.grid_size = self.board_size ** 2
        self.cell_size = 40
        self.width = self.height = self.board_size * self.cell_size

        # 游戏显示界面的大小
        self.border_size = 20
        self.display_width = self.width + 2 * self.border_size
        self.display_height = self.height + 2 * self.border_size + 40

        # 是否静音模式
        self.silent_mode = silent_mode
        if not silent_mode:
            pygame.init()
            pygame.display.set_caption("Snake Game")
            self.screen = pygame.display.set_mode((self.display_width, self.display_height))
            self.font = pygame.font.Font(None, 36)

            # 加载声音效果
            mixer.init()
            self.sound_eat = mixer.Sound("sound/eat.wav")
            self.sound_game_over = mixer.Sound("sound/game_over.wav")
            self.sound_victory = mixer.Sound("sound/victory.wav")
        else:
            self.screen = None
            self.font = None

        # 初始化蛇和非蛇的位置
        self.snake = None
        self.non_snake = None

        # 初始化方向和得分
        self.direction = None
        self.score = 0
        self.food = None
        self.seed_value = seed

        random.seed(seed)  # 设置随机种子
        
        self.reset()

    def reset(self):
        # 重置游戏
        self.snake = [(self.board_size // 2 + i, self.board_size // 2) for i in range(1, -2, -1)]  # 初始化蛇的位置
        self.non_snake = set([(row, col) for row in range(self.board_size) for col in range(self.board_size) if (row, col) not in self.snake])  # 初始化非蛇的位置
        self.direction = "DOWN"  # 蛇的初始方向
        self.food = self._generate_food()
        self.score = 0

    def step(self, action):
        # 根据动作更新方向
        self._update_direction(action)

        # 根据当前动作移动蛇
        row, col = self.snake[0]
        if self.direction == "UP":
            row -= 1
        elif self.direction == "DOWN":
            row += 1
        elif self.direction == "LEFT":
            col -= 1
        elif self.direction == "RIGHT":
            col += 1

        # 检查蛇是否吃到食物
        if (row, col) == self.food:
            food_obtained = True
            self.score += 10  # 吃到食物得分增加10
            if not self.silent_mode:
                self.sound_eat.play()
        else:
            food_obtained = False
            self.non_snake.add(self.snake.pop())  # 蛇的最后一个部分被移除

        # 检查蛇是否与自己或墙壁碰撞
        done = (
            (row, col) in self.snake
            or row < 0
            or row >= self.board_size
            or col < 0
            or col >= self.board_size
        )

        if not done:
            self.snake.insert(0, (row, col))
            self.non_snake.remove((row, col))
        else:
            if not self.silent_mode:
                if len(self.snake) < self.grid_size:
                    self.sound_game_over.play()
                else:
                    self.sound_victory.play()

        # 蛇移动完成后添加新的食物
        if food_obtained:
            self.food = self._generate_food()

        info ={
            "snake_size": len(self.snake),
            "snake_head_pos": np.array(self.snake[0]),
            "prev_snake_head_pos": np.array(self.snake[1]),
            "food_pos": np.array(self.food),
            "food_obtained": food_obtained
        }

        return done, info

    def _update_direction(self, action):
        # 更新蛇的方向
        if action == 0:
            if self.direction != "DOWN":
                self.direction = "UP"
        elif action == 1:
            if self.direction != "RIGHT":
                self.direction = "LEFT"
        elif action == 2:
            if self.direction != "LEFT":
                self.direction = "RIGHT"
        elif action == 3:
            if self.direction != "UP":
                self.direction = "DOWN"

    def _generate_food(self):
        # 生成食物的位置
        if len(self.non_snake) > 0:
            food = random.sample(self.non_snake, 1)[0]
        else:
            food = (0, 0)
        return food
    
    def draw_score(self):
        # 显示得分
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (self.border_size, self.height + 2 * self.border_size))
    
    def draw_welcome_screen(self):
        # 显示欢迎界面
        title_text = self.font.render("SNAKE GAME", True, (255, 255, 255))
        start_button_text = "START"

        self.screen.fill((0, 0, 0))
        self.screen.blit(title_text, (self.display_width // 2 - title_text.get_width() // 2, self.display_height // 4))
        self.draw_button_text(start_button_text, (self.display_width // 2, self.display_height // 2))
        pygame.display.flip()

    def draw_game_over_screen(self):
        # 显示游戏结束界面
        game_over_text = self.font.render("GAME OVER", True, (255, 255, 255))
        final_score_text = self.font.render(f"SCORE: {self.score}", True, (255, 255, 255))
        retry_button_text = "RETRY"

        self.screen.fill((0, 0, 0))
        self.screen.blit(game_over_text, (self.display_width // 2 - game_over_text.get_width() // 2, self.display_height // 4))
        self.screen.blit(final_score_text, (self.display_width // 2 - final_score_text.get_width() // 2, self.display_height // 4 + final_score_text.get_height() + 10))
        self.draw_button_text(retry_button_text, (self.display_width // 2, self.display_height // 2))          
        pygame.display.flip()

    def draw_button_text(self, button_text_str, pos, hover_color=(255, 255, 255), normal_color=(100, 100, 100)):
        # 绘制按钮文本
        mouse_pos = pygame.mouse.get_pos()
        button_text = self.font.render(button_text_str, True, normal_color)
        text_rect = button_text.get_rect(center=pos)
        
        if text_rect.collidepoint(mouse_pos):
            colored_text = self.font.render(button_text_str, True, hover_color)
        else:
            colored_text = self.font.render(button_text_str, True, normal_color)
        
        self.screen.blit(colored_text, text_rect)
    
    def draw_countdown(self, number):
        # 绘制倒计时
        countdown_text = self.font.render(str(number), True, (255, 255, 255))
        self.screen.blit(countdown_text, (self.display_width // 2 - countdown_text.get_width() // 2, self.display_height // 2 - countdown_text.get_height() // 2))
        pygame.display.flip()

    def is_mouse_on_button(self, button_text):
        # 检查鼠标是否在按钮上
        mouse_pos = pygame.mouse.get_pos()
        text_rect = button_text.get_rect(
            center=(
                self.display_width // 2,
                self.display_height // 2,
            )
        )
        return text_rect.collidepoint(mouse_pos)

    def render(self):
        # 渲染游戏界面
        self.screen.fill((0, 0, 0))

        # 绘制边框
        pygame.draw.rect(self.screen, (255, 255, 255), (self.border_size - 2, self.border_size - 2, self.width + 4, self.height + 4), 2)

        # 绘制蛇
        self.draw_snake()
        
        # 绘制食物
        if len(self.snake) < self.grid_size:
            r, c = self.food
            pygame.draw.rect(self.screen, (255, 0, 0), (c * self.cell_size + self.border_size, r * self.cell_size + self.border_size, self.cell_size, self.cell_size))

        # 绘制得分
        self.draw_score()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def draw_snake(self):
        # 绘制蛇的头和身体
        head_r, head_c = self.snake[0]
        head_x = head_c * self.cell_size + self.border_size
        head_y = head_r * self.cell_size + self.border_size

        pygame.draw.polygon(self.screen, (100, 100, 255), [
            (head_x + self.cell_size // 2, head_y),
            (head_x + self.cell_size, head_y + self.cell_size // 2),
            (head_x + self.cell_size // 2, head_y + self.cell_size),
            (head_x, head_y + self.cell_size // 2)
        ])

        eye_size = 3
        eye_offset = self.cell_size // 4
        pygame.draw.circle(self.screen, (255, 255, 255), (head_x + eye_offset, head_y + eye_offset), eye_size)
        pygame.draw.circle(self.screen, (255, 255, 255), (head_x + self.cell_size - eye_offset, head_y + eye_offset), eye_size)

        color_list = np.linspace(255, 100, len(self.snake), dtype=np.uint8)
        i = 1
        for r, c in self.snake[1:]:
            body_x = c * self.cell_size + self.border_size
            body_y = r * self.cell_size + self.border_size
            body_width = self.cell_size
            body_height = self.cell_size
            body_radius = 5
            pygame.draw.rect(self.screen, (0, color_list[i], 0),
                            (body_x, body_y, body_width, body_height), border_radius=body_radius)
            i += 1
        pygame.draw.rect(self.screen, (255, 100, 100),
                            (body_x, body_y, body_width, body_height), border_radius=body_radius)
        

if __name__ == "__main__":
    # 游戏的主循环
    seed = random.randint(0, 1e9)
    game = SnakeGame(seed=seed, silent_mode=True)
    pygame.init()
    game.screen = pygame.display.set_mode((game.display_width, game.display_height))
    pygame.display.set_caption("Snake Game")
    game.font = pygame.font.Font(None, 36)
    

    game_state = "welcome"

    start_button = game.font.render("START", True, (0, 0, 0))
    retry_button = game.font.render("RETRY", True, (0, 0, 0))

    update_interval = 0.15
    start_time = time.time()
    action = -1

    while True:
        # 游戏的主循环，处理用户输入和游戏状态
        for event in pygame.event.get():
            # ... [处理各种事件]

        if game_state == "welcome":
            game.draw_welcome_screen()

        if game_state == "game_over":
            game.draw_game_over_screen()

        if game_state == "running":
            if time.time() - start_time >= update_interval:
                done, _ = game.step(action)
                game.render()
                start_time = time.time()

                if done:
                    game_state = "game_over"
        pygame.time.wait(1)
