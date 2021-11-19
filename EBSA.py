import time
import os
import datetime
import glob
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.file_detector import LocalFileDetector
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException
from graph import get_info_marketer

now = datetime.datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
logging.basicConfig(
    filename=f'logs{now}.log', format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)
errors = []
def write_error(e, numero_cuenta):
    logging.error(
        f'A ocurrido el error: {e} durante la descaga del archivo {numero_cuenta}')
    errors.append(numero_cuenta)

def change_file_name(download_directory, numero_cuenta):
    files_path = os.path.join(download_directory, '*')
    files = sorted(
        glob.iglob(files_path), key=os.path.getctime, reverse=True)
    os.rename(files[0], f'{download_directory}/{numero_cuenta}.pdf')
def create_driver(url, download_directory, actual_directory):
    prefs = {'download.default_directory': f'{download_directory}',
             'download.prompt_for_download': False,
             'plugins.always_open_pdf_externally': True}
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=options)
    driver.file_detector = LocalFileDetector()
    driver.get(url)
    driver.maximize_window()
    return driver
def enter_info_ebsa(driver, download_directory, numero_cuenta):
    try:
        # ingresar info cuenta
        logging.info(
            f'Iniciando proceso de descarga de la cuenta: {numero_cuenta}')
        numClienteFact = driver.find_element(By.ID,'ndc')
        numClienteFact.click()
        numClienteFact.clear()
        numClienteFact.send_keys(f'{numero_cuenta}')
        logging.info(f'Cargando pagina para descargar factura')
        driver.implicitly_wait(5)
        # buscar factura a descargar
        time.sleep(5)
        driver.implicitly_wait(5)
        buttonBrowseAccount = driver.find_element(By.XPATH,'//*[@id="ndc"]').click()
        envio = driver.find_element(By.XPATH,'//*[@id="ndc"]').send_keys({numero_cuenta})
        #Descargar factura
        time.sleep(10)
        buttonDownload = driver.find_element(By.NAME).click()
        time.sleep(5)
        logging.info(f'la factura se descargo exitosamente')
        driver.implicitly_wait(5)
    except NoSuchElementException as e:
        write_error(e, numero_cuenta)

    except ElementNotInteractableException as e:
        write_error(e, numero_cuenta)

    except ElementClickInterceptedException as e:
        write_error(e, numero_cuenta)

    except Exception as e:
        write_error(e, numero_cuenta)

    except KeyboardInterrupt as e:
        logging.info(
            f'El flujo a finalizado por parte del usuario usando: {e}')
        logging.info(
            f'Flujo finalizado con {len(errors)} errores en la descarga de facturas\n {errors}')
        driver.close()
        exit()
if __name__=='__main__':
    logging.info(f'Iniciando proceso fecha:{now}')
    actual_directory = os.getcwd()
    new_dir = f'downloads_{now}'
    os.mkdir(new_dir)
    download_directory = f'{actual_directory}\{new_dir}'
    logging.info(f'creacion carpeta{download_directory}')
    url='https://www.ebsa.com.co/servicios-ebsa/factura/?acc=consulte'
    logging.info(f'Apertura webdriver Selenium')
    driver = create_driver(
        url=url, download_directory=download_directory, actual_directory=actual_directory)
    logging.info(f'Leyendo query de facturas')
    df = get_info_marketer()
    logging.info('lectura correcta')
    time.sleep(1)
    for i in df:
        numero_cuenta = i['account_name']
        enter_info_ebsa(driver, download_directory, numero_cuenta)
        driver.get(driver.current_url)
    driver.close()
    logging.info(
        f'Flujo finalizado con {len(errors)} errores en la descarga de facturas\n {errors}')