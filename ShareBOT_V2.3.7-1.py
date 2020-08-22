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
1.  Inserisci nel campo 'Autenticazione' le tue credenziali di Facebook e poi premi Login (Nessun dato verrà salvato o condiviso a terzi)
1a. Si aprirà il browser, lascia eseguire le operazioni al computer, non dovrai fare nulla.
1b. Le variabili che hanno come valore le tue credenziali verranno distrutte per proteggere la tua privacy
1c. Il Browser, ovvero il WebDriver verrà eseguito in modalità INCOGNITO, ossia non salverà nessun dato in locale
1d. Prima di effettuare qualsiasi operazione, effettua il Login\n
2.  Sarà possibile eseguire la funzione di Logout quando si vuole. Quando avrai finito di condividere l'appello, utilizza Logout e lascia che il Bot esegue le sue operazioni
2a. La funzione di Logout uscirà dal tuo account sfruttando le funzioni di Facebook per non salvare nessun dato alla chiusura del WebDriver.\n
3.  Nel campo 'Importa / Esporta lista gruppi' è possibile importare da 'Importa' una lista precedentemente esportata
3a. Se non hai una lista, effettua il Login ed infine usa il pulsante Esporta, verrà esportata ed importata automaticamente la lista dei tuoi gruppi di Facebook
3b  Puoi modificare i gruppi prima di inviare l'appello, usando il tasto 'Modifica' ed eliminando l'intera riga del gruppo a cui non vuoi condividere l'appello
3c. E' possibile condividere su TUTTI i gruppi anche senza usare Esporta. Per farlo, esegui il login, imposta il messaggio ed infine usa Condividi\n
4.  Nel campo 'Messaggio da condividere' dovrai scrivere il tuo appello\n
5.  Nel campo 'Azioni' ci saranno 4 pulsanti
5a. Il pulsante 'Condividi' serve per, una volta effettuato il login ed inseriti tutti i campi, avviare l'autocondivisione
5b. Il pulsante 'Istruzioni' farà apparire questa schermata di avviso
5c. Il pulsante 'Sviluppatore' aprirà il browser di default sulla pagina Github dello sviluppatore (Colui che ha programmato ShareBOT)
5d. Il pulsante 'Esci' è una funzione di chiusura logica del programma, effettua delle verifiche sul funzionamento del WebDriver per chiudere i processi figli di ShareBOT\n\n
IMPORTANTE: Durante le operazioni, non sarà possibile utilizzare il programma. Il programma lavorerà da solo, non serve chiuderlo solo perchè 'non risponde' o sembra bloccato"""
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
        print("[LOG] Controllo se il WebDriver esiste")

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

                def progress_bar(current, total, width=None):
                    print("[LOG] Download del WebDriver in corso: %d%% [%d / %d] bytes" % (current / total * 100, current, total), end="\t\t\r")

                if version == "83":
                    wget.download(chrome83, dirFile + 'chromedriver_win32.zip', bar=progress_bar)
                    unzip(dirFile + 'chromedriver_win32.zip')
                elif version == "84":
                    wget.download(chrome84, dirFile + 'chromedriver_win32.zip', bar=progress_bar)
                    unzip(dirFile + 'chromedriver_win32.zip')
                elif version == "85":
                    wget.download(chrome85, dirFile + 'chromedriver_win32.zip', bar=progress_bar)
                    unzip(dirFile + 'chromedriver_win32.zip')
                else:
                    print("[LOG] Versione di Chrome non scritta nel programma, aggiorna Google Chrome ad una di queste tre versioni: 83, 84, 85")
                    messagebox.showerror('Errore', 'Versione di Chrome non scritta nel programma, aggiornare Google Chrome ad una di queste tre versioni: 83, 84, 85')
                    input("[LOG] Premi INVIO per continuare")
                    exit()

                print("[LOG] Rimozione del file zippato...")
                try:
                    from os import remove
                    if path.exists(dirFile+"chromedriver_win32.zip"):
                        remove(dirFile+"chromedriver_win32.zip")
                        print("[LOG] File zippato rimosso")
                    else:
                        print("[LOG] File zippato non esistente")
                except Exception as rem_zip:
                    print("[LOG] Rimozione del file zippato non riuscita")
                    pass
                print("[LOG] Avvio il programma")
            except Exception as e:
                print("[LOG] Errore durante il download del WebDriver: " + str(e))
                messagebox.showerror('Errore durante il download del WebDriver', str(e))
                input("[LOG] Premi INVIO per continuare")
                exit()
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

    def login(self, driver, url, session_id, chrome_options):
        try:
            print("[LOG] Eseguo il login")
            driver = webdriver.Remote(command_executor=url, desired_capabilities={}, options=chrome_options)
            driver.close()
            driver.session_id = session_id
            driver.get("https://mbasic.facebook.com/")
            element = driver.find_element_by_name("email")
            element.send_keys(self.username)
            print("[LOG] Email inserita: " + self.username)
            element = driver.find_element_by_name("pass")
            element.send_keys(self.password)
            print("[LOG] Password inserita: ***************")
            print("[LOG] Security: Rimozione delle variabili 'email' e 'password' in corso...")
            try:
                del self.username 
                del self.password
                print("[LOG] Security: Variabili rimosse, eseguo un secondo controllo...")

                # Controllo la variabile username
                if 'username' in dir(self):
                    if len(self.username) > 0:
                        print("[LOG] [WARNING] Security: Variabile 'username' NON rimossa con valore integro")
                    else:
                        print("[LOG] [WARNING] Security: Variabile 'username' NON rimossa ma senza valore")
                else:
                    print("[LOG] Security: Variabile 'username' inesistente [OKAY]")
                    pass

                # Controllo la variabile password
                if 'password' in dir(self):
                    if len(self.password)> 0:
                        print("[LOG] [WARNING] Security: Variabile 'password' NON rimossa con valore integro")
                    else:
                        print("[LOG] [WARNING] Security: Variabile 'password' NON rimossa ma senza valore")
                else:
                    print("[LOG] Security: Variabile 'password' inesistente [OKAY]")
                    pass

            except Exception as del_err:
                print("[LOG] Security Error: Non sono riuscito a rimuovere i valori delle variabili 'email' e 'password': " + str(del_err))
                pass
            else:
                print("[LOG] Security: Variabili rimosse correttamente")
                pass
            print("[LOG] Security: Rimozione del campo 'Password' dall'interfaccia grafica...", end="\r")
            try:
                password.delete(0, END) # Elimino la stringa della Entry
            except Exception as gui_delpass_err:
                print("[LOG] [WARNING] Security: Rimozione del campo 'Password' dall'interfaccia grafica NON riuscita: " + str(gui_delpass_err))
            else:
                print("[LOG] Security: Rimozione del campo 'Password' dall'interfaccia grafica... [OKAY]")
                pass
                
            driver.find_element_by_xpath('//*[@id="login_form"]/ul/li[3]/input').click()
            try:
                if driver.find_element_by_xpath('//*[@id="header"]/nav/a[1]'):
                    print("[LOG] Homepage rilevata. Login effettuato")
                    messagebox.showinfo("Informazione", 'Login effettuato')
            except:
                messagebox.showerror('WARNING', "Non sono riuscito a rilevare la homepage di Facebook, verifica se si è presentato un errore sul WebDriver o se Facebook ha bisogno di identificarti")
                print("[LOG] Warning: Non sono riuscito a rilevare la homepage di Facebook, verifica se si è presentato un errore sul WebDriver o se Facebook ha bisogno di identificarti")
                pass
        except Exception as login_err:
            print("[LOG] Error: Errore nella funzione 'login': " + str(login_err))
            messagebox.showerror("Errore nella funzione 'login'", str(login_err))
            pass
    
    def logout(self, driver, url, session_id, chrome_options):
        try:
            print("[LOG] Eseguo il logout")
            driver = webdriver.Remote(command_executor=url, desired_capabilities={}, options=chrome_options)
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
    
    def cond_with_list(self, driver, url, session_id, lista, post, chrome_options):
        try:
            if driver_process.is_running():
                chrome_process = driver_process.children()
                if chrome_process:
                    chrome_process = chrome_process[0]
                    if chrome_process.is_running():
                        driver = webdriver.Remote(command_executor=url, desired_capabilities={}, options=chrome_options)
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
                            try:
                                for i in range(randint(30, 40), 0, -1):
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
                                driver.quit()
                                print("[LOG] Warning: Condivisione interrotta")
                                messagebox.showwarning('Warning', 'Condivisione interrotta')
                                return

                        facebook_groups.clear()
                        print("[LOG] Condivisione completata")
                        messagebox.showinfo('Informazione', 'Condivisione completata')

                    else:
                        print("[LOG] Warning: Il WebDriver non è in esecuzione")
                        messagebox.showwarning('Warning', 'Il WebDriver non è in esecuzione')
                        pass                          
                else:
                    print("[LOG] Warning: Non ci sono processi figli del WebDriver")
                    messagebox.showwarning('Warning', 'Non ci sono processi figli del WebDriver')
                    pass
            else:
                print("[LOG] Warning: Processo del WebDriver non in servizio")
                messagebox.showwarning('Warning', 'Processo del WebDriver non in servizio')
                pass

        except Exception as cond_with_list_err:
            driver.quit()
            print("[LOG] Error: Errore nella funzione 'cond_with_list': " + str(cond_with_list_err))
            messagebox.showerror("Errore nella funzione 'cond_with_list'", str(cond_with_list_err))

    def cond_without_list(self, driver, url, session_id, post, chrome_options):
        try:
            if driver_process.is_running():
                chrome_process = driver_process.children()
                if chrome_process:
                    chrome_process = chrome_process[0]
                    if chrome_process.is_running():
                        driver = webdriver.Remote(command_executor=url, desired_capabilities={}, options=chrome_options)
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
                                try:
                                    for i in range(randint(30, 40), 0, -1):
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
                            facebook_groups.clear()
                            print("[LOG] Condivisione completata")
                            messagebox.showinfo('Informazione', 'Condivisione completata')
                        else:
                            print("[WARNING] Gruppi non trovati")
                            messagebox.showinfo('Warning', 'Gruppi non trovati')

                    else:
                        print("[LOG] Warning: Il WebDriver non è in esecuzione")
                        messagebox.showwarning('Warning', 'Il WebDriver non è in esecuzione')
                        pass                          
                else:
                    print("[LOG] Warning: Non ci sono processi figli del WebDriver")
                    messagebox.showwarning('Warning', 'Non ci sono processi figli del WebDriver')
                    pass
            else:
                print("[LOG] Warning: Processo del WebDriver non in servizio")
                messagebox.showwarning('Warning', 'Processo del WebDriver non in servizio')
                pass

        except Exception as cond_without_list_err:
            driver.quit()
            print("[LOG] Error: Errore nella funzione 'cond_without_list': " + str(cond_without_list_err))
            messagebox.showerror("Errore nella funzione 'cond_without_list'", str(cond_without_list_err))

    def get_groups(self, driver, url, session_id, chrome_options):
        try:
            driver = webdriver.Remote(command_executor=url,desired_capabilities={}, options=chrome_options)
            driver.close()
            driver.session_id = session_id
            print("[LOG] Estrazione dei gruppi in corso...")
            driver.get("https://mbasic.facebook.com/groups/")
            sleep(randint(2, 4))
            driver.find_element_by_xpath("//span[contains(text(),'Mostra tutti')]").click()
            sleep(randint(2, 4))
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
            print("[LOG] Error: Errore nella funzione 'get_groups': " + str(get_groups_err))
            messagebox.showerror("Errore nella funzione 'get_groups'", str(get_groups_err))
# Termine della classe
# Inizio funzioni out of class
def user_login():
    if len(email.get()) > 0:
        if len(password.get()) > 0:
            global utente
            global chrome_options
            chrome_options = Options()
            chrome_options.add_argument("--incognito") # Abilito la incognito mode
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging']) # Rimuovo lo status di logging
            chrome_options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2}) # Rimuovo JavaScript

            global driver
            if name == "nt":
                driver = webdriver.Chrome(executable_path=dirFile + 'chromedriver.exe', options=chrome_options)
            elif name == "posix":
                driver = webdriver.Chrome(executable_path=chromedriver, options=chrome_options)

            driver.set_window_size(400,800)
            global url, session_id, driver_process
            url = driver.command_executor._url
            session_id = driver.session_id 
            driver_process = psutil.Process(driver.service.process.pid)
            print("[LOG] WebDriver process: " + str(driver_process))
            print("[LOG] WebDriver session id: " + session_id)
            print("[LOG] Il WebDriver è nella modalità 'incognito/privata' quindi non verrà salvato nessun dato sul browser")
            utente = Webdriver(email.get(), password.get())
            utente.login(driver, url, session_id, chrome_options)
            pass
        else:
            print("[LOG] Campo password vuoto")
            messagebox.showwarning("Warning", "Campo PASSWORD vuoto")
            pass
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
                    utente.logout(driver, url, session_id, chrome_options)
                    pass
                else:
                    print("[LOG] Warning: Non posso eseguire il logout se il WebDriver non è attivo, esegui il LOGIN e riprova")
                    messagebox.showwarning('Warning', 'Non posso eseguire il logout se il WebDriver non è attivo, esegui il LOGIN e riprova')
                    pass
            else:
                print("[LOG] Error: Non ci sono processi figli del WebDriver, esegui il Login e riprova")
                messagebox.showwarning('Warning', 'Non ci sono processi figli del WebDriver, esegui il Login e riprova')
                pass
        else:
            print("[LOG] Warning: WebDriver non in funzione")
            messagebox.showwarning('Warning', 'WebDriver non in funzione')
            pass
    except Exception as user_logout_error:
        if str(user_logout_error) == "name 'driver_process' is not defined":
            print("[LOG] Error: Processo del WebDriver non valorizzato, effettua prima il Login")
            messagebox.showerror('Error', "Processo del WebDriver non valorizzato, effettua prima il Login")
            pass
        else:
            print("[LOG] Error: Problema nella funzione 'Logout': " + str(user_logout_error))
            messagebox.showerror("Problema nella funzione 'Logout'", str(user_logout_error))
            pass

def lista_import():
    try:
        ilist = askopenfilename(initialdir=dirFile, filetypes =(("File di test", "*.txt"),("All Files", "*.*")), title = "Importa la lista gruppi")
        lista.delete(0, END)
        lista.insert(0, ilist)
        pass
    except Exception as lista_import_err:
        print("[LOG] Error: Problemi nella funzione 'lista_import': " + str(lista_import_err))
        messagebox.showerror("Errore nella funzione 'lista_import'", str(lista_import_err))
        pass

def lista_export():
    try:
        if driver_process.is_running():
            print("[LOG] Controllo se il WebDriver è attivo per eseguire il logout")
            chrome_process = driver_process.children()
            if chrome_process:
                chrome_process = chrome_process[0]
                if chrome_process.is_running():
                    utente.get_groups(driver, url, session_id, chrome_options)
                    pass
                else:
                    print("[LOG] Warning: Non posso eseguire il logout se il WebDriver non è attivo, esegui il LOGIN e riprova")
                    messagebox.showwarning('Warning', 'Non posso eseguire il logout se il WebDriver non è attivo, esegui il LOGIN e riprova')
                    pass
            else:
                print("[LOG] Error: Non ci sono processi figli del WebDriver, esegui il Login e riprova")
                messagebox.showwarning('Warning', 'Non ci sono processi figli del WebDriver, esegui il Login e riprova')
                pass
        else:
            print("[LOG] Warning: WebDriver non in funzione")
            messagebox.showwarning('Warning', 'WebDriver non in funzione')
            pass
    except Exception as lista_export_err:
        if str(lista_export_err) == "name 'utente' is not defined":
            print("[LOG] Error: Effettua prima il Login")
            messagebox.showwarning('Warning', 'Effettua prima il Login')
            pass
        elif str(lista_export_err) == "name 'driver_process' is not defined":
            print('[LOG] Error: Processo del WebDriver non valorizzato, effettua prima il Login')
            messagebox.showwarning('Warning', 'Processo del WebDriver non valorizzato, effettua prima il Login')
            pass
        else:
            print("[LOG] Error: Errore nella funzione 'lista_export': " + str(lista_export_err))
            messagebox.showerror("Errore nella funzione 'lista_export'", str(lista_export_err))
            pass

def user_share():
    try:
        if driver_process.is_running():
            print("[LOG] Controllo se il WebDriver è attivo per eseguire il logout")
            chrome_process = driver_process.children()
            if chrome_process:
                chrome_process = chrome_process[0]
                if chrome_process.is_running():
                    if len(lista.get()) > 1:
                        if path.exists(lista.get()):
                            utente.cond_with_list(driver, url, session_id, lista.get(), post.get("1.0","end-1c"), chrome_options)
                            pass
                        else:
                            print("[LOG] Errore: La lista sembra non essere accessibile o forse è danneggiata")
                            messagebox.showerror('Errore', 'La lista sembra non essere accessibile o forse è danneggiata')
                            pass
                    else:
                        utente.cond_without_list(driver, url, session_id, post.get("1.0","end-1c"), chrome_options)
                        pass
                else:
                    print("[LOG] Warning: Non posso eseguire il logout se il WebDriver non è attivo, esegui il LOGIN e riprova")
                    messagebox.showwarning('Warning', 'Non posso eseguire il logout se il WebDriver non è attivo, esegui il LOGIN e riprova')
                    pass
            else:
                print("[LOG] Error: Non ci sono processi figli del WebDriver")
                messagebox.showwarning('Warning', 'Non ci sono processi figli del WebDriver, esegui il Login e riprova')
                pass
        else:
            print("[LOG] Warning: WebDriver non in funzione")
            messagebox.showwarning('Warning', 'WebDriver non in funzione')
            pass
    except Exception as user_share_err:
        if str(user_share_err) == "name 'utente' is not defined":
            print("[LOG] Error: Effettua prima il Login")
            messagebox.showwarning('Warning', 'Effettua prima il Login')
            pass
        elif str(user_share_err) == "name 'driver_process' is not defined":
            print("[LOG] Error: Processo del WebDriver non valorizzato, effettua prima il Login")
            messagebox.showerror('Error', "Processo del WebDriver non valorizzato, effettua prima il Login")
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
        pass

def sviluppatore():
    if name == "nt":
        print("[LOG] Apertura del profilo Github dello sviluppatore")
        startfile("https://github.com/FebVeg")
    elif name == "posix":
        print("[LOG] Apertura del profilo Github dello sviluppatore")
        system("xdg-open https://github.com/FebVeg")

def user_exit():
    try:         
        if driver_process.is_running():
            chrome_process = driver_process.children()
            if chrome_process:
                chrome_process = chrome_process[0]
                if chrome_process.is_running():
                    # Il WebDriver è attivo, chiudo il programma
                    driver.quit()
                    master.destroy()
                    exit()
                else:
                    # Il WebDriver non è attivo, eseguo la kill del processo
                    chrome_process.kill()
                    master.destroy()
                    exit()
            else:
                # Non ci sono processi figli del WebDriver
                master.destroy()
                exit()
        else:
            # WebDriver non in funzione
            master.destroy()
            exit()
    except Exception as user_exit_err:
        print("[LOG] Error: Errore nella funzione 'user_exit': " + str(user_exit_err))
        master.destroy()
        exit()

master = tk.Tk()
master.title("ShareBOT - V2.3.7-1 - FebVeg")
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
# attaccatura della scrollbar sulla textbox
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