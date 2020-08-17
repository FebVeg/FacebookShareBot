try:
    import PySimpleGUI as sg
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options
    from os import path, name
    if name == "posix":
        from os import system, environ
    elif name == "nt":
        from os import startfile
    from random import randint, choice
    from time import sleep
    import psutil
    import re
except Exception as e:
    print("[FATAL] Libreria mancante: " + str(e))

if name == "nt":
    dirFile = path.dirname(path.abspath(__file__)) + "\\" # Default dir
elif name == "posix":
    dirFile = path.dirname(path.abspath(__file__)) + "/" # Default dir

facebook_groups = []

# Auto configurazione iniziale
print("[LOG] Autoconfigurazione in corso")
print("[LOG] Non chiudere questa finestra")
print("[LOG] Controllo se Chrome o Chromium sono installati")

if name == "nt":
    if path.exists(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"):
        print("[LOG] Chrome trovato")
        print("[LOG] Controllo se il WebDriver esiste già")

        if path.exists(dirFile + 'chromedriver.exe'):
            print("[LOG] WebDriver trovato, continuo")
        else:
            print("[WARNING] WebDriver non trovato, recupero informazioni sulla versione di Chrome")
            
            def get_version_via_com(filename): # Thanks to temascal
                from win32com.client import Dispatch
                parser = Dispatch("Scripting.FileSystemObject")
                try:
                    version = parser.GetFileVersion(filename)
                except Exception:
                    return None
                return version

            paths = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"]
            version = list(filter(None, [get_version_via_com(p) for p in paths]))[0]
            print("[LOG] Versione di Chrome: " + version)
            version = version[0:2]

            print("[LOG] Download del WebDriver in corso")
            try:
                import wget
                chrome83 = "https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_win32.zip"
                chrome84 = "https://chromedriver.storage.googleapis.com/84.0.4147.30/chromedriver_win32.zip"
                chrome85 = "https://chromedriver.storage.googleapis.com/85.0.4183.38/chromedriver_win32.zip"

                def unzip(arg):
                    print("\n[LOG] Estraggo il WebDriver dallo zip")
                    try:
                        import zipfile
                        with zipfile.ZipFile(arg, 'r') as zip_ref:
                            zip_ref.extractall(dirFile)
                        print("[LOG] File estratto, imposto il WebDriver nel programma")
                    except Exception as zip_err:
                        print("[ERROR] Errore nella lavorazione del file zippato: " + str(zip_err))
                        input("[LOG] Premi INVIO per continuare")
                        exit()                

                if version == "83":
                    wget.download(chrome83, dirFile + 'chromedriver_win32.zip')
                    unzip(dirFile + 'chromedriver_win32.zip')

                elif version == "84":
                    wget.download(chrome84, dirFile + 'chromedriver_win32.zip')
                    unzip(dirFile + 'chromedriver_win32.zip')
                
                elif version == "85":
                    wget.download(chrome85, dirFile + 'chromedriver_win32.zip')
                    unzip(dirFile + 'chromedriver_win32.zip')
                
                else:
                    print("[ERROR] Versione di Chrome non scritta nel programma, aggiorna Google Chrome ad una di queste tre versioni: 83, 84, 85")
                    input("[QUESTION] Premi INVIO per continuare")
                    exit()

                print("\n[LOG] Download completato, il WebDriver si trova qui: " + dirFile + "chromedriver.exe")
                print("[LOG] Avvio il programma")
            except Exception as e:
                print("[ERROR] Errore durante il download del WebDriver: " + str(e))
    else:
        print("[WARNING] Google Chrome non è stato trovato.")
        print("[LOG] Per far funzionare il programma, hai bisogno di installare Google Chrome")
        input("[LOG] Premi INVIO per continuare")
        exit()

elif name == "posix":
    if path.exists("/snap/bin/chromium.chromedriver"):
        print("[LOG] Chromium WebDriver trovato, continuo")
        chromedriver = "/snap/bin/chromium.chromedriver"
        environ["WebDriver.chrome.driver"] = chromedriver
    else:
        print("[WARNING] WebDriver non trovato, installa Chromium da terminale 'sudo apt install chromium* -y'")
        exit()

print("[LOG] Fine dell'autoconfigurazione, avvio il programma...")

class Webdriver:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self, driver, url, session_id):
        try:
            print("[LOG] Eseguo il login")
            driver = webdriver.Remote(command_executor=url, desired_capabilities={})
            driver.close()
            driver.session_id = session_id
            driver.get("https://mbasic.facebook.com/")
            element = driver.find_element_by_name("email")
            element.send_keys(self.username)
            print("[LOG] Email inserita")
            element = driver.find_element_by_name("pass")
            element.send_keys(self.password)
            print("[LOG] Password inserita")
            driver.find_element_by_xpath('//*[@id="login_form"]/ul/li[3]/input').click()
            print("[LOG] Accedo come %s" % (self.username))
            try:
                if driver.find_element_by_xpath('//*[@id="header"]/nav/a[1]'):
                    print("[LOG] Login effettuato")
            except:
                sg.popup_error('WARNING', 'Non son riuscito ad effettuare il login, probabilmente le credenziali non sono esatte')
                print("[WARNING] Login fallito")
                print("[LOG] Chiudo il WebDriver")
                driver.quit()
                pass
        except Exception as login_err:
            print("[ERROR] Errore nella funzione 'login': " + str(login_err))
            pass
    
    def logout(self, driver, url, session_id):
        try:
            print("[LOG] Eseguo il logout")
            driver = webdriver.Remote(command_executor=url, desired_capabilities={})
            driver.close()
            driver.session_id = session_id
            driver.get("https://mbasic.facebook.com/")
            sleep(5)
            driver.find_element_by_xpath('//*[@id="header"]/nav/a[10]').click()
            print("[LOG] Logout passaggio 1/5")
            sleep(5)
            driver.find_element_by_xpath('//*[@id="mbasic_logout_button"]').click()
            print("[LOG] Logout passaggio 2/5")
            sleep(5)
            driver.find_element_by_xpath('//*[@id="root"]/table/tbody/tr/td/div/form[2]/input[3]').click()
            print("[LOG] Logout passaggio 3/5")
            sleep(5)
            driver.find_element_by_xpath('//*[@id="root"]/table/tbody/tr/td/div/div[2]/div[1]/table/tbody/tr/td[3]/a/div/img').click()
            print("[LOG] Logout passaggio 4/5")
            sleep(5)
            driver.find_element_by_xpath('//*[@id="root"]/table/tbody/tr/td/div[3]/div/form[1]/table/tbody/tr/td/header/h3[1]/input').click()
            print("[LOG] Logout passaggio 5/5")
            sleep(5)
            # check
            if driver.find_element_by_xpath('//*[@id="login_form"]/ul/li[3]/input'):
                print("[LOG] Logout eseguito")
            else:
                print("[ERROR] Errore durante la verifica di logout")
        except Exception as logout_err:
            print("[ERROR] Errore nella funzione 'logout': " + str(logout_err))
            pass
    
    def cond_with_list(self, driver, url, session_id, lista, post):
        try:
            driver = webdriver.Remote(command_executor=url, desired_capabilities={})
            driver.close()
            driver.session_id = session_id
            print("[LOG] Condivisione su tutti i gruppi nella lista in corso")
            print("[LOG] Preparazione della lista")
            group_lines = open(lista, encoding="utf-8").readlines()
            for line in group_lines:
                line = line.strip()
                line = re.sub(r' \s.*$', '', line)
                line = line.split(" ", 1)[0]
                facebook_groups.append(line)
            print("[LOG] Lista preparata")
            print("[LOG] Procedo con la condivisione")
            print("[ + ] Per interrompere il processo: Premi CTRL+C in questa schermata")
            for idx, val in enumerate(facebook_groups, 1):
                if driver_process.is_running():
                    chrome_process = driver_process.children()
                    if chrome_process:
                        chrome_process = chrome_process[0]
                        if chrome_process.is_running():
                            try:
                                tempo = randint(20, 40)
                                print("[ + ] Attendo %s secondi..." % (tempo))
                                sleep(tempo)
                                driver.get(val)
                                title = driver.title
                                sleep(randint(2, 6))
                                cond = driver.find_element_by_name("xc_message")
                                cond.click()
                                sleep(randint(2, 6))
                                cond.send_keys(post)
                                sleep(randint(2, 6))
                                cond = driver.find_element_by_name("view_post")
                                sleep(randint(2, 6))
                                cond.click()
                                print("[LOG] %d/%s Post condiviso a: %s" % (idx, len(facebook_groups), title))
                            except:
                                print("[WARNING] In questo gruppo '%s' non sembra possibile condividere il post" % (title))
                                pass
                    else:
                        print("[WARNING] Condivisione interrotta")
                        break
            facebook_groups.clear()
            print("[LOG] Condivisione completata")
            sg.popup('Informazione', 'Condivisione completata')
        except Exception as cond_with_list_err:
            print("[ERROR] Errore nella funzione 'cond_with_list': " + str(cond_with_list_err))
            sg.popup_error('Errore', "Errore nella funzione 'cond_with_list': " + str(cond_with_list_err))

    def cond_without_list(self, driver, url, session_id, post):
        try:
            driver = webdriver.Remote(command_executor=url, desired_capabilities={})
            driver.close()
            driver.session_id = session_id
            print("[LOG] Condivisione su tutti i gruppi di cui fai parte")
            print("[LOG] Cerco i gruppi")
            driver.get("https://mbasic.facebook.com/groups/?seemore&refid=27")
            elems = driver.find_elements_by_tag_name("a")
            if elems:
                for elem in elems:
                    elem_clean = elem.get_attribute("href") # Raccolto in variabile solo gli href dell'html
                    if elem_clean.endswith("?refid=27"): # estraggo solo le stringhe che finiscono per ?refid=27
                        facebook_groups.append(elem_clean) # appeno il gruppo all'array
                print("[LOG] Gruppi importati nell'array")
                print("[LOG] Procedo con la condivisione")
                print("[ + ] Per interrompere il processo: Premi CTRL+C in questa schermata")

                for idx, val in enumerate(facebook_groups, 1):
                    if driver_process.is_running():
                        chrome_process = driver_process.children()
                        if chrome_process:
                            chrome_process = chrome_process[0]
                            if chrome_process.is_running():
                                try:
                                    tempo = randint(20, 40)
                                    print("[ + ] Attendo %s secondi..." % (tempo))
                                    sleep(tempo)                                    
                                    driver.get(val)
                                    title = driver.title
                                    sleep(randint(2, 6))
                                    cond = driver.find_element_by_name("xc_message")
                                    cond.click()
                                    sleep(randint(2, 6))
                                    cond.send_keys(post)
                                    sleep(randint(2, 6))
                                    driver.find_element_by_name("view_post").click()
                                    sleep(randint(2, 6))
                                    print("[+] %d/%s Post inviato a: %s" % (idx, len(facebook_groups), title))
                                except:
                                    print("[WARNING] In questo gruppo '%s' non sembra possibile condividere il post" % (title))
                                    pass
                        else:
                            print("[WARNING] Condivisione interrotta")
                            break
                facebook_groups.clear()
                print("[LOG] Condivisione completata")
                sg.popup('Informazione', 'Condivisione completata')
            else:
                print("[WARNING] Gruppi non trovati")
                sg.popup('Errore', 'Gruppi non trovati')

        except Exception as cond_without_list_err:
            print("[ERROR] Errore nella funzione 'cond_without_list': " + cond_without_list_err)
            sg.popup_error("Errore nella funzione 'cond_without_list': " + cond_without_list_err)

    def get_groups(self, driver, url, session_id):
        try:
            driver = webdriver.Remote(command_executor=url,desired_capabilities={})
            driver.close()
            driver.session_id = session_id
            print("[LOG] Estrazione dei gruppi in corso...")
            driver.get("https://mbasic.facebook.com/groups/?seemore&refid=27")
            gp_list = "ListaGruppi.txt"
            print("[LOG] Cerco i gruppi...")
            elems = driver.find_elements_by_tag_name("a")
            if elems:
                for elem in elems:
                    elem_clean = elem.get_attribute("href") # Raccolto in variabile solo gli href dell'html
                    if elem_clean.endswith("?refid=27"): # estraggo solo le stringhe che finiscono per ?refid=27
                        name_clean = elem.get_attribute('text')
                        blob = elem_clean + " : " + name_clean
                        facebook_groups.append(blob) # appeno il gruppo all'array
                print("[LOG] Salvataggio dei gruppi in corso...")
                dump = open(dirFile+gp_list, "w", encoding='utf-8')
                for x in facebook_groups:
                    dump.write(x + "\n")
                dump.close()
                print("[LOG] Gruppi salvati qui: " + dirFile + gp_list)
                facebook_groups.clear()
                sg.popup('Gruppi esportati')
                window.find_element('lista').Update(dirFile + gp_list)
            else:
                print("[WARNING] Gruppi non trovati")
                sg.popup('Errore', 'Gruppi non trovati')
        except Exception as get_groups_err:
            print("[ERROR] Errore nella funzione 'get_groups': " + get_groups_err)
            sg.popup("Errore nella funzione 'get_groups': " + get_groups_err)

