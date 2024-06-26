import pickle
import matplotlib.pyplot as plt
import numpy as np


#Grafico lazo abierto
with open("data/laboratorio/lazoAbierto.pkl", "rb") as f:
    datos = pickle.load(f)

plt.figure(figsize=(10,5))
plt.plot(datos[50:], linestyle='-', label = "Nivel depósito")
plt.plot(50*np.ones(len(datos)-50), color = 'r', linestyle='--', label = 'SP')

plt.xlabel('Tiempo (s)')
plt.ylabel('Nivel (%)')
plt.title(f'Lazo abierto')
plt.grid(True)

plt.tight_layout()
plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.125), fancybox=True, shadow=True, ncol=5)
plt.show()



#Gráfico Relay-Feedback
with open("data/laboratorio/datosRelayFeedBack.pkl", "rb") as f:
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



#Gráficos regulador PI
def graph_pi(datos):

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

with open("data/laboratorio/PI1_nivel.pkl", "rb") as f:
    datos1 = pickle.load(f)[:180]

with open("data/laboratorio/PI2_nivel.pkl", "rb") as f:
    datos2 = pickle.load(f)[:180]

with open("data/laboratorio/PI3_nivel.pkl", "rb") as f:
    datos3 = pickle.load(f)[:180]

with open("data/laboratorio/PI4_nivel.pkl", "rb") as f:
    datos4 = pickle.load(f)[:180]

graph_pi(datos1)
graph_pi(datos2)
graph_pi(datos3)
graph_pi(datos4)
plt.show()



#Gráficos regulador PI + feedforward.
def graph_pi_feedforward(datos, valvula, cv):

    plt.figure(figsize=(10,5))
    plt.plot(datos[-650:], linestyle='-', label = "Nivel depósito")
    plt.plot(valvula[-650:], linestyle='-', label = "Consigna válvula")
    plt.plot(cv[-650:], linestyle='-', label = "CV")
    plt.plot(np.ones(650)*50, linestyle='-', label = "Set Point")
    plt.plot([np.argmax(datos[-650:]), np.argmax(datos[-650:])], [datos[-650:][np.argmax(datos[-650:])], 50], color='blue', linestyle='--', label="Sobreoscilación")
    plt.title(f'Controlador PI + Feedforward: Sobreoscilación máxima del {(datos[-650:][np.argmax(datos[-650:])] - 50) /0.5:.2f} %')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Nivel (%)')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=5)
    plt.tight_layout()

with open("data/laboratorio/datosPI_nivel.pkl", "rb") as f:
    datos = pickle.load(f)

with open("data/laboratorio/datosPI_valvula.pkl", "rb") as f:
    valvula = pickle.load(f)

with open("data/laboratorio/datosPI_cv.pkl", "rb") as f:
    cv = pickle.load(f)

with open("data/laboratorio/datosPI2_nivel.pkl", "rb") as f:
    datos2 = pickle.load(f)

with open("data/laboratorio/datosPI2_valvula.pkl", "rb") as f:
    valvula2 = pickle.load(f)

with open("data/laboratorio/datosPI2_cv.pkl", "rb") as f:
    cv2 = pickle.load(f)

with open("data/laboratorio/datosPI3_nivel.pkl", "rb") as f:
    datos3 = pickle.load(f)

with open("data/laboratorio/datosPI3_valvula.pkl", "rb") as f:
    valvula3 = pickle.load(f)

with open("data/laboratorio/datosPI3_cv.pkl", "rb") as f:
    cv3 = pickle.load(f)

with open("data/laboratorio/datosPI4_nivel.pkl", "rb") as f:
    datos4 = pickle.load(f)

with open("data/laboratorio/datosPI4_valvula.pkl", "rb") as f:
    valvula4 = pickle.load(f)

with open("data/laboratorio/datosPI4_cv.pkl", "rb") as f:
    cv4 = pickle.load(f)

graph_pi_feedforward(datos, valvula, cv)
graph_pi_feedforward(datos2, valvula2, cv2)
graph_pi_feedforward(datos3, valvula3, cv3)
graph_pi_feedforward(datos4, valvula4, cv4)

plt.show()



