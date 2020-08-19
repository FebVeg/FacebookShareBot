try:
    from tkinter import *
    from tkinter.ttk import *
    import tkinter as tk
    from tkinter.filedialog import askopenfilename
    from tkinter import messagebox
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

def istruzioni():
    i = """Benvenuto in ShareBOT, programma che automatizza il processo di condivisione dei post su Facebook per tutti i volontari
In questa mini-guida verrà scritto passo-passo il corretto funzionamento\n
1.  Inserisci nel campo 'Autenticazione' le tue credenziali di Facebook (Nessun dato verrà salvato o condiviso a terzi)
1a. Prima di effettuare qualsiasi operazione, effettua il Login\n
2.  Una volta inseriti i campi di Autenticazione, premi Login per loggarti su Facebook
2a. Potrai eseguire il Logout della tua utenza quando avrai finito di condividere il tuo appello usando Logout\n
3.  Nel campo 'Importa / Esporta lista gruppi' è possibile importare da 'Importa' una lista precedentemente esportata
3a. Se non hai una lista, effettua il Login ed infine usa il pulsante Esporta, verrà esportata ed importata automaticamente la lista dei tuoi gruppi di Facebook
3b  Puoi modificare i gruppi prima di inviare l'appello, usando il tasto 'Modifica' ed eliminando l'intera riga del gruppo a cui non vuoi condividere l'appello\n
4.  Nel campo 'Messaggio da condividere' dovrai scrivere il tuo appello\n
5.  Nel campo 'Azioni' ci saranno 4 pulsanti
5a. Il pulsante 'Condividi' serve per, una volta effettuato il login ed inseriti tutti i campi, avviare l'autocondivisione
5b. Il pulsante 'Istruzioni' farà apparire questa schermata di avviso
5c. Il pulsante 'Sviluppatore' aprirà il browser di default sulla pagina Github dello sviluppatore (Colui che ha programmato ShareBOT)
5d. Il pulsante 'Esci' è una funzione di chiusura logica del programma, effettua delle verifiche sul funzionamento del WebDriver per chiudere i processi figli di ShareBOT [Usare per chiudere il programma]"""
    istruzioni_window = tk.Tk()
    istruzioni_window.title('Istruzioni - Guida')
    istruzioni_window.resizable(False, False)
    Label(istruzioni_window, text=str(i)).grid(row=0, column=0, padx=5, pady=5)
    istruzioni_window.mainloop()

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
        print("[LOG] Controllo se il WebDriver è presente")

        if path.exists(dirFile + 'chromedriver.exe'):
            print("[LOG] WebDriver trovato, continuo")
        else:
            print("[LOG] WebDriver non trovato, recupero informazioni sulla versione di Chrome")
            
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
                        print("[LOG] Error: Errore nella lavorazione del file zippato: " + str(zip_err))
                        messagebox.showerror('Errore nella lavorazione del file zippato', str(zip_err))
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
                    print("[LOG] Versione di Chrome non scritta nel programma, aggiorna Google Chrome ad una di queste tre versioni: 83, 84, 85")
                    messagebox.showerror('Errore', 'Versione di Chrome non scritta nel programma, aggiornare Google Chrome ad una di queste tre versioni: 83, 84, 85')
                    exit()

                print("\n[LOG] Download completato, il WebDriver si trova qui: " + dirFile + "chromedriver.exe")
                print("[LOG] Avvio il programma")
            except Exception as e:
                print("[LOG] Errore durante il download del WebDriver: " + str(e))
                messagebox.showerror('Errore durante il download del WebDriver', str(e))
    else:
        print("[LOG] Google Chrome non è stato trovato")
        print("[LOG] Per far funzionare il programma, hai bisogno di installare Google Chrome")
        messagebox.showwarning('Google Chrome non è stato trovato', "Per far funzionare il programma, hai bisogno di installare Google Chrome")
        exit()

