import traceback
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from shutil import which
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy_selenium import SeleniumRequest

S0_options = []
S1_options = []
S2_options = []
S3_options = []
S4_options = []

burned_list = []

# S0_burned = []
# S1_burned = []
# S2_burned = []
# S3_burned = []
# S4_burned = []

# burned_options = []

# options_in_reserve = S0_options + S1_options + S2_options
# + S3_options + S4_options

def test():
    S0_options = ['asd']
    S1_options = ['asdasd']
    S2_options = []
    S3_options = []
    S4_options = []

    S0_burned = []
    S1_burned = []
    S2_burned = []
    S3_burned = []
    S4_burned = []

    options_in_reserve = S0_options + S1_options + S2_options
    + S3_options + S4_options

    while options_in_reserve:
        print(options_in_reserve.pop(-1))



def ebay_var_prod(driver):
    '''selección or selection is a variable, like color, GB
    option is an option of that seelction, like yellow or 32GB '''

    global S0_options
    global S1_options
    global S2_options
    global S3_options
    global S4_options

    burned_options = []
    # result with a list of lists with each price for each combination
    prod_var_price = []

    #identify variables to select, like color, capacity
    variables = driver.find_elements_by_xpath('//select[@class="msku-sel "]')
    len_var = len(variables) # to use later in get_price()
    #it points in which Selection index is the script, begins in 0
    var_index = 0
    #lists for available options in each selection

    options_in_reserve = ['0'] # 0= initilizer, to make run the loop, it's deleted in the 1º iteration
    while options_in_reserve: #mientras haya opciones disponibles en alguna selección:
        options_in_reserve.pop(0) #pop the initilizer to be able to stop it
        for variable in variables:
            sleep(2)
            my_click(id=variable,type='web_element')
            sleep(2)
            #if var_index = 0, we know that the script is in S0, so append to list options_S0
            get_available_options(variable,var_index)
            select_option(var_index,variables)
            variables_and_price = get_price(var_index,len_var)
            print("This are the variables and its price:",variables_and_price)
            #append this to a list with all options and prices
            prod_var_price.append(variables_and_price)
            # get price                        
            var_index += 1
    for prod in prod_var_price:
        print(prod)
        
    return prod_var_price
    #get price
    #RESTart function, inside while

    ##identify the 1º one
    # first_variable = variables[0]

    # #click it to see options
    # my_click(id=first_variable,type='web_element')

    # #identify AVAILABLE options from variables, like, yellow, grey, or 64G
    # options_from_first = check_available(first_variable)

    # var_index = 0
    # #for loop iterating each option
    # for option in options_from_first:

    #     #use the fxunciton to see availables
    #     options_from_first[var_index]

    #     var_index += 1

def get_price(var_index, len_var):
    # total select   var_index = no following select = get price
    options_and_price = []

    if var_index == len_var: #meaning the actual index = maximum = there's no more select below this, time to take price
        #identify the variables, selections in ebay
        variables = driver.find_elements_by_xpath('//select[@class="msku-sel "]')
        for var in variables: #for each variable extract the active option
            option = var.find_element_by_xpath('.//option[@selected="selected"]')
            options_and_price.append(option)#append the option to a list
    
    #get the price, append to the list,
    price = driver.find_element_by_xpath('//div[@id="vi-mskumap-none"]/span').text
    options_and_price.append(price)
    
    return options_and_price

def select_option(var_index,variables):

    global S0_options
    global S1_options
    global S2_options
    global S3_options
    global S4_options
    global burned_list
    
    #seelct an options based on given var_index
    if var_index == 0:
        option = S0_options.pop(4)
        #my_print('going to click in var 0')
        #sleep(3)
        #my_click(id=variables[0],type='web_element')
        #my_print("clicked in var 0")
        #sleep(2)

        #my_print('going to hoover var0')
        #ActionChains(driver).move_to_element(variables[0]).perform()
        print("hoover donde")
        sleep(3)
    if var_index == 1:
        option = S1_options.pop()
        
    #click the option, pop it from options and add it to burned
    sleep(1)
    burned_list.append(option)

    #driver.execute_script("arguments[0].scrollIntoView();", option)
    # while option.is_displayed():
    #     driver.execute_script("window.scrollBy(0, 250)")
    #if not option.is_displayed(): # if the option doesn't show up in the screen
#    ActionChains(driver).click_and_hold(variables[0]).perform()

    # action = ActionChains(driver)
    # action.move_to_element(option).perform()
    # print("moved to option")
    print("Going to click",option.text)
    my_click(id=option,type='web_element')


def get_available_options(element,var_index):
    ''' this uses a ebay select tag and return available options
    tags for that select tag'''

    global S0_options
    global S1_options
    global S2_options
    global S3_options
    global S4_options

    options = element.find_elements_by_xpath('.//option[not(@class="outofstock")]')
    #findElement(By.tagName,'outofstock')

    availables = []
    for option in options: # if product doesn't have "No hay existencias = available"
        if "No hay existencias" not in option.text:
            if var_index == 0: # append options based on variable_index
                S0_options.append(option)
                print("append to S0",option.text)
            elif var_index == 1:
                S1_options.append(option)
                print("append to S1",option.text)
            elif var_index == 2:
                S2_options.append(option)
                print("append to S2",option.text)
            elif var_index == 3:
                S3_options.append(option)
                print("append to S3",option.text)
            elif var_index == 4:
                S4_options.append(option)
                print("append to S4",option.text)

