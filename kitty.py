from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import os
from csv import writer



# Run chrome web driver
option=webdriver.ChromeOptions()
path=os.path.dirname(os.path.abspath(__file__)) 
driver=webdriver.Chrome(path+"\\chromedriver")
driver.maximize_window()
driver.get("https://kittyhelper.co/kitty-rarity-factors/")
time.sleep(1)

#Default start number
start_number = "818294"
end_number = "818314"

loop_count = int(end_number) - int(start_number)

for loop_id in range(loop_count):

    cat_id = str(int(start_number) + loop_id)
    insert_row = []
    insert_row.append(cat_id)

    # Input search kitty ids.
    start_number_input = driver.find_elements_by_name('kittyid')
    search_button = driver.find_element_by_class_name('btn.btn-success')

    start_number_input[0].send_keys(cat_id)
    time.sleep(1)

    # Click search button to search inputed id Kitty.
    search_button.click()
    time.sleep(1)

    # Check Sale badge   
    sale = "Yes"
    sell_value = ""

    try:
        sale_badge = driver.find_element_by_class_name('badge.bg-green.badge-price')
        sell_value = sale_badge.text
        sell_value = sell_value.replace("For sale ", "")
    except NoSuchElementException:
        sale = "No"
   
    insert_row.append(sale)
    insert_row.append(sell_value)

    pp_table_dom = driver.find_element_by_id('tab_content-1')
    n_summary_count = 0
    summary_value = ""
    try:
        p_table_dom = pp_table_dom.find_elements_by_class_name("row")
        if len(p_table_dom):
            insert_row.append("")
        else:
            p_table_dom = pp_table_dom.find_elements_by_class_name("x_content")
            table_dom = p_table_dom[0].find_elements_by_class_name("table-responsive")
            table = table_dom[0].find_elements_by_tag_name("table")

            trs = table[0].find_elements_by_tag_name("tr")
            trcount = len(trs)
            tmp_summary_value = 0.0
            for i in range(trcount):
                if i > 0:
                    tds = trs[i].find_elements_by_tag_name("td")
                    tmp_value = tds[1].text
                    if tmp_value.find(" ETH") > -1:
                        tmp_value = tmp_value.replace(" ETH", "")
                        tmp_summary_value += float(tmp_value)
            tmp_summary_value = round(tmp_summary_value, 2)
            summary_value = str(tmp_summary_value) + " ETH"
            if tmp_summary_value < 0.2:
                summary_value = ""
            insert_row.append(summary_value)
    except NoSuchElementException:
        print("ok")
        

    # Save row data to csv file
    with open('data.csv', 'a+', newline='') as write_obj:
         csv_writer = writer(write_obj)
         csv_writer.writerow(insert_row)