# Parte grafica del programma
sg.change_look_and_feel('Dark Blue 3')
layout = [        
    [sg.Frame('Login / Logout',[
        [sg.Text('1. Inserisci le tue credenziali di Facebook e usa LOGIN per autenticarti')],
        [sg.Text("Email", size=(13, 1)), sg.InputText(key='username')],
        [sg.Text("Password", size=(13, 1)), sg.InputText(key='password', password_char='*')],
        [sg.Button('LOGIN', key='Login', size=(9, 1)), sg.Button('LOGOUT', key='Logout', size=(9, 1))]
    ])],

    [sg.Frame('Esporta / Modifica lista gruppi',[
        [sg.Text('2. Usa ESPORTA per generare una lista dei tuoi gruppi')],
        [sg.Text('3. Usa MODIFICA per modificare la lista gruppi')],

        [sg.Text('Lista:', size=(None, 1)), sg.Input(key='lista'), sg.FileBrowse(button_text="Apri", size=(None, 1))],
        [sg.Button('ESPORTA', size=(None, 1), key='esporta'), sg.Button('MODIFICA', size=(None, 1), key='modifica')]
    ])],

    [sg.Frame('Messaggio / Post',[
        [sg.Text('4. Inserisci in questo campo il messaggio che vuoi condividere')],
        [sg.Multiline(size=(60, 10), key='post')]
    ]),
],  
    [sg.Text('5. Dopo aver compilato tutti i campi usa CONDIVIDI per avviare il BOT')],
    [sg.Button('CONDIVIDI', key='Condividi', size=(None, 1)), sg.Button('ISTRUZIONI', key='Informazioni', size=(None, 1)), sg.Button("SVILUPPATORE", size=(None, 1), key='dev'), sg.Button('ESCI', key='Esci', size=(5, 1))]
]

