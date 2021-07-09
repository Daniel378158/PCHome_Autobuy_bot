from selenium import webdriver
import requests
import time
import sys
option = webdriver.ChromeOptions()
option.add_argument("--lang=en")
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains ## MAYBE
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome()
#輸入你要的商品的pchome網址
login_url ='https://ecvip.pchome.com.tw/login/v3/login.htm'  
items_url ='https://24h.pchome.com.tw/prod/DGBJCW-A900BCGGE?fq=/S/DGBJGD'
PS5_url1 = 'https://24h.pchome.com.tw/prod/DGBJG9-A900B51SM?fq=/S/DGBJG9' #PS5光碟版 7/9 12:00 pm
PS5_url2 = 'https://24h.pchome.com.tw/prod/DGBJG9-A900B51SS?fq=/S/DGBJG9' #PS5數位版 7/9 12:00 pm

""" 登入 """
driver.get(login_url)
#輸入帳號
button_login = driver.find_element_by_id('loginAcc')
button_login.send_keys('daniel378158@gmail.com')  #輸入你的帳號

WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'loginPwd'))) 

#輸入密碼
button_passwd = driver.find_element_by_id("loginPwd")
button_passwd.send_keys('daniel0721') #輸入你的密碼

driver.find_element_by_id('btnLogin').click() #點擊登入鍵
time.sleep(4) #等待

""" 引導進商品頁面 """
#driver.get(items_url)
driver.get(PS5_url1)


isComplete = False

#等待加入購物車鍵出現
while not isComplete:
    # find add to cart button
    try:
        atcBtn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//li[@id="ButtonContainer"]/button'))
        )
    except:
        time.sleep(3)
        driver.refresh()
        continue #持續重新整理頁面直到加入購物車鍵出現

    print("Add to cart button found")

    try:
        # add to cart
        atcBtn.click() 
        time.sleep(0.2)

        checkoutBtn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "check"))
        )
        checkoutBtn.click()
        print("Successfully added to cart - beginning check out")

        payment = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//li[@class='CC']/a[@class='ui-btn']")) #一次付清
        )
        payment= driver.execute_script("arguments[0].click();", payment)
        print("Successfully added to cart - beginning check out")

        try: #pchome有些商品會出現"訂單不受24小時到貨時間限制"的提示，如果出現點擊繼續，沒出現就繼續最後一步驟
            WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//a[@id='warning-timelimit_btn_confirm']"))
                )
            button_hint = driver.find_element_by_xpath("//a[@id='warning-timelimit_btn_confirm']")
            driver.execute_script("arguments[0].click();", button_hint)
        except:
               pass

        # fill in card cvv
        cvvField = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="multi_CVV2Num"]'))
        )
        cvvField.send_keys('068')
        print("Attempting to place order")

        # place order
        placeOrderBtn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="btnSubmit"]'))
        )
        placeOrderBtn.click()

        isComplete = True
    except:
        # make sure this link is the same as the link passed to driver.get() before looping
        driver.get(PS5_url1)
        print("Error - restarting bot")
        continue

print("Order successfully placed")

