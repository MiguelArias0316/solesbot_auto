""" from selenium import webdriver """
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from iniciar_webdriver_uc import iniciar_webdriver
import time
from moneda import Moneda
# Navega a la página web
driver = iniciar_webdriver(headless=False)
wait = WebDriverWait(driver, 20)
driver.get('https://bot.solesbot.ai/login')

#Creamos un arreglo con las monedas
# Inicializamos la lista de Monedas
lista_monedas = [
    Moneda("CAKE/USDT",30,1.88,False),
    Moneda("Arbitrum/USDT",300,0.88,False),
    Moneda("VeChain/USDT",300,0.60,False),
    Moneda("Lido/USDT",300,0.65,False),
    Moneda("Cosmos/USDT",1000,0.88,False),
    Moneda("Filecoin/USDT",1000,0.55,False),
    Moneda("Fantom/USDT",100,1.68,False)
]
""" moneda1 = Moneda("CAKE/USDT",30,1.88,False)
moneda2 = Moneda("Arbitrum/USDT",300,0.88,False)
moneda3 = Moneda("VeChain/USDT",300,0.60,False)
moneda4 = Moneda("Lido/USDT",300,0.65,False)
moneda5 = Moneda("Cosmos/USDT",1000,0.88,False)
moneda6 = Moneda("Filecoin/USDT",1000,0.55,False)
moneda7 = Moneda("Fantom/USDT",100,1.68,False)
lista_monedas.append(moneda1)
lista_monedas.append(moneda2)
lista_monedas.append(moneda3)
lista_monedas.append(moneda4)
lista_monedas.append(moneda5)
lista_monedas.append(moneda6)
lista_monedas.append(moneda7) """

# Login de la pagina
    #Email
email_input = WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.ID, 'Email'))
    )
    # Limpia el campo y escribe en él
email_input.clear()
email_input.send_keys('test')
 #Password
password_input = WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.ID, 'Email'))
    )
    # Limpia el campo y escribe en él
password_input.clear()
password_input.send_keys('test')

#click botón de login
login_button = driver.find_element_by_id("login")
login_button.click()
#Resolver capchat con los indios
#Carlos de mierda

#Entrar a la sesión de arbitraje 
#Opcion 1
driver.get('https://bot.solesbot.ai/arbitrage/manual')
#Opcion 2
rocket_icon = driver.find_element_by_class(By.CLASS_NAME, "fa fa-rocket")
rocket_icon.click()

#Verificar saldo Available
def get_avalible(driver):
    avalible = driver.find_element(By.CLASS_NAME, 'notranslate ng-binding')
    avalible_text = avalible.text
    avalible_number = float(avalible_text.replace('USDT','').strip())
    return avalible_number

def check_avalible():    
    while True:
        try:
            monedaOperar = None
            opcion_encontrada = None
            saldo_avalible = get_avalible(driver)
            if saldo_avalible >= 1030:
                for moneda in lista_monedas:
                     if moneda.Estado == False:
                          monedaOperar=moneda   
                     break
                select_element = driver.find_element(By.CSS_SELECTOR, 'input[ng-model="coin"]')

                for option in select_element.options:
                    if option.text == monedaOperar.NombreMoneda:
                        opcion_encontrada = option
                        break
                opcion_encontrada.click()
                time.sleep(5)
                roi_moneda = driver.find_element(By.CSS_SELECTOR, 'input[ng-model="suggestion.profit"]')
                roi_moneda_texto = roi_moneda.text
                roi_float = float(roi_moneda_texto)

                if roi_float == monedaOperar.ROI:
                    #Click en el boton Execute
                    execute_button = driver.find_element(By.CSS_SELECTOR, '.withdraw__con__btn button')
                    execute_button.click()
                    #Ingresar el monto
                    amount_input = driver.find_element(By.CSS_SELECTOR, 'input[ng-model="amount"]')
                    amount_input.clear()
                    amount_input.send_keys(monedaOperar.Monto)
                    #Confirmar operación
                    confirm_button = driver.find_element(By.CSS_SELECTOR, 'submitSuggestion(true)')
                    confirm_button.click()
                    #Cambiar estado de la moneda a operada
                    monedaOperar.Estado = True
                    break
                break
            else:
                time.sleep(5) #esperar 10 segundos para volver a intentar  
        except Exception as e:
            print("error diego es gay")
        break

check_avalible()


""" # Espera hasta que el select de monedas esté presente y selecciona la moneda deseada
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'select[ng-model="coin"]'))
)
select_coin = Select(driver.find_element(By.CSS_SELECTOR, 'select[ng-model="coin"]'))
select_coin.select_by_visible_text('CAKE/USDT')

# Encuentra el ROI más alto (1.88 en este caso)
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[ng-model="suggestion.profit"]'))
)
roi_input = driver.find_element(By.CSS_SELECTOR, 'input[ng-model="suggestion.profit"]')

# Verifica que el ROI sea 1.88
roi_value = float(roi_input.get_attribute('value'))
if roi_value == 1.88:
    # Selecciona el monto
    amount_input = driver.find_element(By.CSS_SELECTOR, 'input[ng-model="suggestion.buy.price"]')
    amount_input.clear()
    amount_input.send_keys('300')

    # Haz clic en el botón Execute
    execute_button = driver.find_element(By.CSS_SELECTOR, '.withdraw__con__btn button')
    execute_button.click()
else:
    print("El ROI no es 1.88")

# Espera unos segundos para ver el resultado
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.modal'))
) """

# Cierra el navegador
""" driver.quit() """