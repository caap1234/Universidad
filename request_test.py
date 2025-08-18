import requests

def check_website(url):
    print(f"\n[+] Verificando sitio web: {url}")
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            print(f"[OK] El sitio {url} está en línea y responde correctamente.")
        else:
            print(f"[!] El sitio respondió con código {resp.status_code}.")
    except requests.exceptions.RequestException as e:
        print(f"[X] Error al conectar con {url}: {e}")

# Llamadas de prueba
check_website("https://www.google.com")
check_website("https://www.python.org")
