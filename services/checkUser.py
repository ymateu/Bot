from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time


def checkUserBio(token: str, user_id: str, search_string: str = "Java", driver_path: str = "./chromedriver.exe", timeout: int = 15) -> bool:
    service = Service(driver_path)
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")

    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, timeout)

    try:
        driver.get("https://discord.com/login")
        time.sleep(5)

        script = f"""
            function login(token) {{
                setInterval(() => {{
                    document.body.appendChild(document.createElement('iframe')).contentWindow.localStorage.token = `"${{token}}"`;
                }}, 50);
                setTimeout(() => {{
                    location.reload();
                }}, 2500);
            }}
            login("{token}");
        """

        driver.execute_script(script)
        wait.until(lambda d: "https://discord.com/channels/@me" in d.current_url)

        driver.get(f"https://discord.com/users/{user_id}")
        xpath_bio = "/html/body/div[1]/div[2]/div/div[6]/div[2]/div/div/div/div/div[2]/div/main/div[2]/section[1]/div/div/span"

        bio_span = wait.until(lambda d: d.find_element(By.XPATH, xpath_bio))
        bio_texto = bio_span.text.strip()

        if search_string in bio_texto:
            return True
        raise ValueError(f"Texto '{search_string}' não encontrado na bio do usuário {user_id}.")

    except Exception as error:
        raise

    finally:
        driver.quit()
