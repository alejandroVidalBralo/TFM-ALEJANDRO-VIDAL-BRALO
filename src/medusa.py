from opcua import Client, ua
import time
import pickle
import matplotlib.pyplot as plt
from opc_manager_medusa import bomba1, deposito, bomba2, valvula_entrada, valvula_recirculacion, valvula_salida_dep, valvula_grandes, opc_manager_control, caudalimetro_grandes
from src.GENERAL.PID import PID, PID_FeedForward
from src.GENERAL.perturbaciones import consumos1200_pb

def lazo_abierto(duracion: int = 1800):

    valvula_entrada.position = 35
    valvula_salida_dep.position = 50
    valvula_grandes.position = 50
    valvula_recirculacion.position = 65

    #Se da tiempo a las válvulas a recolocarse
    time.sleep(60)


    bomba1.power = True
    bomba2.power = True

    nivel_historico = []

    try:
        for i in range(1200):
            tiempo_inicio = time.time()

            nivel = deposito.nivel
            nivel_historico.append(nivel)

            #Se asegura tiempo de muestreo constante
            time.sleep(1 - (tiempo_inicio-time.time()))

    except:

        #Se apagan las bombas en caso de error durante la ejecucción
        bomba1.power = False
        bomba2.power = False


    #Se guardan las 
    with open("src/data/med/lazoAbierto.pkl", "wb") as f:
        pickle.dump(nivel_historico, f)


    #Se cierra conexión con el servidor OPC
    opc_manager_control.disconnect()

def relay_feedback(duracion: int = 1800):

    nivel_historico = []
    bomba1.power = True
    bomba2.power = True
    valvula_entrada.position = 50
    valvula_salida_dep.position = 50
    valvula_grandes.position = 50
    valvula_recirculacion.position = 50

    try:

        while True:

            inicio = time.time()
            nivel = deposito.nivel

            if nivel < 45:
                
                valvula_entrada.position = 100
                valvula_recirculacion.position = 0

            elif  nivel > 55:
                valvula_entrada.position = 0
                valvula_recirculacion.position = 100

            nivel_historico.append(nivel)
            print(nivel)

            time.sleep(1 - (inicio-time.time()))


    except:
        bomba1.power = False
        bomba2.power = False  


    with open("med/datosRelayFeedBack.pkl", "wb") as f:
        pickle.dump(medidas, f)


    opc_manager_control.disconnect()


#CONTROLADOR PI
valvula_entrada.position = 100
valvula_recirculacion.position = 0
valvula_salida_dep.position = 50
valvula_grandes.position = 50

bomba1.power = True
bomba2.power = True

'''
#pid = PID(1.96, 70, 0, 1, 8)
#pid = PID(1.7, 140, 0, 1, 8)
#pid = PID_FeedForward(1.45, 180, 0, 1, 8, anti_windup=100, feedforward_gain=0)
#pid = PID_FeedForward(1.45, 180, 0, 1, 8, anti_windup=100, feedforward_gain=1)
#pid = PID_FeedForward(1.45, 180, 0, 1, 8, anti_windup=100, feedforward_gain=3)
#pid = PID_FeedForward(1.45, 180, 0, 1, 8, anti_windup=100, feedforward_gain=2)
#pid = PID_FeedForward(1.45, 180, 0, 1, 8, anti_windup=100, feedforward_gain=4)
pid = PID_FeedForward(1.45, 180, 0, 1, 8, anti_windup=100, feedforward_gain=4)

'''

i = 0
try:
    while True:

        i += 1
        inicio = time.time()
        nivel_valor = deposito.nivel
        valor = pid.control(nivel_valor, 50)

        valvula_entrada.position = valor
        valvula_recirculacion.position = 100-valor

        print(nivel_valor)
        medidas.append(nivel_valor)
        setpoint.append(50)
        cv.append(valor)

        update_plot()
        print(i)

        time.sleep(1 - (inicio-time.time()))

except:
    bomba1.power = False
    bomba2.power = False

with open("med/PI3_nivel.pkl", "wb") as f:
    pickle.dump(medidas, f)

with open("med/PI3_cv.pkl", "wb") as f:
    pickle.dump(cv, f)

opc_manager_control.disconnect()



#SIMULACIÓN DE CONSUMOS / PERTURBACIONES
medidas = []
flow = []
setpoint = []
cv = []
valvula = []   



valvula_entrada.position = 100
valvula_recirculacion.position = 0
valvula_salida_dep.position = 50

bomba1.power = True
bomba2.power = True

#Llevamos el sistema a regimen permanente
for i in range(600):

    inicio = time.time()
    nivel_valor = deposito.nivel
    valor = pid.control(nivel_valor, 50, disturbance = 0)
    valvula_entrada.position = valor
    valvula_recirculacion.position = 100-valor
    valvula.append(valvula_grandes.position)

    medidas.append(nivel_valor)
    cv.append(valor)
    print(i)
    caudal = caudalimetro_grandes.caudal
    flow.append(caudal)
    setpoint.append(50)
    update_plot()

    time.sleep(1 - (inicio-time.time()))


#Simulamos consumos.
for i in range(1200):

    inicio = time.time()
    nivel_valor = deposito.nivel
    caudal = caudalimetro_grandes.caudal
    valor = pid.control(nivel_valor, 50, disturbance = 3.4 - caudal)

    valvula_entrada.position = valor
    valvula_recirculacion.position = 100-valor
    cv.append(valor)
    valvula.append(valvula_grandes.position)
    medidas.append(nivel_valor)
    valvula_grandes.position = consumos1200_pb[i]
    flow.append(caudal)
    setpoint.append(50)
    update_plot()


    print(i)
    time.sleep(1 - (inicio-time.time()))

bomba1.power = False
bomba2.power = False


with open("med/perPI7_nivel.pkl", "wb") as f:
    pickle.dump(medidas, f)

with open("med/perPI7_valvula.pkl", "wb") as f:
    pickle.dump(flow, f)

with open("med/perPI7_cv.pkl", "wb") as f:
    pickle.dump(cv, f)









