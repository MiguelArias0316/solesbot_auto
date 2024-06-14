
import time
import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from moneda import Moneda
from datetime import datetime
import openpyxl
import keyboard

# Inicializa las variables
usernametxt = None
passwordtxt = None
lista_monedas_principal = []
lista_monedas_ronda1 = []
lista_monedas_ronda2 = []
lista_monedas_ronda3 = []

# Abre el archivo en modo de lectura
with open("config.txt", "r") as archivo:
    # Lee cada línea del archivo
    for linea in archivo:
        # Divide cada línea en clave y valor usando el signo '=' como separador
        clave, valor = linea.strip().split("=")

        # Asigna los valores correspondientes a las variables
        if clave == "username":
            usernametxt = valor
        elif clave == "password":
            passwordtxt = valor
        elif clave == "lista_monedas_principal":
            lista_monedas_principal = eval(valor)
        elif clave == "lista_monedas_ronda1":
            lista_monedas_ronda1 = eval(valor)
        elif clave == "lista_monedas_ronda2":
            lista_monedas_ronda2 = eval(valor)
        elif clave == "lista_monedas_ronda3":
            lista_monedas_ronda3 = eval(valor)

# Convertir las listas cargadas en instancias de la clase Moneda
lista_monedas_principal = [Moneda(*moneda) for moneda in lista_monedas_principal]
lista_monedas_ronda1 = [Moneda(*moneda) for moneda in lista_monedas_ronda1]
lista_monedas_ronda2 = [Moneda(*moneda) for moneda in lista_monedas_ronda2]
lista_monedas_ronda3 = [Moneda(*moneda) for moneda in lista_monedas_ronda3]

# Cargar el libro de trabajo existente
libro = openpyxl.load_workbook("pruebaSoles.xlsx")
hoja = libro.active

moneda_operar = None # Variable global para almacenar la moneda a operar

# Función para mostrar un cuadro de diálogo con opciones Sí/No.
def ask_yes_no():
    root = tk.Tk()
    root.withdraw()  
    
    result = messagebox.askyesno("Question", "Do you want to continue?")

    root.destroy()

# Ruta al ejecutable de chromedriver
driver_path = r'C:\Users\Arias\Downloads\chromedriver-win64\chromedriver.exe'  # Update this path to where your chromedriver is located

# Inicializa las opciones de Chrome
options = webdriver.ChromeOptions()

# Configura el servicio de ChromeDriver
service = Service(executable_path=driver_path)

# Crea una nueva instancia del controlador de Chrome con las opciones especificadas
driver = webdriver.Chrome(service=service, options=options)

# Navega a la página de inicio de sesión
driver.get('https://bot.solesbot.ai/login')

""" ask_yes_no() """

# Localiza el campo de nombre de usuario usando su atributo ID
""" username = driver.find_element(By.ID, 'Email') """
try:
 wait = WebDriverWait(driver, 300)
 username = wait.until(EC.presence_of_element_located((By.ID, 'Email')))
except Exception as e:
    print(f"Error: {e}")

# Localiza el campo de contraseña usando su atributo ID
password = driver.find_element(By.ID, 'Password')

# Ingresa el nombre de usuario  
username.send_keys(usernametxt)
""" username.send_keys('ariasmiguel0316@gmail.com') """

# Ingresa la contraseña
password.send_keys(passwordtxt)
""" password.send_keys('MiguelAri1234*') """

# Opción para enviar el formulario
""" password.send_keys(Keys.RETURN) """

# Localiza y hace clic en el botón de inicio de sesión
login_button = driver.find_element(By.CLASS_NAME, 'theme-btn')
login_button.click()

# Call the function to display the pop-up
ask_yes_no()

# Espera unos segundos para ver el resultado (no recomendado para código de producción)

driver.get('https://bot.solesbot.ai/arbitrage/manual')


# Localiza y hace clic en el icono del ojo para mostrar el saldo
eye_icon = driver.find_element(By.CSS_SELECTOR, 'i.fa.fa-eye.cursor-pointer[ng-click="showBalance()"]')
eye_icon.click()

time.sleep(2)# Espera 2 segundos

# Verificar saldo Available
def get_available_balance(driver):
    try:
        # Encuentra el elemento correspondiente al balance disponibl
        available_element = driver.find_element(By.XPATH, '//div[contains(@class, "pnl__single__box")][p[contains(text(), "Available")]]/h4[contains(@class, "notranslate ng-binding")]')
        currency = available_element.find_element(By.XPATH, './/span[contains(@class, "notranslate")]').text
        balance_text = available_element.get_attribute('innerText').replace(currency, '').strip()
        available_number = float(balance_text.replace(',', ''))
        return available_number
    except Exception as e:
        print(f"Error getting available balance: {e}")
        return 0.0

