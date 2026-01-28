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
    current_pos = (s['x'], s['y'])
    food_pos = (f['x'], f['y'])
    current_dist = math.dist(current_pos, food_pos)
    MOVES = {
        Keys.ARROW_RIGHT: (25, 0),
        Keys.ARROW_LEFT: (-25, 0),
        Keys.ARROW_UP: (0, -25),
        Keys.ARROW_DOWN: (0, 25)
    }

    best_key = None
    best_dist = current_dist

    for key, (dx, dy) in MOVES.items():
        next_pos = (s['x'] + dx, s['y'] + dy)

        if next_pos[0] < 0 or next_pos[1] < 0 or next_pos[0] > xm or next_pos[1] > ym:
            
            continue
        
        if [next_pos[0], next_pos[1]] in b or [next_pos[0] + dx, next_pos[1] + dy] in b:
            continue

        d = math.dist(next_pos, food_pos)

        if d < best_dist:
            best_dist = d
            best_key = key

    if best_key:
        actions.send_keys(best_key).perform()
        print([s['x']+MOVES[best_key][0], s['y']+MOVES[best_key][1]], b)

if __name__ == "__main__":
    main()