window = sg.Window('ShareBOT - v2.3.4 - FebVeg', layout)
while True:
    try:
        event, values = window.read()

        username = values['username']
        password = values['password']
        lista = values['lista']
        post = values['post']

        utente = Webdriver(username, password)

        if event == "Informazioni":
            if name == "nt":
                print("[LOG] Apertura file di istruzioni")
                startfile(dirFile + "tutorial.txt")
            elif name == "posix":
                print("[LOG] Apertura file di istruzioni")
                system("xdg-open %s" % (dirFile + "tutorial.txt"))

        elif event == 'Login':
            if len(username) > 0:
                if len(password) > 0:
                    ua = [
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
                        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)',
                        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
                        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
                        ]
                    random_ua = "".join(choice(ua))
                    chrome_options = Options()
                    chrome_options.add_argument("--incognito")
                    chrome_options.add_argument('--user-agent="%s"' % (random_ua))
                    print("[LOG] UserAgent: %s" % (random_ua))

                    if name == "nt":
                        driver = webdriver.Chrome(executable_path=dirFile + 'chromedriver.exe', options=chrome_options)
                    elif name == "posix":
                        driver = webdriver.Chrome(executable_path=chromedriver, options=chrome_options)

                    driver.set_window_size(400,600)
                    url = driver.command_executor._url
                    session_id = driver.session_id
                    driver_process = psutil.Process(driver.service.process.pid)
                    print("[LOG] WebDriver process: " + str(driver_process))
                    print("[LOG] WebDriver session id: " + session_id)
                    print("[LOG] Il WebDriver è nella modalità 'incognito/privata' quindi non verrà salvato nessun dato sul browser")
                    utente.login(driver, url, session_id)
                else:
                    print("[ERROR] Valore Password vuoto")
            else:
                print("[ERROR] Valore Email vuoto")

        elif event == 'Logout':
            try:         
                if driver_process.is_running():
                    print("[LOG] Controllo se il WebDriver è attivo per eseguire il logout")
                    chrome_process = driver_process.children()
                    if chrome_process:
                        chrome_process = chrome_process[0]
                        if chrome_process.is_running():
                            utente.logout(driver, url, session_id)
                        else:
                            print("[WARNING] Non posso eseguire il logout se il WebDriver non è attivo, esegui il LOGIN e riprova")
                    else:
                        print("[ERROR] Il WebDriver è inattivo, esegui il LOGIN e riprova")
                else:
                    print("[WARNING] WebDriver non attivo.")
            except:
                print("[ERROR] Errore nel controllo della funzione 'Logout'.")
                pass

        elif event == "Condividi":
            if len(lista) > 0:
                if path.exists(lista):
                    utente.cond_with_list(driver, url, session_id, lista, post)
                else:
                    print("[LOG] Errore: La lista sembra non essere accessibile o forse è danneggiata")
            else:
                utente.cond_without_list(driver, url, session_id, post)

        elif event == "esporta":
            utente.get_groups(driver, url, session_id)
      
        elif event == 'modifica':
            if path.exists(dirFile + "ListaGruppi.txt"):
                if name == "nt":
                    print("[LOG] Apertura della lista gruppi")
                    startfile(dirFile + "ListaGruppi.txt")
                elif name == "posix":
                    print("[LOG] Apertura della lista gruppi")
                    system("xdg-open %s" % (dirFile + "/ListaGruppi.txt"))
            else:
                print("[ERROR] File non trovato")
                sg.popup_error('File non trovato')
        
        elif event == 'dev':
            if name == "nt":
                print("[LOG] Apertura del profilo Github dello sviluppatore")
                startfile("https://github.com/FebVeg")
            elif name == "posix":
                print("[LOG] Apertura del profilo Github dello sviluppatore")
                system("xdg-open https://github.com/FebVeg")

        elif event == sg.WINDOW_CLOSED or event == 'Esci':
            try:         
                if driver_process.is_running():
                    print("[LOG] Controllo se il WebDriver è attivo")
                    chrome_process = driver_process.children()
                    if chrome_process:
                        chrome_process = chrome_process[0]
                        if chrome_process.is_running():
                            print("[LOG] Il WebDriver è attivo, chiudo il programma.")
                            driver.quit()
                            break
                        else:
                            print("[ERROR] Il WebDriver non è attivo, eseguo la kill del processo")
                            chrome_process.kill()
                            break
                    else:
                        print("[ERROR] Il WebDriver è inattivo.")
                        break
            except:
                break

    except Exception as error_code:
        print("[FATAL] Environment error: " + str(error_code))
        input("[ + ] Premere INVIO per continuare")
        exit()
        
window.close()