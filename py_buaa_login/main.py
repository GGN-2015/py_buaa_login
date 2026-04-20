import requests
from requests.exceptions import Timeout, RequestException

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import time
import traceback
from typing import Optional
import os
import logging
from multiprocessing import Process, Queue

# 关闭 webdriver-manager 日志与 Selenium 警告
os.environ["WDM_LOG_LEVEL"] = "0"
os.environ["WDM_SSL_VERIFY"] = "0"
logging.getLogger("selenium").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)

try:
    from .time_elapsed import timed_task
except:
    from time_elapsed import timed_task

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
    options.add_argument("--disable-background-networking")
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    wait_page_loaded(driver)
    time.sleep(sleep_time)
    return driver

def login_check_core(timeout: float) -> bool:
    try:
        response = requests.get(
            "https://www.baidu.com",
            allow_redirects=False,
            timeout=timeout,
        )
        return response.status_code == 200

    except Timeout:
        return False

    except RequestException:
        return False

def _task(timeout:float, result_q:Queue):
    res = login_check_core(timeout)
    result_q.put(res)

# 检测网络是否可用
@timed_task("login check")
def login_check(timeout: float = 2) -> bool:
    return login_check_core(timeout=timeout)

# 等待页面加载完成
def wait_page_loaded(driver, timeout=10):
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

# 登录核心函数
@timed_task("logout")
def login_core_funcion(driver, username:str, password:str):
    # 点击登录按钮, 尝试登录
    try:
        fill_input_by_id_class(driver, "username", "input-box", username)
        fill_input_by_id_class(driver, "password", "input-box", password)
        click_button_by_id_class(driver, "login-account", "btn-login")
        time.sleep(1.0)
        wait_page_loaded(driver)
    except:
        traceback.print_exc()

# 如果没有网络可用
# 则试图登录校园网客户端
def login(username:str, password:str, headless:bool=True) -> bool:
    info_print("checking login status ...")
    driver = None

    if not login_check():
        info_print("not logged in.")

        driver = create_driver_with_url("https://gw.buaa.edu.cn", headless)

        info_print("try to login ...")
        login_core_funcion(driver, username, password)

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

# 退出登陆的核心函数
@timed_task("logout")
def logout_core_function(driver):
    try:
        click_button_by_id_class(driver, "logout", "btn-logout")
        time.sleep(0.5)
        click_button_by_id_class(driver, None, "btn-confirm")
        time.sleep(0.5)
        wait_page_loaded(driver)
    except:
        traceback.print_exc()

# 试图退出校园网
def logout(headless:bool=True) -> bool:
    info_print("checking login status ...")
    driver = None

    if login_check():
        info_print("logged in.")
        driver = create_driver_with_url("https://gw.buaa.edu.cn", headless)
        
        info_print("try to logout ...")
        logout_core_function(driver)
        
    ans = not login_check()
    if ans:
        info_print("logout success.")
    else:
        info_print("logout failed.")

    if driver is not None:
        driver.quit()
    return ans
