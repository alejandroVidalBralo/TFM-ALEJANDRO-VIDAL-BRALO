import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import pickle
import matplotlib.pyplot as plt
import numpy as np
from src.comun.perturbaciones import consumos1200_pb


#Gráfica lazo abierto
with open("data/medusa/lazoAbierto.pkl", "rb") as f:
    datos = pickle.load(f)

plt.figure(figsize=(10,5))
plt.plot(datos[50:], linestyle='-', label = "Nivel depósito")
plt.plot(35*np.ones(len(datos)-50), color = 'r', linestyle='--', label = 'SP')

plt.xlabel('Tiempo (s)')
plt.ylabel('Nivel (%)')
plt.title(f'Lazo abierto')
plt.grid(True)

plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), fancybox=True, shadow=True, ncol=5)
plt.tight_layout()
plt.show()


#Gráfica Relay-Feedback

with open("data/medusa/datosRelayFeedBack.pkl", "rb") as f:
    datos = pickle.load(f)

plt.figure(figsize=(10,5))
plt.plot(datos[50:], linestyle='-', label = "Nivel depósito")
plt.plot(55*np.ones(len(datos)-50), color = 'r', linestyle='--', label = 'Limite superior histéresis')
plt.plot(45*np.ones(len(datos)-50), color = 'r', linestyle='--', label = 'Limite inferior histéresis')

plt.xlabel('Tiempo (s)')
plt.ylabel('Nivel (%)')
plt.title(f'Relay Feedback')
plt.grid(True)

plt.tight_layout()
plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.125), fancybox=True, shadow=True, ncol=5)
plt.show()



#Gráfica regulador PI
def graph_PI(datos):
    plt.figure(figsize=(10, 8))
    plt.plot(50*np.ones(len(datos)), color='r', linestyle='-', label="Setpoint")
    plt.plot(datos[:], linestyle='-', label="Nivel depósito")
    plt.plot([np.argmax(datos), np.argmax(datos)], [50, datos[np.argmax(datos)]], color='blue', linestyle='--', label="Sobreoscilación")
    plt.title(f'Controlador PI: sobreoscilación del {(datos[np.argmax(datos)] - 50) /0.5:.2f} %')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Nivel (%)')
    plt.grid(True)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=5)
    plt.tight_layout()

with open("data/medusa/PI1_nivel.pkl", "rb") as f:
    datos1 = pickle.load(f)[:600]

with open("data/medusa/PI2_nivel.pkl", "rb") as f:
    datos2 = pickle.load(f)[:600]

with open("data/medusa/perPI7_nivel.pkl", "rb") as f:
    datos3 = pickle.load(f)[:600]

graph_PI(datos1)
graph_PI(datos2)
graph_PI(datos3)
plt.show()




#Graficar PI + feedforward
def graph_PI_feedforward(datos, cv, caudal):

    plt.figure(figsize=(10,5))
    plt.subplot(2,1,1)
    plt.plot(datos, linestyle='-', label = "Nivel depósito")
    plt.plot(cv, linestyle='-', label = "CV")
    plt.plot(np.ones(1200)*50, linestyle='-', label = "Set Point")
    plt.plot(consumos1200_pb[:], linestyle='-', label = "Consigna válvula")
    plt.plot([np.argmax(datos), np.argmax(datos)], [50, datos[np.argmax(datos)]], color='blue', linestyle='--', label="Sobreoscilación")
    plt.title(f'Controlador PI con Feedforward: sobreoscilación del {(datos[np.argmax(datos)] - 50) /0.5:.2f} %')
    plt.legend()

    plt.xlabel('Tiempo (s)')
    plt.ylabel('Nivel (%)')
    plt.subplot(2,1,2)
    plt.plot(caudal, linestyle='-', label = "Caudal")

    plt.xlabel('Tiempo (s)')
    plt.ylabel('Caudal (l/s)')
    plt.legend()

with open("data/medusa/perPI2_nivel.pkl", "rb") as f:
    datos = pickle.load(f)[600:]

with open("data/medusa/perPI2_valvula.pkl", "rb") as f:
    caudal = pickle.load(f)[600:]

with open("data/medusa/perPI2_cv.pkl", "rb") as f:
    cv = pickle.load(f)[600:]

with open("data/medusa/perPI3_nivel.pkl", "rb") as f:
    datos2 = pickle.load(f)[600:]

with open("data/medusa/perPI3_valvula.pkl", "rb") as f:
    caudal2 = pickle.load(f)[600:]

with open("data/medusa/perPI3_cv.pkl", "rb") as f:
    cv2 = pickle.load(f)[600:]

with open("data/medusa/perPI5_nivel.pkl", "rb") as f:
    datos3 = pickle.load(f)[600:]

with open("data/medusa/perPI5_valvula.pkl", "rb") as f:
    caudal3 = pickle.load(f)[600:]

with open("data/medusa/perPI5_cv.pkl", "rb") as f:
    cv3 = pickle.load(f)[600:]

with open("data/medusa/perPI7_nivel.pkl", "rb") as f:
    datos4 = pickle.load(f)[600:]

with open("data/medusa/perPI7_valvula.pkl", "rb") as f:
    caudal4 = pickle.load(f)[600:]

with open("data/medusa/perPI7_cv.pkl", "rb") as f:
    cv4 = pickle.load(f)[600:]

graph_PI_feedforward(datos, cv, caudal)
graph_PI_feedforward(datos2, cv2, caudal2)
graph_PI_feedforward(datos3, cv3, caudal3)
graph_PI_feedforward(datos4, cv4, caudal4)

plt.show()