# Verificar saldo en operación
def get_balance_operando(driver):
    try:
        # Encuentra y hace clic en el icono del cohete
        """ rocket_icon = driver.find_element(By.CSS_SELECTOR, 'fa fa-rocket')
        rocket_icon.click() """
        """ driver.refresh() """
        driver.get('https://bot.solesbot.ai/arbitrage/manual')
        time.sleep(2) 
        # Muestra el balance en operación
        eye_icon = driver.find_element(By.CSS_SELECTOR, 'i.fa.fa-eye.cursor-pointer[ng-click="showBalance()"]')
        eye_icon.click()
        # Encuentra el elemento correspondiente al balance en operación
        operation_element = driver.find_element(By.XPATH, '//div[contains(@class, "pnl__single__box")][p[contains(text(), "Balance in Operation")]]/h4[contains(@class, "ng-binding")]')
        currency = operation_element.find_element(By.XPATH, './/span[contains(@class, "notranslate")]').text
        balance_text = operation_element.get_attribute('innerText').replace(currency, '').strip()
        
        operation_number = float(balance_text.replace(',', ''))
        return operation_number
    except Exception as e:
        print(f"Error getting balance in operation: {e}")
        return 1.0

# Obtiene el saldo disponible
saldo_available = get_available_balance(driver)
# Obtiene el saldo en operación
""" saldo_en_operacion = get_balance_operando(driver) """

# Función para verificar el saldo disponible y determinar la moneda a operar.
def check_avalible_balance(continue_checking):    
    while continue_checking:
        try:
            saldo_available = get_available_balance(driver)
            for moneda in lista_monedas_principal:
                if moneda.Estado == False:
                  continue_checking= False
                  return moneda           
        
        except Exception as e:
            print("error ")
        break