elif name == "posix":
    if path.exists("/snap/bin/chromium.chromedriver"):
        print("[LOG] Chromium WebDriver trovato, continuo")
        chromedriver = "/snap/bin/chromium.chromedriver"
        environ["WebDriver.chrome.driver"] = chromedriver
    else:
        print("[LOG] WebDriver non trovato, installa Chromium da terminale 'sudo apt install chromium* -y'")
        messagebox.showwarning("WebDriver non trovato", "installa Chromium da terminale 'sudo apt install chromium* -y'")
        exit()

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
            self.password = None # Assegno il valore None alla variabile della password
            driver.find_element_by_xpath('//*[@id="login_form"]/ul/li[3]/input').click()
            try:
                if driver.find_element_by_xpath('//*[@id="header"]/nav/a[1]'):
                    print("[LOG] Login effettuato")
                    messagebox.showinfo("Informazione", 'Login effettuato')
            except:
                messagebox.showerror('WARNING', "Non son riuscito ad effettuare il login o Facebook ha bisogno di verificare la tua identità")
                print("[LOG] Warning: Non son riuscito ad effettuare il login o Facebook ha bisogno di verificare la tua identità")
                pass
        except Exception as login_err:
            print("[LOG] Error: Errore nella funzione 'login': " + str(login_err))
            messagebox.showerror("Errore nella funzione 'login'", str(login_err))
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
                messagebox.showinfo('Informazione', 'Logout riuscito')
            else:
                print("[LOG] Warning: Logout non riuscito")
                messagebox.showwarning('Warning', 'Logout non riuscito')
        except Exception as logout_err:
            print("[LOG] Error: Errore nella funzione 'logout': " + str(logout_err))
            messagebox.showerror("Errore nella funzione 'logout'", str(logout_err))
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
                                for i in range(randint(20, 30), 0, -1):
                                    print("[ + ] Attesa di", i, "secondi ", end='\r')
                                    sleep(1)
                                print("[ + ] Condivisione del post in corso...", end="\r") 
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
                            except Exception as err:
                                print("[LOG] Warning: In questo gruppo '%s' non sembra possibile condividere il post: %s" % (title, err))
                                pass
                            except KeyboardInterrupt:
                                print("[LOG] Warning: Condivisione interrotta")
                                messagebox.showwarning('Warning', 'Condivisione interrotta')
                                return
                        else:
                            print("[LOG] Warning: Il WebDriver non è in esecuzione")
                            messagebox.showwarning('Warning', 'Il WebDriver non è in esecuzione')
                            pass                          
                    else:
                        print("[LOG] Warning: Processo del WebDriver figlio non in servizio")
                        messagebox.showwarning('Warning', 'Processo del WebDriver figlio non in servizio')
                        pass
                else:
                    print("[LOG] Warning: Processo del WebDriver non in servizio")
                    messagebox.showwarning('Warning', 'Processo del WebDriver non in servizio')
                    pass
            facebook_groups.clear()
            print("[LOG] Condivisione completata")
            messagebox.showinfo('Informazione', 'Condivisione completata')
        except Exception as cond_with_list_err:
            print("[LOG] Error: Errore nella funzione 'cond_with_list': " + str(cond_with_list_err))
            messagebox.showerror("Errore nella funzione 'cond_with_list'", str(cond_with_list_err))

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
                                    for i in range(randint(20, 30), 0, -1):
                                        print("[ + ] Attesa di", i, "secondi ", end='\r')
                                        sleep(1)   
                                    print("[ + ] Condivisione del post in corso...", end="\r")                                
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
                                except Exception as err:
                                    print("[LOG] Warning: In questo gruppo '%s' non sembra possibile condividere il post: %s" % (title, err))
                                    pass
                                except KeyboardInterrupt:
                                    print("[LOG] Warning: Condivisione interrotta")
                                    messagebox.showwarning('Warning', 'Condivisione interrotta')
                                    return
                            else:
                                print("[LOG] Warning: Il WebDriver non è in esecuzione")
                                messagebox.showwarning('Warning', 'Il WebDriver non è in esecuzione')
                                pass                          
                        else:
                            print("[LOG] Warning: Processo del WebDriver figlio non in servizio")
                            messagebox.showwarning('Warning', 'Processo del WebDriver figlio non in servizio')
                            pass
                    else:
                        print("[LOG] Warning: Processo del WebDriver non in servizio")
                        messagebox.showwarning('Warning', 'Processo del WebDriver non in servizio')
                        pass
                facebook_groups.clear()
                print("[LOG] Condivisione completata")
                messagebox.showinfo('Informazione', 'Condivisione completata')
            else:
                print("[WARNING] Gruppi non trovati")
                messagebox.showinfo('Warning', 'Gruppi non trovati')

        except Exception as cond_without_list_err:
            print("[LOG] Error: Errore nella funzione 'cond_without_list': " + cond_without_list_err)
            messagebox.showerror("Errore nella funzione 'cond_without_list'", cond_without_list_err)

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
                messagebox.showinfo('Informazione', "Gruppi salvati qui: " + dirFile + gp_list)
                lista.insert(0, dirFile + gp_list)
            else:
                print("[LOG] Warning: Gruppi non trovati")
                messagebox.showwarning('Warning', 'Gruppi non trovati')
        except Exception as get_groups_err:
            print("[LOG] Error: Errore nella funzione 'get_groups': " + get_groups_err)
            messagebox.showerror("Errore nella funzione 'get_groups'", get_groups_err)

