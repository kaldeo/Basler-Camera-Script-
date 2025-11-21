from flask import Flask, render_template, Response, send_from_directory
from pypylon import pylon
from datetime import datetime
import time
import os
import cv2
import json
import threading
import logging

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # Dossier src/
DOSSIER_IMAGES = os.path.join(SCRIPT_DIR, "images")
app = Flask(__name__, static_folder=SCRIPT_DIR, template_folder=SCRIPT_DIR)
app.static_url_path = '/static'

# Désactiver les logs Flask
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# GLOBALES VARIABLES
active_camera = None
derniere_image = None
capture_en_cours = False
intervalle_capture = 3

# FONCTIONS
def lancer_cam():
    global active_camera
    if active_camera is not None:
        print(f"[OTHER] Caméra déjà lancée")
    MAX_TENTATIVES = 5
    DELAI_SECONDES = 0
    for tentative in range(MAX_TENTATIVES):
        try:
            camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
            camera.Open()
            active_camera = camera 
            print(f"[OK] Caméra Lancée")
            return
        except Exception as e:
            if tentative < MAX_TENTATIVES - 1:
                print(f"[KO] Tentative {tentative + 1} échouée.")
                time.sleep(DELAI_SECONDES)
            else:
                print(f"[KO] Echec de connexion après {MAX_TENTATIVES} tentatives. Détails : {e}")

def fermer_cam():
    global active_camera
    if active_camera is None:
        print(f"[OTHER] La caméra n'est pas active.")
    try:
        active_camera.Close()
        active_camera = None
        print(f"[OK] Caméra fermée")
        return 
    except Exception as e:
        active_camera = None 
        print(f"[KO] Erreur lors de la fermeture de la caméra : {e}")
        return

def capture_image(camera):
    global derniere_image
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    nom_fichier = f"capture_{timestamp}.png"
    chemin_fichier_complet = os.path.normpath(os.path.join(DOSSIER_IMAGES, nom_fichier))
    try:
        if camera is None :
             print(f"[KO] Caméra inactive pour la capture.")
             return False
        camera.TriggerMode.SetValue("Off")
        camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
        grabResult = camera.RetrieveResult(10000, pylon.TimeoutHandling_ThrowException)

        if grabResult.GrabSucceeded():
            image_en_nombres = grabResult.GetArray()
            is_success, buffer = cv2.imencode(".png", image_en_nombres)
            if is_success:
                with open(chemin_fichier_complet, 'wb') as f:
                    f.write(buffer)
                print(f"[OK] Image enregistree sous")
                
                derniere_image = nom_fichier
            else:
                print(f"[KO] Erreur lors de l'encodage de l'image")
                
            grabResult.Release()
            camera.StopGrabbing()
            return is_success, nom_fichier if is_success else "[KO] Encodage échoué"
        else:
            print("[KO] Echec de la capture de l'image (GrabSucceeded = False).")
            grabResult.Release()
            camera.StopGrabbing()
            return False, "[KO] Echec de la capture."
    except Exception as e:
        print(f"[KO] Erreur lors de l'acquisition de l'image. Details : {e}")
        if camera and camera.IsGrabbing():
            camera.StopGrabbing()
        return False, f"Erreur de capture : {e}"

def capture_continue():
    global capture_en_cours
    global intervalle_capture
    print(f"[INFO] Thread de capture démarré")
    while capture_en_cours:
        if active_camera:
            capture_image(active_camera)
            time.sleep(intervalle_capture)
        else:
            time.sleep(1)
    print(f"[INFO] Thread de capture arrêté")

# ROUTES FLASK
@app.route('/')
def index():
    return render_template('basler.html', image_path='/images/cap_default.png', timestamp=time.time())

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(SCRIPT_DIR, filename)

@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory(DOSSIER_IMAGES, filename)

@app.route('/stream')
def stream():
    def event_stream():
        last_sent = None
        while True:
            if derniere_image and derniere_image != last_sent:
                last_sent = derniere_image
                data = json.dumps({'image': f'/images/{derniere_image}', 'timestamp': time.time()})
                yield f"data: {data}\n\n"
            time.sleep(0.5)
    
    return Response(event_stream(), mimetype='text/event-stream')


if __name__ == '__main__':
    lancer_cam()
    
    if active_camera:
        capture_en_cours = True
        thread_capture = threading.Thread(target=capture_continue, daemon=True)
        thread_capture.start()
        
        print(f"[INFO] Serveur Flask démarré sur http://localhost:5000")
        
        try:
            app.run(debug=False, threaded=True, port=5000, use_reloader=False)
        except KeyboardInterrupt:
            print(f"\n[INFO] Arrêt du serveur...")
        finally:
            capture_en_cours = False
            time.sleep(1)
            fermer_cam()
    else:
        print(f"[KO] Impossible de démarrer sans caméra active")
