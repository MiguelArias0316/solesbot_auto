
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from email.message import EmailMessage
from selenium import webdriver
from tkinter import messagebox
from datetime import datetime
from moneda import Moneda
import tkinter as tk
import keyboard
import openpyxl
import logging
import smtplib
import time
import ssl
from PIL import Image,ImageTk
import os

#Limpiar log
open('log.txt', 'w').close()

def mostrar_imagen():
    # Crear la ventana de tkinter y obtener dimensiones de la pantalla
    root = tk.Tk()
    root.title("AutoSoles By Arias & Edrass")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Cargar la imagen
    ruta_imagen = os.path.join(os.getcwd(), 'autoSolesIni.jpeg')
    imagen = Image.open(ruta_imagen)
    imagen = imagen.resize((800, 800))  # Ajusta el tamaño de la imagen según sea necesario

    # Mostrar la imagen en la ventana
    imagen_tk = ImageTk.PhotoImage(imagen)
    label = tk.Label(root, image=imagen_tk)
    label.pack(padx=10, pady=10)

    # Centrar la ventana en la mitad de la pantalla
    ventana_width = 800
    ventana_height = 800
    x_pos = (screen_width // 2) - (ventana_width // 2)
    y_pos = (screen_height // 2) - (ventana_height // 2)
    root.geometry(f'{ventana_width}x{ventana_height}+{x_pos}+{y_pos}')

    # Mostrar la ventana y esperar unos segundos antes de cerrarla
    root.after(5000, root.destroy)  # Cierra la ventana después de 5000 milisegundos (5 segundos)
    root.mainloop()

mostrar_imagen()

# Configurar el logger
logging.basicConfig(filename='log.txt', level=logging.ERROR,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Inicializa las variables
moneda_operar = None  # Variable global para almacenar la moneda a operar
usernametxt = None  # Variable para almacenar el nombre de usuario
passwordtxt = None  # Variable para almacenar la contraseña
chromedriverurl = None  # Variable para almacenar la URL del ChromeDriver
cuentaprocesada = None  # Variable para almacenar la cuenta procesada
lista_monedas_principal = []  # Lista principal de monedas
lista_monedas_ronda1 = []  # Lista de monedas para la ronda 1
lista_monedas_ronda2 = []  # Lista de monedas para la ronda 2
lista_monedas_ronda3 = []  # Lista de monedas para la ronda 3
correodestinatario = []  # Lista de destinatarios del correo
mensaje = None  # Variable para almacenar el mensaje del correo
remitente = "solesautogerencia@gmail.com"  # Dirección de correo del remitente
contraseña = "bzin hxxj aqoj dpit"  # Contraseña del correo del remitente
asunto = "Informacion Auto Soles"  # Asunto del correo


# Abre el archivo de parametros y configuración en modo de lectura
try:
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
            elif clave == "chromedriverurl":
                chromedriverurl = valor
            elif clave == "cuentaprocesada":
                cuentaprocesada = valor
            elif clave == "lista_monedas_principal":
                lista_monedas_principal = eval(valor)
            elif clave == "lista_monedas_ronda1":
                lista_monedas_ronda1 = eval(valor)
            elif clave == "lista_monedas_ronda2":
                lista_monedas_ronda2 = eval(valor)
            elif clave == "lista_monedas_ronda3":
                lista_monedas_ronda3 = eval(valor)
            elif clave == "correodestinatario":
                correodestinatario = eval(valor)
except Exception as e:
    logging.error("Error leyendo el archivo de configuración: %s", e)

# Convertir las listas cargadas en instancias de la clase Moneda
try:
    lista_monedas_principal = [Moneda(*moneda) for moneda in lista_monedas_principal]
    lista_monedas_ronda1 = [Moneda(*moneda) for moneda in lista_monedas_ronda1]
    lista_monedas_ronda2 = [Moneda(*moneda) for moneda in lista_monedas_ronda2]
    lista_monedas_ronda3 = [Moneda(*moneda) for moneda in lista_monedas_ronda3]
except Exception as e:
    logging.error("Error convirtiendo listas en instancias de Moneda: %s", e)

# Cargar el libro de trabajo existente
try:
    libro = openpyxl.load_workbook("balanceSolesBot.xlsx")
    hoja = libro.active
except Exception as e:
    logging.error("Error cargando el libro de trabajo: %s", e)

# Funcion para enviar correos
def enviar_correo_a_destinatarios(remitente, contraseña, destinatarios, asunto, mensaje):
    try:
        context = ssl.create_default_context()
        em = EmailMessage()
        em['From'] = remitente
        em['To'] = ", ".join(destinatarios)
        em['Subject'] = asunto
        em.set_content(mensaje)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(remitente, contraseña)
            smtp.sendmail(remitente, destinatarios, em.as_string())
    except Exception as e:
        logging.error("Error enviando correo: %s", e)

# Función para mostrar un cuadro de diálogo con opciones Sí/No.
def ask_yes_no():
    try:
        root = tk.Tk()
        root.withdraw()
        result = messagebox.askokcancel("Bienvenido a AutoSoles", "Si tienes captcha ejecutalo y luego dale click en aceptar, para terminar cancelar")
        if result:
            root.destroy()
        else:
            root.destroy()
            driver.quit()
    except Exception as e:
        logging.error("Error en ask_yes_no: %s", e)


# Inicializar WebDriver
try:
    driver_path = chromedriverurl
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=options)
except Exception as e:
    logging.error("Error inicializando WebDriver: %s", e)

# Navega a la página de inicio de sesión
try:
    driver.get('https://bot.solesbot.ai/login')
except Exception as e:
    logging.error("Error navegando a la página de inicio de sesión: %s", e)

""" ask_yes_no() """

# Localizar e interactuar con elementos
try:
    wait = WebDriverWait(driver, 300)
    username = wait.until(EC.presence_of_element_located((By.ID, 'Email')))
    password = driver.find_element(By.ID, 'Password')
    username.send_keys(usernametxt)
    password.send_keys(passwordtxt)

    wait = WebDriverWait(driver, 10)
    login_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'theme-btn')))
    driver.execute_script("arguments[0].scrollIntoView();", login_button)
    time.sleep(1)
    login_button.click()
