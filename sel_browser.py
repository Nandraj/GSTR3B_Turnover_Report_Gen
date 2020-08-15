from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
from dialog import getCaptcha


def login_to_GST_Portal(client_data, mysqldb):
    browser = webdriver.Chrome()
    browser.get('https://services.gst.gov.in/services/login')
    browser.maximize_window()
    browser.implicitly_wait(30)
    for data in client_data:
        try:
            name = data[1]
            gstin = data[2]
            userid = data[3]
            password = data[4]
            id_box = browser.find_element_by_id("username")
            id_box.clear()
            id_box.send_keys(userid)
            pswd_box = browser.find_element_by_id("user_pass")
            pswd_box.clear()
            pswd_box.send_keys(password)
            capcha_box = browser.find_element_by_id("captcha")
            capcha_box.clear()
            captcha_text = getCaptcha()
            if captcha_text == "":
                captcha_text = getCaptcha()
            capcha_box.send_keys(captcha_text)
            login_button = browser.find_element_by_xpath(
                "/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/form/\
                div[6]/div/button")
            login_button.click()
            time.sleep(7)
            #################################################################
            # GSTR-3B Processing
            # click on return dashboard btn
            # browser.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/\
            #     div[2]/div/div[1]/div[3]/div/div[1]/button/span").click()
            # time.sleep(7)
            year = "2019-20"
            month_list = ['April', 'May', 'June', 'July', 'August',
                          'September', 'October', 'November', 'December', 'January',
                          'February', 'March']
            for month in month_list:
                month_db_data = mysqldb.query2(
                    "SELECT * FROM gstr3b_data WHERE gstin=? AND month=? ", (gstin, month))
                if len(month_db_data) == 0:
                    # services click
                    browser.find_element_by_xpath(
                        '//*[@id="main"]/ul/li[2]/a').click()
                    # returns click
                    browser.find_element_by_xpath(
                        '//*[@id="main"]/ul/li[2]/ul/li[4]/a').click()
                    time.sleep(7)
                    browser.find_element_by_xpath(
                        '/html/body/div[2]/div[2]/div/div[2]/div[2]/div/div/ul/li[1]/a').click()
                    time.sleep(7)
                    year_select = Select(browser.find_element_by_xpath(
                        '/html/body/div[2]/div[2]/div/div[2]/div[2]/form/div/div[1]/select'))
                    year_select.select_by_visible_text(year)
                    time.sleep(2)
                    month_select = Select(browser.find_element_by_xpath(
                        '/html/body/div[2]/div[2]/div/div[2]/div[2]/form/div/div[2]/select'))
                    month_select.select_by_visible_text(month)
                    search_btn = browser.find_element_by_xpath(
                        "/html/body/div[2]/div[2]/div/div[2]/div[2]/form/div/div[3]/button")
                    search_btn.click()
                    time.sleep(7)
                    view_3b = browser.find_element_by_xpath(
                        "/html/body/div[2]/div[2]/div/div[2]/div[3]/div[3]/div[2]/div[1]/div/div[2]/div/div[1]/button")
                    view_3b.click()
                    time.sleep(7)
                    dialog_ok = browser.find_element_by_xpath(
                        '//*[@id="GSTR3bInfoModal"]/div/div/div[3]/button')
                    dialog_ok.click()
                    time.sleep(2)
                    table_31 = browser.find_element_by_xpath(
                        "/html/body/div[2]/div[2]/div/div[2]/div[1]/div[3]/div[8]/div/div[1]/a/div[1]/p")
                    if table_31.text == "3.1 Tax on outward and reverse charge inward supplies":
                        table_31.click()
                        time.sleep(5)
                        table_31_dialog_ok = browser.find_element_by_xpath(
                            '//*[@id="iosupAdvisory"]/div/div/div[2]/button')
                        table_31_dialog_ok.click()
                        time.sleep(3)
                        threeBData = browser.find_elements_by_tag_name("input")
                    else:
                        threeBData = ["0.00" for x in range(1, 16)]

                    def val(i):
                        if type(i) == str:
                            value = i
                        else:
                            value = i.get_attribute('value')
                            value = value.replace("₹", "").replace(
                                "'", "").replace(",", "")
                        return value

                    mysqldb.edit_insert("INSERT INTO gstr3b_data(gstin, name, month, \
                                        normal_sales, nor_igst, nor_cgst, nor_sgst, nor_cess, \
                                        export, exp_igst, exp_cess, exempt,\
                                        rcm_taxval, rcm_igst, rcm_cgst, rcm_sgst, \
                                        rcm_cess, non_gst)\
                                        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                                        (gstin,
                                         name,
                                         month,
                                         val(threeBData[0]),
                                         val(threeBData[1]),
                                         val(threeBData[2]),
                                         val(threeBData[3]),
                                         val(threeBData[4]),
                                         val(threeBData[5]),
                                         val(threeBData[6]),
                                         val(threeBData[7]),
                                         val(threeBData[8]),
                                         val(threeBData[9]),
                                         val(threeBData[10]),
                                         val(threeBData[11]),
                                         val(threeBData[12]),
                                         val(threeBData[13]),
                                         val(threeBData[14])))
            #################################################################
            # click on logout
            browser.find_element_by_xpath(
                "/html/body/div[1]/ng-include[1]/header/div[2]/div/div/ul/li/\
                div/a").click()
            time.sleep(3)
            browser.find_element_by_xpath(
                "/html/body/div[1]/ng-include[1]/header/div[2]/div/div/ul/li/\
                div/ul/li[5]/a").click()
            time.sleep(7)
            # click on login link
            browser.find_element_by_xpath(
                "/html/body/div[2]/div[2]/div[2]/div/div/div/div/div[2]/p/\
                a").click()
            time.sleep(7)
            mysqldb.edit_insert(
                "UPDATE client_data SET processed = ? WHERE gstin = ?",
                ("yes", gstin))
        except Exception as e:
            print(e)
            browser.get('https://services.gst.gov.in/services/login')
            browser.maximize_window()
            browser.implicitly_wait(30)
    browser.close()
