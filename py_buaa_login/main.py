import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import time
import traceback
from typing import Optional

info_print = print

# 向指定的文本框中填入内容
def fill_input_by_id_class(driver, input_id: str, input_class: str, text: str, timeout: int = 1):
    selector = f"#{input_id}.{input_class}"
    elem = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
    )
    elem.clear()
    elem.send_keys(text)

# 点击按钮
def click_button_by_id_class(driver, btn_id: Optional[str], btn_class: str, timeout: int = 2):
    if btn_id is not None:
        selector = f"#{btn_id}.{btn_class}"
    else:
        selector = f".{btn_class}"
    btn = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    )
    driver.execute_script("arguments[0].click();", btn)

# 检查页面中是否有指定的元素
def has_element_with_id_and_class(driver, target_id, target_class):
    try:
        driver.find_element(By.CSS_SELECTOR, f"#{target_id}.{target_class}")
        return True
    except NoSuchElementException:
        return False

# 使用指定 url 启动一个 driver
def create_driver_with_url(url:str, headless:bool, sleep_time:float=2.0):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    wait_page_loaded(driver)
    time.sleep(sleep_time)
    return driver

# 检测网络是否可用
def login_check(timeout:float=2) -> bool:
    try:
        response = requests.get(
            "https://www.baidu.com", allow_redirects=False, timeout=timeout)
        return response.status_code == 200
    except:
        return False

# 等待页面加载完成
def wait_page_loaded(driver, timeout=10):
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

# 如果没有网络可用
# 则试图登录校园网客户端
def login(stuid:str, password:str, headless:bool=True) -> bool:
    info_print("checking login status ...")
    driver = None

    if not login_check():
        info_print("not logged in.")

        driver = create_driver_with_url("https://gw.buaa.edu.cn", headless)

        # 找到登录按钮
        # 则尝试登录
        info_print("try to login ...")
        try:
            fill_input_by_id_class(driver, "username", "input-box", stuid)
            fill_input_by_id_class(driver, "password", "input-box", password)
            click_button_by_id_class(driver, "login-account", "btn-login")
            time.sleep(1.0)
            wait_page_loaded(driver)
        except:
            traceback.print_exc()

    # 检查网络登录是否成功
    ans = login_check()
    if ans:
        info_print("login success.")
    else:
        info_print("login failed.")

    # 最后再释放连接
    if driver is not None:
        driver.quit()
    return ans

# 试图退出校园网
def logout(headless:bool=True) -> bool:
    info_print("checking login status ...")
    driver = None

    if login_check():
        info_print("logged in.")

        info_print("try to logout ...")
        driver = create_driver_with_url("https://gw.buaa.edu.cn", headless)
        try:
            click_button_by_id_class(driver, "logout", "btn-logout")
            time.sleep(0.5)
            click_button_by_id_class(driver, None, "btn-confirm")
            time.sleep(0.5)
            wait_page_loaded(driver)
        except:
            traceback.print_exc()
            
    ans = not login_check()
    if ans:
        info_print("logout success.")
    else:
        info_print("logout failed.")

    if driver is not None:
        driver.quit()
    return ans