except (NoSuchElementException, TimeoutException, ElementClickInterceptedException) as e:
    logging.error("Error interactuando con elementos: %s", e)

ask_yes_no()

# Navegar y obtener balances
try:
    driver.get('https://bot.solesbot.ai/arbitrage/manual')
    eye_icon = driver.find_element(By.CSS_SELECTOR, 'i.fa.fa-eye.cursor-pointer[ng-click="showBalance()"]')
    eye_icon.click()
    time.sleep(2)
except (NoSuchElementException, WebDriverException) as e:
    logging.error("Error navegando y obteniendo balances: %s", e)


# Verificar saldo Available
def get_available_balance(driver):
    try:
        available_element = driver.find_element(By.XPATH, '//div[contains(@class, "pnl__single__box")][p[contains(text(), "Available")]]/h4[contains(@class, "notranslate ng-binding")]')
        currency = available_element.find_element(By.XPATH, './/span[contains(@class, "notranslate")]').text
        balance_text = available_element.get_attribute('innerText').replace(currency, '').strip()
        available_number = float(balance_text.replace(',', ''))
        return available_number
    except Exception as e:
        logging.error("Error getting available balance: %s", e)
        return 0.0

# Verificar saldo en operación
def get_balance_operando(driver):
    try:
        driver.get('https://bot.solesbot.ai/arbitrage/manual')
        time.sleep(2)
        eye_icon = driver.find_element(By.CSS_SELECTOR, 'i.fa.fa-eye.cursor-pointer[ng-click="showBalance()"]')
        eye_icon.click()
        time.sleep(10)

        operation_element = driver.find_element(By.XPATH, '//div[contains(@class, "pnl__single__box")][p[contains(text(), "Balance in Operation")]]/h4[contains(@class, "ng-binding")]')
        currency = operation_element.find_element(By.XPATH, './/span[contains(@class, "notranslate")]').text
        balance_text = operation_element.get_attribute('innerText').replace(currency, '').strip()
        operation_number = float(balance_text.replace(',', ''))
        return operation_number
    except Exception as e:
        logging.error("Error getting balance in operation: %s", e)
        return 1.0


# Obtiene el saldo disponible
saldo_available = get_available_balance(driver)

# Función para verificar el saldo disponible y determinar la moneda a operar.
def check_avalible_balance(continue_checking):
    while continue_checking:
        try:
            saldo_available = get_available_balance(driver)
            for moneda in lista_monedas_principal:
                if moneda.Estado == False:
                    continue_checking = False
                    return moneda
        except Exception as e:
            logging.error("Error in check_avalible_balance: %s", e)
        break


