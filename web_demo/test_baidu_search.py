import os
import pytest
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from loguru import logger


class TestBaidu:

    def setup_class(self):
        try:
            headless = os.getenv("headless")
        except Exception:
            headless = None
        chrome_options = Options()
        if headless == "true":
            logger.info("设置了headless变量并且设置为true，将会无界面运行测试")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument('--no-sandbox')
        else:
            logger.info("系统未设置headless为true，将会有界面运行测试")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_window_size("1360", "768")
        self.driver.implicitly_wait(10)
        logger.info("请求百度www.baidu.com")
        self.driver.get('http://www.baidu.com')

    def teardown_class(self):
        self.driver.quit()

    @pytest.mark.parametrize("keys", ("霍格沃兹", "测试开发"))
    def test_baidu(self, keys):
        el = self.driver.find_element(By.ID, "kw")
        logger.info("清除输入框的内容")
        el.clear()
        logger.info(f"填写关键字{keys}到输入框")
        el.send_keys(keys)
        logger.info(f"提交，进行符合{keys}的结果查找")
        self.driver.find_element(By.ID, "su").click()
        sleep(5)
        assert keys in self.driver.title


if __name__ == '__main__':
    pytest.main(["-s", "-v"])
