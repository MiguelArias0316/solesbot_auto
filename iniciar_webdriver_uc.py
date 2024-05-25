# módulos de terceros
import undetected_chromedriver as uc

def iniciar_webdriver (headless=False, pos="maximizada"):
    options = uc.ChromeOptions()
    options.add_argument("--    -store=basic")
    options.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
        },
    )
    # intclanos el driver
    driver = uc.Chrome(
        options=options, 
        headless=headless, 
        log_level=3,
    )
    return driver 
    
    