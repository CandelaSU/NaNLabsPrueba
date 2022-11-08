from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests as rq
import json
from threading import Thread, Barrier 
import pandas as pd

start=time.perf_counter()
options=webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')
driver_path='./NaNLabs/chromedriver'
fil = open('NaNLabs\\listado.txt','a')
fil.write('creo el archivo\n')
fil.close()
#salida=pd.DataFrame(columns=['primer','segunda','tercera','cuarta'])
def multi(threads): 
    driver=webdriver.Chrome(driver_path,chrome_options=options)
#    salida=pd.DataFrame(columns=['primer','segunda','tercera'])
    driver.get('https://transparency-in-coverage.uhc.com')
    #print('driver leido-(tiene que ser uno solo)')
    WebDriverWait(driver,120)\
        .until(EC.element_to_be_clickable((By.XPATH,'/html/body/div/section/main/div/div/div/ul/li[1]')))
    print('ya cargo el webdriverwait (x)')
    elementXPath = driver.find_elements(By.XPATH,
                            "//*[@id='root']/section/main/div/div/div/ul/li[@class='ant-list-item']/div/div[2]/a"
                            ) #regex del final index.json
    #print('tiene el elementXpath')
    #print(len(elementXPath))
    fil = open('NaNLabs\\listado.txt','a')
    print('abrio el archivo')
    for a in elementXPath:
        titulo = a.get_attribute('text')
        if titulo.endswith('index.json') :
            data = json.loads(rq.get(a.get_attribute('href')).text)      
            for i in range(0,len(data['reporting_structure'][0]['in_network_files']),1):
                fil.write(f"{data['reporting_structure'][0]['reporting_plans'][0]['plan_name']} , {data['reporting_structure'][0]['in_network_files'][i]['location']} , {data['reporting_structure'][0]['reporting_plans'][0]['plan_id']}\n")
    fil.write('termino de cargar el archivo')
    fil.close()

#    print(salida)
#    return salida



numero_multitarea=6
barrier=Barrier(numero_multitarea)
threads=[]


#multi(threads)

for _ in range(numero_multitarea):
    i = Thread(target=multi, args=(barrier,))
    i.start()
    threads.append(i)

for i in threads:
    i.join()

finish=time.perf_counter()
print(f'Finished in {round(finish-start,2)} second(s)')
#print(salida)