# Función para verificar el ROI de cada moneda y ejecutar operaciones.
def check_roi_by_coin(lista_operar, moneda_principal, listaActual):
    polanco = True  # Bucle de control para la operación
    hora_actual = datetime.now()
    hora_formateada = hora_actual.strftime("%I:%M %p")
    hora_final = None
    print("_____________La ronda de " + moneda_principal.NombreMoneda + " comenzó a las", hora_formateada)
    
    while polanco:
        # Recorre cada moneda en la lista para operar
        for moneda2 in lista_operar:
            try:
                opcion_encontrada = None
                # Si la moneda no ha sido operada aún
                if moneda2.Estado != True:
                    wait = WebDriverWait(driver, 10)
                    select_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select[ng-model="coin"]')))
                    dropdown = Select(select_element)
                    
                    # Buscar opción en el dropdown
                    for option in dropdown.options:
                        if moneda2.NombreMoneda != "CAKE/USDT":
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
                        continue
                    
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
                        continue

                    time.sleep(1)

                    # Obtener el ROI de la moneda
                    roi_moneda = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[ng-model="suggestion.profit"]')))
                    roi_moneda_texto = roi_moneda.get_attribute('value')
                    roi_float = float(roi_moneda_texto)

                    # Comparar el ROI obtenido con el ROI deseado
                    if roi_float >= moneda2.ROI:
                        # Click en el botón Execute
                        execute_button = driver.find_element(By.CSS_SELECTOR, '.withdraw__con__btn button')
                        execute_button.click()

                        # Ingresar el monto
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
                            valorAEchar = saldo_available - suma_montos - 0.01
                        else:
                            valorAEchar = moneda2.Monto

                        if valorAEchar > moneda2.Monto:
                            valorAEchar = moneda2.Monto

                        # Convertir el valor a string y setearlo al campo de monto
                        valorAEchar_str = f"{valorAEchar:,.2f}"
                        amount_input.send_keys(valorAEchar_str)

                        # Confirmar operación
                        confirm_button = driver.find_element(By.CSS_SELECTOR, '.confirm__btn a')
                        confirm_button.click()

                        hora_actual = datetime.now()
                        hora_formateada = hora_actual.strftime("%I:%M %p")
                        print("Se ejecutó :" + moneda2.NombreMoneda + " a las :", hora_formateada)

                        # Encontrar la próxima fila vacía en la hoja
                        fila_vacia = hoja.max_row + 1

                        # Escribir datos en la hoja en la próxima fila vacía
                        fecha_formateada = hora_actual.strftime("%d/%m/%Y")
                        hoja["A" + str(fila_vacia)] = moneda2.NombreMoneda
                        hoja["B" + str(fila_vacia)] = hora_formateada
                        hoja["C" + str(fila_vacia)] = fecha_formateada
                        hoja["D" + str(fila_vacia)] = roi_float
                        hoja["E" + str(fila_vacia)] = cuentaprocesada
                        hora_final = hora_formateada + " del " + fecha_formateada

                        # Guardar los cambios en el libro de trabajo
                        libro.save("balanceSolesBot.xlsx")

                        # Cambiar estado de la moneda a operada
                        moneda2.Estado = True
                    else:
                        time.sleep(2)
            except (NoSuchElementException, TimeoutException, ElementClickInterceptedException, ValueError) as e:
                logging.error("Error en check_roi_by_coin con la moneda %s: %s", moneda2.NombreMoneda, e)
                continue

        # Validar que todos los objetos en la lista tienen 'activo' como True
        todos_activos = all(monedita.Estado for monedita in lista_operar)
        if todos_activos:
            polanco = False
            # Actualizar el estado de la moneda principal en la lista principal
            print("________________________")
            mensaje = "La ronda número " + str(listaActual) + " de " + moneda_principal.NombreMoneda + " finalizó a las " + hora_final + " y comenzó a las " + hora_formateada
            enviar_correo_a_destinatarios(remitente, contraseña, correodestinatario, asunto, mensaje)
            for moneditas in lista_monedas_principal:
                if moneda_principal.NombreMoneda == moneditas.NombreMoneda:
                    moneditas.Estado = True
                    break
            for moneditas2 in lista_operar:
                moneditas2.Estado = False
        else:
            polanco = True 
                     
"""ask_yes_no() """

# Ciclo principal para la verificación y operación
continue_checking = True
while True:
    try:
        saldo_en_operacion = get_balance_operando(driver)
        
        if saldo_en_operacion == 0.0:
            moneda_operar = check_avalible_balance(continue_checking)
            print(f'Opción {moneda_operar.NombreMoneda} encontrada como principal')
            
            # Verificar el ROI según la moneda principal y lista correspondiente
            if moneda_operar.NombreMoneda == "CAKE/USDT":
                check_roi_by_coin(lista_monedas_ronda1, moneda_operar, 1)
            elif moneda_operar.NombreMoneda == "Lido/USDT":
                check_roi_by_coin(lista_monedas_ronda2, moneda_operar, 2)
            elif moneda_operar.NombreMoneda == "Cosmos/USDT":
                check_roi_by_coin(lista_monedas_ronda3, moneda_operar, 3)

            # Reiniciar el estado de las monedas principales si es Cosmos/USDT
            if moneda_operar.NombreMoneda == "Cosmos/USDT":
                for moneditas in lista_monedas_principal:
                    moneditas.Estado = False
        else:
            hours = minutes = 0
            try:
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
                # Enviar correos
                mensaje = f"Total {hours}h {minutes}m para ejecutar siguiente ronda"
                enviar_correo_a_destinatarios(remitente, contraseña, correodestinatario, asunto, mensaje)
                time.sleep(total_seconds)
            except (NoSuchElementException, TimeoutException, ValueError) as e:
                logging.error("Error en la verificación del tiempo: %s", e)

        if keyboard.is_pressed("k"):
            print("Se ha presionado la tecla 'k'. Deteniendo el script...")
            break

    except (NoSuchElementException, TimeoutException, ElementClickInterceptedException, ValueError) as e:
        logging.error("Error en el ciclo principal: %s", e)
    except Exception as e:
        logging.critical("Error inesperado: %s", e)


# Cierra el navegador al finalizar
try:
    driver.quit()
except Exception as e:
    logging.error("Error al cerrar el navegador: %s", e)