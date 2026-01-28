from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def main():
    driver = webdriver.Chrome()
    actions = ActionChains(driver)
    driver.get("http://mazebound.caesarbrahh.dev")
    WebDriverWait(driver, 10).until(lambda d: d.execute_script("return typeof window !== 'undefined'") is True)
    driver.find_element("tag name", "body").click()

    snake = {'x': 2, 'y': 2}
    food = {'x': 0, 'y': 0}
    blocks = []

    while True:
        snake = driver.execute_script("return {'x': snakeX, 'y': snakeX, 'dir_x': velocityX, 'dir_y': velocityY}")
        food = driver.execute_script("return {'x': foodX, 'y': foodY}")
        blocks = driver.execute_script("return blocks")

        path = pursue_food(snake, food)

        actions.send_keys(Keys.ARROW_LEFT).perform()
        # if path == 1:
        #     # left key down

        # elif path == 2:
        #     # up key down
        # elif path == 3:
        #     # right key down
        # elif path == 4:
        #     # down key down


    driver.quit()

def pursue_food(s, f):
    n = 0
    return n

'''
def determine_action(s, f, b):
    if [s['x']+s['dir_x'], s['y']+s['dir_y']] in b:
        return [0, 0]
    else:
        if 

'''

if __name__ == "__main__":
    main()