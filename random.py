from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
import time
import random

def main():
    driver = webdriver.Chrome()
    actions = ActionChains(driver)
    driver.get("http://mazebound.caesarbrahh.dev")
    WebDriverWait(driver, 10).until(lambda d: d.execute_script("return typeof window !== 'undefined'") is True)
    driver.find_element("tag name", "body").click()

    snake = {'x': 2, 'y': 2}
    blocks = []
    x_max = driver.execute_script("return board.width")
    y_max = driver.execute_script("return board.height")

    try:
        while True:
            snake = driver.execute_script("return {'x': snakeX, 'y': snakeY, 'dir_x': velocityX, 'dir_y': velocityY}")
            blocks = driver.execute_script("return blocks")

            key = random(snake, blocks, x_max, y_max)

            actions.send_keys(key).perform()

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