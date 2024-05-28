#import pywhatkit
import time
import random
import pyautogui
from pynput.keyboard import Key, Controller
import requests
current_time = time.localtime()
hour = current_time.tm_hour
minute = current_time.tm_min + 1
keyboard = Controller()
def sendmes(number, sms):
    # send = pywhatkit.sendwhatmsg_instantly(
    #     number, 
    #     sms,
    #     15,
    #     False,
    #     5
        
    
    # )
    # time.sleep(1)
    # pyautogui.click()
    # time.sleep(1)
    # keyboard.press(Key.enter)
    # keyboard.release(Key.enter)
    # time.sleep(5)
    # with keyboard.pressed(Key.ctrl.value):
    #     keyboard.press('w')
    #     keyboard.release('w')
    # if send:
    #     print("Message send succeffully")
    # else:
    #     print("Error, send message")
    api_url = "http://10.68.132.2:3000/api/sendText/"

    # Remplacez ces données par le corps de votre requête
    payload = {
        "chatId": number,
        "text": sms,
        "session": "default"
    }

    headers = {
        "Content-Type": "application/json",
    }

    try:
        # Effectuer la requête POST
        response = requests.post(api_url, json=payload, headers=headers)

        # Vérifier si la requête a réussi (code 2xx)
        if response.status_code // 100 == 2:
            print("Requête POST réussie!")
        else:
            print(f"Échec de la requête POST. Code d'erreur: {response.status_code}")
            print("Réponse du serveur:", response.text)

    except Exception as e:
        print(f"Une erreur s'est produite: {e}")