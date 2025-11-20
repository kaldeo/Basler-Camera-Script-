from pypylon import pylon

try:
    devices = pylon.TlFactory.GetInstance().EnumerateDevices()
    
    if len(devices) == 0:
        print("Aucune caméra Basler détectée")
    else:
        print(f"{len(devices)} caméra(s) Basler détectée(s)")
        for i, device in enumerate(devices, 1):
            print(f"   Caméra {i}: {device.GetModelName()} - S/N: {device.GetSerialNumber()}")
            
except Exception as e:
    print(f"Erreur : {e}")
