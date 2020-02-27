import requests, os, string
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
import glob
import numpy as np
from config import user, user_pass

chromeOptions = Options()
chromeOptions.add_experimental_option("prefs", {"download.default_directory": r"C:\Users\alexi\OneDrive\Documents\Phone Orders\OrderSheetRawExcel"})

def get_sheet():
    cpath = "C:\Users\alexi\Onedrive\chromedriver.exe"
    url = "http://www.myrtpos.com/newbdi/index.fwx"
    driver = webdriver.Chrome(cpath, options=chromeOptions)
    driver.get(url)

    driver.find_element_by_id('secUserID').send_keys(user)
    driver.find_element_by_id ('secPassword').send_keys(user_pass)
    driver.find_element_by_class_name('submit').click()

    order_url = 'http://www.myrtpos.com/newbdi/ReorderReport_Calculated_Week2.fwx'
    response = driver.get(order_url)

    markets = ["ORLANDO", "TAMPA", "KANSAS CITY"]
    # market = input(f'')
    market = "ORLANDO"


    select = Select(driver.find_element_by_id('frmMarketID'))
    # select by value 
    select.select_by_value(market)
    select = Select(driver.find_element_by_name('frmSerialized'))
    # select by value 
    select.select_by_value('Yes')

    driver.find_element_by_id("chkByStore").click()
    driver.find_element_by_id("chkAllInv").click()
    buttons= driver.find_elements_by_class_name("button-inner") # Selects Both "Generate" and "Raw Excel" Buttons


    # Need to Generate file and wait until finished
    buttons= driver.find_elements_by_class_name("button-inner")
    buttons[0].click()
    time.sleep(5)

    # Need to download file and wiat until finished
    buttons= driver.find_elements_by_class_name("button-inner")
    buttons[1].click() # Raw Excel Download
    time.sleep(5)


    driver.quit() # Close Chrome Driver   

get_sheet()


# Get latest File
list_of_files = glob.glob('OrderSheetRawExcel/*') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)

orl = pd.read_excel(f"{latest_file}")
orl_df = orl[["itmdesc", "orderqty"]]
sums = orl_df.groupby("itmdesc").sum()


sums = sums.replace(0, np.nan)
sums = sums.dropna(how='all', axis=0)


allocations= []
for i, j in sums.iterrows():
    answer = input(f"How much of {i} were we allocated?")
    allocations.append(answer)

sums['allocation'] = allocations
sums = sums.astype({'orderqty':float,'allocation':float})
sums['order_percent'] = sums['orderqty']/sums['allocation']
sums = sums[['order_percent']]
full_order_sheet = orl.set_index("itmdesc")
new_sheet = pd.merge(full_order_sheet, sums, on='itmdesc', how='left')
new_sheet = new_sheet[['company','qty','onorderqty','orderqty','totsold7','totsold14','totsold30','order_percent']]
new_sheet["request"]=new_sheet["orderqty"]/new_sheet["order_percent"]
new_sheet["totalqty"]=new_sheet[['qty','onorderqty','orderqty','request']].sum(axis=1)
new_sheet['weeksworth'] = new_sheet['totalqty']/new_sheet['totsold7']
calculated_sheet=new_sheet[['company','qty','onorderqty','orderqty','request','totalqty','weeksworth','totsold7','totsold14','totsold30','order_percent']]
calculated_sheet.round({"orderqty":0,"request":0,"weeksworth":2})


#Save file
calculated_sheet.to_excel("test_orlando.xlsx", sheet_name="orlando", index=True)