def user_login():
    if len(email.get()) > 0:
        if len(password.get()) > 0:
            global utente
            utente = Webdriver(email.get(), password.get()) 
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

            global driver
            if name == "nt":
                driver = webdriver.Chrome(executable_path=dirFile + 'chromedriver.exe', options=chrome_options)
            elif name == "posix":
                driver = webdriver.Chrome(executable_path=chromedriver, options=chrome_options)

            driver.set_window_size(400,600)
            global url, session_id, driver_process
            url = driver.command_executor._url
            session_id = driver.session_id 
            driver_process = psutil.Process(driver.service.process.pid)
            print("[LOG] WebDriver process: " + str(driver_process))
            print("[LOG] WebDriver session id: " + session_id)
            print("[LOG] Il WebDriver è nella modalità 'incognito/privata' quindi non verrà salvato nessun dato sul browser")
            utente.login(driver, url, session_id)
        else:
            print("[LOG] Campo password vuoto")
            messagebox.showwarning("Warning", "Campo PASSWORD vuoto")
    else:
        print("[LOG] Campo email vuoto")
        messagebox.showwarning("Warning", "Campo EMAIL vuoto")
    pass

def user_logout():
    try:         
        if driver_process.is_running():
            print("[LOG] Controllo se il WebDriver è attivo per eseguire il logout")
            chrome_process = driver_process.children()
            if chrome_process:
                chrome_process = chrome_process[0]
                if chrome_process.is_running():
                    utente.logout(driver, url, session_id)
                else:
                    print("[LOG] Warning: Non posso eseguire il logout se il WebDriver non è attivo, esegui il LOGIN e riprova")
                    messagebox.showwarning('Warning', 'Non posso eseguire il logout se il WebDriver non è attivo, esegui il LOGIN e riprova')
            else:
                print("[LOG] Error: Il WebDriver è inattivo, esegui il LOGIN e riprova")
                messagebox.showwarning('Warning', 'Il WebDriver è inattivo, esegui il LOGIN e riprova')
        else:
            print("[LOG] Warning: WebDriver non attivo.")
    except Exception as user_logout_error:
        if str(user_logout_error) == "name 'driver_process' is not defined":
            print("[LOG] Error: Processo del WebDriver non valorizzato, effettua prima il Login")
            messagebox.showerror('Error', "Processo del WebDriver non valorizzato, effettua prima il Login")
        else:
            print("[LOG] Error: Problema nella funzione 'Logout': " + str(user_logout_error))
            messagebox.showerror("Problema nella funzione 'Logout'", str(user_logout_error))
    pass

def lista_import():
    try:
        ilist = askopenfilename(initialdir=dirFile, filetypes =(("File di test", "*.txt"),("All Files", "*.*")), title = "Importa la lista gruppi")
        lista.delete(0, END)
        lista.insert(0, ilist)
    except Exception as lista_import_err:
        print("[LOG] Error: Problemi nella funzione 'lista_import': " + str(lista_import_err))
        messagebox.showerror("Errore nella funzione 'lista_import'", str(lista_import_err))
    pass

def lista_export():
    try:
        utente.get_groups(driver, url, session_id)
    except Exception as lista_export_err:
        if str(lista_export_err) == "name 'utente' is not defined":
            print("[LOG] Error: Effettua prima il Login")
            messagebox.showwarning('Warning', 'Effettua prima il Login')
            pass
        else:
            print("[LOG] Error: Errore nella funzione 'lista_export': " + str(lista_export_err))
            messagebox.showerror("Errore nella funzione 'lista_export'", str(lista_export_err))
    pass

def user_share():
    try:
        if len(lista.get()) > 1:
            if path.exists(lista.get()):
                utente.cond_with_list(driver, url, session_id, lista.get(), post.get("1.0","end-1c"))
            else:
                print("[LOG] Errore: La lista sembra non essere accessibile o forse è danneggiata")
                messagebox.showerror('Errore', 'La lista sembra non essere accessibile o forse è danneggiata')
        else:
            utente.cond_without_list(driver, url, session_id, post.get("1.0","end-1c"))
    except Exception as user_share_err:
        if str(user_share_err) == "name 'utente' is not defined":
            print("[LOG] Error: Effettua prima il Login")
            messagebox.showwarning('Warning', 'Effettua prima il Login')
            pass
        else:
            print("[LOG] Error: Errore nella funzione 'user_share': " + str(user_share_err))
            messagebox.showerror("Errore nella funzione 'user_share'", str(user_share_err))
    pass

