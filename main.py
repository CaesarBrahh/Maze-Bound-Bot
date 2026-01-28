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

    try:
        while True:
            snake = driver.execute_script("return {'x': snakeX, 'y': snakeY, 'dir_x': velocityX, 'dir_y': velocityY}")
            food = driver.execute_script("return {'x': foodX, 'y': foodY}")
            blocks = driver.execute_script("return blocks")

            pursue_food(snake, food, actions)

            if not driver.execute_script("return isRunning"):
                driver.quit()

            time.sleep(0.15)
    except WebDriverException as e:
        print("Selenium session lost:")
    finally:
        try:
            driver.quit()
        except:
            pass


def pursue_food(s, f, actions):
    current_pos = (s['x'], s['y'])
    food_pos = (f['x'], f['y'])
    current_dist = math.dist(current_pos, food_pos)
    MOVES = {
        Keys.ARROW_RIGHT: (1, 0),
        Keys.ARROW_LEFT: (-1, 0),
        Keys.ARROW_UP: (0, -1),
        Keys.ARROW_DOWN: (0, 1)
    }

    best_key = None
    best_dist = current_dist

    for key, (dx, dy) in MOVES.items():
        next_pos = (s['x'] + dx, s['y'] + dy)
        d = math.dist(next_pos, food_pos)

        if d < best_dist:
            best_dist = d
            best_key = key

    if best_key:
        actions.send_keys(best_key).perform()

'''
def determine_action(s, f, b):
    if [s['x']+s['dir_x'], s['y']+s['dir_y']] in b:
        return [0, 0]
    else:
        if 

'''

if __name__ == "__main__":
    main()