#type xp if you want target by xpath, css taget by css, id = css/xpath identifier
def my_click(id, type='xp'):
    '''Uses action chains to click
    requiered xpath by default, type=css to use css, web_element...'''

    from selenium.webdriver.common.action_chains import ActionChains
    #from selenium.webdriver.chrome.webdriver import WebDriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.common.exceptions import TimeoutException


    # from selenium import webdriver
    # #in linux
    # chrome_path =  '/home/kv/Desktop/python_scripts/chromedriver_linux64/chromedriver'
    # driver = webdriver.Chrome(executable_path=chrome_path)#, options=options)

    if type == 'xp':
        wait = WebDriverWait(driver,12)
        target = wait.until(
        EC.element_to_be_clickable((By.XPATH, id)))

        try:
            #target.click()
            actions = ActionChains(driver)
            actions.move_to_element(target).click().perform()
        # except TimeoutException as e:
        #     print("THIS IS TIMEOUT EXCEPTION")
        #     print(e)
        except:
            try:
                print("going to normal")
                target.click()
            except Exception as e:
                traceback.print_exc()


    elif type == 'css':
        wait = WebDriverWait(driver,12)
        target = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, id)))


    elif type == 'web_element':

        #using the raw web element passed in args(id) as target
        target = id

        try:
            #target.click()
            actions = ActionChains(driver)
            actions.move_to_element(target).click().perform()
        # except TimeoutException as e:
        #     print("THIS IS TIMEOUT EXCEPTION")
        #     print(e)
        except Exception as e:
            traceback.print_exc()


def my_print(text, color='green', mode='normal',**id):
    ''' red,green,yellow,blue // mode="lines" to print a list line by line in BLUE"'''

    # IMPORTS
    from colorama import init
    from termcolor import colored
    init()


    if mode == 'normal':
        if color == 'red':
            print(colored(id, 'white','on_red'))
            print(colored(text, 'white','on_red'))

        elif color == 'green':
            print(colored(id, 'white','on_green'),sep="\n")
            print(colored(text, 'white','on_green'),sep="\n")

        elif color == 'yellow':
            print(colored(id, 'blue','on_yellow'))
            print(colored(text, 'blue','on_yellow'))

        elif color == 'blue':
            print(colored(id, 'white','on_blue'))
            print(colored(text, 'white','on_blue'))

    elif mode=='lines':

        for item in text:
            print(colored(item, 'white','on_blue'))


driver_path = "C:\\Users\\HP EliteBook\\OneDrive\\A_Miscalaneus\\Escritorio\\Code\\Spiders\\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument("--window-size=1920, 1200")

driver = webdriver.Chrome(executable_path=driver_path, options=options)
driver.set_window_size(1920, 1080)
driver.get('https://www.ebay.es/itm/224351242649?_trkparms=ispr%3D1&hash=item343c604999:g:6G4AAOSwkxhgxOF1&amdata=enc%3AAQAGAAACkPYe5NmHp%252B2JMhMi7yxGiTJkPrKr5t53CooMSQt2orsSK%252B2M%252Ffp5X4rboLTBP5niNbTv1ywJWOYsoKlq6xFU0PRClyha9SSFgtTPHFGcaPKryyzusvo5I9qE2vPrKqU9oT7kaK2KKCyefKNr1Mq9DuOpAMwYgmT3iwZ2eIXn6N7DqKM7F%252BfsX7hsdVJAALBuklC%252F%252B94lWyZBcc9f4pPHrVzBJta0bc8QJVOmeGEpbAXFXDo03LkncmdPzdt51RftsYXch3c64iej6fNgm6NwCFRHZjNduV3tCvxabZpolgmyRhyCUpyyFSQ%252FJDdEZC%252Fki4jFjEtqyzee%252FemCo7xCfzIVjuI7rEvZEvFpICSf9emJvNYHN3seH3%252BgdKkFniUM141Odjvn2sp4dTpXB3hU9HtyMtj%252FjS68jpeGQcBrqJcqw%252FTDz%252BxKcU9xj2tcAnhoHFc4I%252FeKvYFt04iPfeX%252FOtiiD1XOGGMedn2TaqbsQnh2yucwfFs5q3cnRKGpsJ7QTa881lE6ICi1exhLRJ8RyywnUoXGll3wiVOkS2MVuJTOV5s8QZpA9K4wYjqHvcTPr7A4Tx89nbgPCS4%252B06IAZLyB8e5vBub1K4rM%252FLblUQTND3nw75Q6mTk0PLAY4%252FX9dx3nKcZbRWhSre6o%252FGjn1fv9FmASf8i7uo7gWtLVSzNIrW9TqOJKotDWSORar%252F74xHAwmfDURu7R2fvObLMSJuoIS7nlESyOjYqFBLxFknNm0S0SJXv31B95rRSvtc08%252BIGVWtSNFkyw7NtBpAEbs9ZlxCix67p1qsdnl3TtGiEdYbxgG7uBF%252FFwTAf%252FmvJqTtEwSBqBOwpTyKwCoG2V6mize4tyec%252F3X9akprUBMbdo%7Campid%3APL_CLK%7Cclp%3A2499334&var=523272874125')
driver.maximize_window()

# driver.get(driver.current_url)
# sleep(2)
# driver.refresh()
sleep(2)
try:
    my_click(type='xp',id='//button[@id="gdpr-banner-accept"]')
except:
    pass

ebay_var_prod(driver)