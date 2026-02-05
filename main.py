from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
import math
import time
import random

def main():
    driver = webdriver.Chrome()
    actions = ActionChains(driver)
    driver.get("http://mazebound.caesarbrahh.dev")
    WebDriverWait(driver, 10).until(lambda d: d.execute_script("return typeof window !== 'undefined'") is True)
    driver.find_element("tag name", "body").click()

    snake = {'x': 2, 'y': 2}
    food = {'x': 0, 'y': 0}
    food_prev = food
    blocks = []
    x_max = driver.execute_script("return board.width")
    y_max = driver.execute_script("return board.height")

    try:
        while True:
            snake = driver.execute_script("return {'x': snakeX, 'y': snakeY, 'dir_x': velocityX, 'dir_y': velocityY}")
            food = driver.execute_script("return {'x': foodX, 'y': foodY}")
            blocks = driver.execute_script("return blocks")

            key = greedy(snake, food, blocks, x_max, y_max)
            # key = random(snake, blocks, x_max, y_max)

            actions.send_keys(key).perform()

            print(greedy.prev_pos)
            if food_prev != food:
                food_prev = food
                greedy.prev_pos = []

            if not driver.execute_script("return isRunning"):
                driver.quit()

            time.sleep(0.05)
    except WebDriverException as e:
        print("Selenium session lost:")
    finally:
        try:
            driver.quit()
        except:
            pass


# Greedy Euclidean path-finding algorithm w/ Back-Tracking Penalties
def greedy(s, f, b, xm, ym):
    if not hasattr(greedy, "prev_pos"):
        greedy.prev_pos = []

    food_pos = (f['x'], f['y'])
    MOVES = {
        Keys.ARROW_RIGHT: (25, 0),
        Keys.ARROW_LEFT: (-25, 0),
        Keys.ARROW_UP: (0, -25),
        Keys.ARROW_DOWN: (0, 25)
    }

    best_key = None
    best_dist = float("inf")

    for key, (dx, dy) in MOVES.items():
        next_pos = (s['x'] + dx, s['y'] + dy)

        # Checks for wall collisions
        if next_pos[0] < 0 or next_pos[1] < 0 or next_pos[0] >= xm or next_pos[1] >= ym:
            continue

        # Checks for block collisions
        if [next_pos[0], next_pos[1]] in b:
            continue

        d = math.dist(next_pos, food_pos)

        # Prevent stalling by penalizing each repeat position by 10k
        for i in greedy.prev_pos:
            if (i == next_pos):
                d += 10_000

        if d < best_dist:
            best_dist = d
            best_key = key

    if best_key:
        greedy.prev_pos.append((s['x'], s['y']))
        return best_key

# Random Walk path-finding algorithm (for fun)
def random(s, b, xm, ym):
    MOVES = {
        Keys.ARROW_RIGHT: (25, 0),
        Keys.ARROW_LEFT: (-25, 0),
        Keys.ARROW_UP: (0, -25),
        Keys.ARROW_DOWN: (0, 25)
    }
    options = []

    # block and edge detection
    for key, (dx, dy) in MOVES.items():
        next_pos = (s['x'] + dx, s['y'] + dy)
        if ([next_pos[0], next_pos[1]] not in b) and (next_pos[0] >= 0) and (next_pos[1] > 0) and (next_pos[0] < xm) and (next_pos[1] < ym):
            options.append(key)

    # choose and send random key
    random_key = random.choice(options)
    return random_key 

if __name__ == "__main__":
    main()