def lista_edit():
    if path.exists(dirFile + "ListaGruppi.txt"):
        if name == "nt":
            print("[LOG] Apertura della lista gruppi")
            startfile(dirFile + "ListaGruppi.txt")
        elif name == "posix":
            print("[LOG] Apertura della lista gruppi")
            system("xdg-open %s" % (dirFile + "/ListaGruppi.txt"))
    else:
        print("[LOG] Warning: Lista gruppi non trovata")
        messagebox.showwarning('Warning', 'Lista gruppi non trovata')

def sviluppatore():
    if name == "nt":
        print("[LOG] Apertura del profilo Github dello sviluppatore")
        startfile("https://github.com/FebVeg")
    elif name == "posix":
        print("[LOG] Apertura del profilo Github dello sviluppatore")
        system("xdg-open https://github.com/FebVeg")

def user_exit():
    global master
    try:         
        if driver_process.is_running():
            print("[LOG] Controllo se il WebDriver è attivo")
            chrome_process = driver_process.children()
            if chrome_process:
                chrome_process = chrome_process[0]
                if chrome_process.is_running():
                    print("[LOG] Il WebDriver è attivo, chiudo il programma.")
                    driver.quit()
                    master.destroy()
                    exit()
                else:
                    print("[LOG] Il WebDriver non è attivo, eseguo la kill del processo")
                    chrome_process.kill()
                    master.destroy()
                    exit()
            else:
                print("[LOG] Il WebDriver è inattivo.")
                master.destroy()
                exit()
    except:
        master.quit()

master = tk.Tk()
master.title("ShareBOT - V2.3.6 - FebVeg")
master.resizable(True, True)
master.grid_columnconfigure(1, weight=1)

# Frame di autenticazione
frame_auth = LabelFrame(master, text="Autenticazione")
frame_auth.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="WENS")
frame_auth.columnconfigure(1, weight=1)

# Campo Email
Label(frame_auth, text="Email").grid(row=0, column=0, sticky="W", padx=5)
email = Entry(frame_auth)
email.grid(row=0, column=1, pady=5, padx=5, sticky="WENS")
# Campo Password
Label(frame_auth, text="Password").grid(row=1, column=0, sticky="W", padx=5)
password = Entry(frame_auth, show="*")
password.grid(row=1, column=1, pady=5, padx=5, sticky="WENS")
# Pulsanti Login e Logout
Button(frame_auth, text='Login', command=user_login).grid(row=2, column=0, sticky="W", padx=5, pady=5)
Button(frame_auth, text='Logout',command=user_logout).grid(row=2, column=1, sticky="E", padx=5, pady=5)

# Frame della lista gruppi
frame_lista = LabelFrame(master, text="Importa / Esporta lista gruppi")
frame_lista.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="WENS")
frame_lista.columnconfigure(1, weight=1)

# Campi esporta importa lista gruppi
Label(frame_lista, text="Lista").grid(row=0, column=0, sticky="W", padx=5)
lista = Entry(frame_lista)
lista.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky="WENS")
Button(frame_lista, text='Importa', command=lista_import).grid(row=1, column=0, sticky="E", padx=5, pady=5)
Button(frame_lista, text='Esporta', command=lista_export).grid(row=1, column=1, sticky="E", padx=5, pady=5)
Button(frame_lista, text='Modifica', command=lista_edit).grid(row=1, column=2, sticky="E", padx=5, pady=5)

# Frame post
frame_post = LabelFrame(master, text="Messaggio da condividere")
frame_post.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="WENS")
frame_post.columnconfigure(0, weight=1)

# campo post
post = Text(frame_post, width=20, height=8)
post.grid(row=0, column=0, sticky="WENS", pady=5, padx=5)
scrollbar = Scrollbar(frame_post)
scrollbar.grid(row=0, column=0, sticky="ENS")
# attach textbox to scrollbar
post.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=post.yview)

# Frame pulsanti
frame_buttons = LabelFrame(master, text="Azioni")
frame_buttons.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="WENS")
Button(frame_buttons, text="Condividi", command=user_share).grid(row=0, column=0, padx=5, pady=5, sticky="E")
Button(frame_buttons, text="Istruzioni", command=istruzioni).grid(row=0, column=1, padx=5, pady=5, sticky="E")
Button(frame_buttons, text="Sviluppatore", command=sviluppatore).grid(row=0, column=2, padx=5, pady=5, sticky="E")
Button(frame_buttons, text="Esci", command=user_exit).grid(row=0, column=3, padx=5, pady=5, sticky="E")

master.mainloop()