from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

driver_path = Path(__file__).parent / "driver" / "chromedriver.exe"

service = Service(str(driver_path))
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 15)


TOKEN = os.getenv("DISCORD_TOKEN")
driver.get("https://discord.com/login")

time.sleep(5)

def verifyBio(user_id, search_string):

    string_procurada = search_string

    script = f"""
    function login(token) {{
        setInterval(() => {{
            document.body.appendChild(document.createElement('iframe')).contentWindow.localStorage.token = `"${{token}}"`;
        }}, 50);
        setTimeout(() => {{
            location.reload();
        }}, 2500);
    }}
    login("{TOKEN}");
    """
    driver.execute_script(script)
    wait.until(lambda d: "https://discord.com/channels/@me" in d.current_url)
    print("✅ Logado!")

    driver.get(f"https://discord.com/users/{user_id}")
    xpath_bio = "/html/body/div[1]/div[2]/div/div[6]/div[2]/div/div/div/div/div[2]/div/main/div[2]/section[1]/div/div/span"

    try:
        bio_span = wait.until(lambda d: d.find_element(By.XPATH, xpath_bio))
        bio_texto = bio_span.text.strip()
        
        print(f"Bio: {bio_texto}")
        
        if string_procurada in bio_texto:
            print("[+] Encontrou! Usuário ganha o cargo.")
            return True
        else:
            print("[-] Não encontrou! Usuário não ganha o cargo.")
            return False
            
    except Exception as e:
        print(f" Erro ao pegar bio: {e}")

    time.sleep(30)

    driver.quit()