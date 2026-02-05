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

            key = astar(snake, food, blocks, x_max, y_max)

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


# Greedy Euclidean path-finding algorithm w/ Back-Tracking Penalties
def astar(s, f, b, xm, ym):
    return "cake"

if __name__ == "__main__":
    main()