# Función para verificar el ROI de cada moneda y ejecutar operaciones.
def check_roi_by_coin(lista_operar, moneda_principal,listaActual):
                polanco = True # Bucle de control para la operación
                hora_actual = datetime.now()
                hora_formateada = hora_actual.strftime("%I:%M %p")
                print("_____________La ronda de "+ moneda_principal.NombreMoneda +" comenzo a las",hora_formateada)
                while polanco:
                     # Recorre cada moneda en la lista para operar                  
                    for moneda2 in lista_operar:
                        opcion_encontrada = None
                        # Si la moneda no ha sido operada aún
                        if moneda2.Estado != True:
                         wait = WebDriverWait(driver, 10)
                         select_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select[ng-model="coin"]')))
                         dropdown = Select(select_element)
                         # Buscar opción en el dropdown
                         for option in dropdown.options:
                            if moneda2.NombreMoneda !="CAKE/USDT":
                             if option.text.strip() == "CAKE/USDT":
                                opcion_encontrada = option
                                break
                            else:
                             if option.text.strip() == "Arbitrum/USDT":
                                opcion_encontrada = option
                                break
                        # Seleccionar la moneda encontrada
                         if opcion_encontrada:
                            opcion_encontrada.click()
                         else:
                            print(f'Opción {moneda2.NombreMoneda} no encontrada')
                         
                         time.sleep(1)
                         # Buscar y seleccionar la opción de la moneda deseada
                         for option in dropdown.options:
                            if option.text.strip() == moneda2.NombreMoneda:
                                opcion_encontrada = option
                                break
                         if opcion_encontrada:
                            opcion_encontrada.click()
                         else:
                            print(f'Opción {moneda2.NombreMoneda} no encontrada')
            
                         time.sleep(1)

                         # Obtener el ROI de la moneda
                         roi_moneda = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[ng-model="suggestion.profit"]')))
                         roi_moneda_texto = roi_moneda.get_attribute('value')
                         roi_float = float(roi_moneda_texto)
                         roi_moneda_texto = roi_moneda.text

                         # Comparar el ROI obtenido con el ROI deseado
                         if roi_float >= moneda2.ROI or (moneda2.NombreMoneda == "CAKE/USDT" and roi_float >= 1.80):
                            #Click en el boton Execute
                            execute_button = driver.find_element(By.CSS_SELECTOR, '.withdraw__con__btn button')
                            execute_button.click()

                            #Ingresar el monto
                            amount_input = driver.find_element(By.CSS_SELECTOR, 'input[ng-model="amount"]')
                            amount_input.clear()
                            valorAEchar = 0.0
                            
                            # Determinar el valor a operar
                            ultimo_dato = lista_operar[-1]
                            suma_montos = 0

                            # Iterar sobre los elementos de lista_s_principal excluyendo el último
                            for moneda in lista_operar[:-1]:
                                # Sumar el monto de cada moneda a la suma total
                                suma_montos += moneda.Monto

                            if moneda2.NombreMoneda == ultimo_dato.NombreMoneda:
                               valorAEchar = saldo_available- suma_montos -0.01
                            else:
                               valorAEchar = moneda2.Monto 
                                  
                            """ if listaActual == 1:
                               if moneda2.NombreMoneda == "Arbitrum/USDT":
                                   valorAEchar=saldo_available -30.00-500.00-500.00-0.01
                               else:
                                   valorAEchar=moneda2.Monto
                            elif listaActual == 2:
                                if moneda2.NombreMoneda == "Lido/USDT":
                                   valorAEchar = saldo_available -100.00-500.00-500.00-0.01
                                else:
                                   valorAEchar = moneda2.Monto
                            elif listaActual == 3:
                                if moneda2.NombreMoneda == "Cosmos/USDT":
                                   valorAEchar = saldo_available -500.00-0.01
                                else:
                                   valorAEchar = moneda2.Monto  """

                            # Convertir el valor a string y setearlo al campo de monto
                            valorAEchar_str = f"{valorAEchar:,.2f}"
                            amount_input.send_keys(valorAEchar_str)
                            #Confirmar operación
                            """   ask_yes_no() """
                            confirm_button = driver.find_element(By.CSS_SELECTOR, '.confirm__btn a')
                            confirm_button.click()
                            hora_actual = datetime.now()
                            hora_formateada = hora_actual.strftime("%I:%M %p")
                            print("Se ejecutó :"+moneda2.NombreMoneda+"a las :", hora_formateada)
                            # Encontrar la próxima fila vacía en la hoja
                            fila_vacia = hoja.max_row + 1
                            # Escribir datos en la hoja en la próxima fila vacía
                            hora_actual = datetime.now()
                            hora_formateada = hora_actual.strftime("%I:%M %p")
                            fecha_formateada = hora_actual.strftime("%d/%m/%Y")
                            hoja["A" + str(fila_vacia)] = moneda2.NombreMoneda
                            hoja["B" + str(fila_vacia)] = hora_formateada
                            hoja["C" + str(fila_vacia)] = fecha_formateada
                            hoja["D" + str(fila_vacia)] = roi_float
                            # Guardar los cambios en el libro de trabajo
                            libro.save("pruebaSoles.xlsx")
                            #Cambiar estado de la moneda a operada
                            moneda2.Estado = True
                            
                         else:
                            time.sleep(2) 

                    # Validar que todos los objetos en la lista tienen 'activo' como True
                    todos_activos = all(monedita.Estado for monedita in lista_operar)
                    if todos_activos:
                     polanco=False
                     # Actualizar el estado de la moneda principal en la lista principal
                     print("________________________")
                     for moneditas in lista_monedas_principal:
                        if moneda_principal.NombreMoneda == moneditas.NombreMoneda: 
                            moneditas.Estado==True
                            break
                     for moneditas2 in lista_operar:
                        moneditas2.Estado==False
                            
                    else:
                     polanco=True   

# Ciclo principal para la verificación y operación
continue_checking = True
while True:
    saldo_en_operacion = get_balance_operando(driver)
    if saldo_en_operacion == 0.0:
        moneda_operar=check_avalible_balance(continue_checking)
        print(f'Opción {moneda_operar.NombreMoneda} encontrada como principal')
        # Verificar el ROI según la moneda principal y lista correspondiente
        if  moneda_operar.NombreMoneda=="CAKE/USDT":
            check_roi_by_coin(lista_monedas_ronda1,moneda_operar,1)
        elif moneda_operar.NombreMoneda=="Lido/USDT":
            check_roi_by_coin(lista_monedas_ronda2,moneda_operar,2)
        elif moneda_operar.NombreMoneda=="Cosmos/USDT":
            check_roi_by_coin(lista_monedas_ronda3,moneda_operar,3)

# Reiniciar el estado de las monedas principales si es Cosmos/USDT
        if moneda_operar.NombreMoneda=="Cosmos/USDT":
            for moneditas in lista_monedas_principal:
                moneditas.Estado=False
    else: 
        hours = minutes = 0
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((By.ID, 'clock')))
        time.sleep(2)
        time_text = element.text
        parts = time_text.split()
        for part in parts:
            if 'h' in part:
                hours = int(part.replace('h', ''))
            elif 'm' in part:
                minutes = int(part.replace('m', ''))
        
        total_seconds = hours * 3600 + minutes * 60
        
        """ element= driver.find_element(By.CSS_SELECTOR, '.confirm__btn a')  """
        time.sleep(total_seconds)

    if keyboard.is_pressed("k"):
        print("Se ha presionado la tecla 'k'. Deteniendo el script...")
        break


# Cierra el navegador al finalizar
driver.quit()