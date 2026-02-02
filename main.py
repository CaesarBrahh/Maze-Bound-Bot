from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
import math
import time

def main():
    driver = webdriver.Chrome()
    actions = ActionChains(driver)
    driver.get("http://mazebound.caesarbrahh.dev")
    WebDriverWait(driver, 10).until(lambda d: d.execute_script("return typeof window !== 'undefined'") is True)
    driver.find_element("tag name", "body").click()

    snake = {'x': 2, 'y': 2}
    food = {'x': 0, 'y': 0}
    blocks = []
    x_max = driver.execute_script("return board.width")
    y_max = driver.execute_script("return board.height")

    try:
        while True:
            snake = driver.execute_script("return {'x': snakeX, 'y': snakeY, 'dir_x': velocityX, 'dir_y': velocityY}")
            food = driver.execute_script("return {'x': foodX, 'y': foodY}")
            blocks = driver.execute_script("return blocks")

            pursue_food(snake, food, blocks, actions, x_max, y_max)

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


def pursue_food(s, f, b, actions, xm, ym):
    if not hasattr(pursue_food, "prev_pos"):
        pursue_food.prev_pos = None

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

        # Prevent stalling by "penalizing" a repeated move
        if next_pos == pursue_food.prev_pos:
            d += 10_000
            print(d)

        if d < best_dist:
            best_dist = d
            best_key = key

    if best_key:
        pursue_food.prev_pos = (s['x'], s['y'])
        actions.send_keys(best_key).perform()

if __name__ == "__main__":
    main()