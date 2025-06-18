import urequests as requests
import uos
import machine

class OTAUpdater:
    def __init__(self, repo_url):
        self.repo_url = repo_url.rstrip('/')
        self.raw_base_url = self.repo_url.replace('github.com', 'raw.githubusercontent.com') + '/main'

    def download_file(self, path):
        url = f"{self.raw_base_url}/{path}"
        print("Descarregant:", url)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                with open(path, 'w') as f:
                    f.write(r.text)
                print(f"[OK] Fitxer {path} descarregat.")
            else:
                print(f"[ERROR] No s'ha trobat el fitxer: {path}")
            r.close()
        except Exception as e:
            print(f"[ERROR] No s'ha pogut descarregar {path}: {e}")

    def delete_file(self, path):
        try:
            uos.remove(path)
            print(f"[INFO] Fitxer {path} eliminat.")
        except:
            pass

    def download_and_install_update_if_available(self, main_filename='main.py'):
        print("[OTA] Comprovant actualitzacions...")

        # Fitxers a actualitzar - pots ampliar aquesta llista
        files_to_update = ['main.py', 'boot.py']

        for file in files_to_update:
            self.download_file(file)

        print("[OTA] Actualització completada. Reiniciant...")
        machine.reset()
