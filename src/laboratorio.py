import time
import pickle
import matplotlib.pyplot as plt

#Se importan el regular y el vector con los consumos que simula las perturbaciones
from comun.regulador import PI_FeedForward
from comun.perturbaciones import consumos600_pb

#Se importan los dispositivos a utilizar
from comun.opc_manager import opc_manager_control, bomba, deposito, discharge_valve


def lazo_abierto(duracion:int = 600, SP:int = 50):

    '''
    Función por el cual se implementa la regulación en lazo abierto.

    Args:

    duracion (int): tiempo durante el que se desea llevar a cabo el experimento.
    SP (int): setpoint que se desea establecer para la regulación
    '''

    #Se establecen las condiciones del control
    bomba.power = True
    bomba.speed = SP
    nivel_historico = []

    #Se registra el valor del nivel durante el tiempo establecido
    for _ in range(duracion):

        tiempo_inicio = time.time()

        nivel = deposito.nivel
        nivel_historico.append(nivel)

        time.sleep(1 - (tiempo_inicio-time.time()))


    #Se guardan los datos del nivel y se apaga la bomba
    bomba.power = False
    with open("data/laboratorio/lazoAbierto.pkl", "wb") as f:
        pickle.dump(nivel_historico, f)

def relay_feedback(duracion:int):

    '''
    Función por el cual se implementa el método del relay feedback.

    Args:

    duracion (int): tiempo durante el que se desea llevar a cabo la histéresis.
    '''

    nivel_historico = []

    #Se enciende la bomba
    bomba.power = True

    #Se lleva a cabo el control y registro del nivel durante el tiempo establecido
    for _ in range(duracion):

        inicio = time.time()
        nivel_dep = deposito.nivel

        #Histéresis
        if nivel_dep < 45:
            bomba.power =  True

        elif  nivel_dep > 55:
            bomba.power =  False

        nivel_historico.append(nivel_dep)
        print(nivel_dep)

        time.sleep(1 - (inicio-time.time()))


    #Se guardan los datos del nivel y se apaga la bomba
    bomba.speed = 0

    with open("data/laboratorio/datosRelayFeedBack.pkl", "wb") as f:
        pickle.dump(nivel_historico, f)

def pi_ff_perturbaciones(regulador:PI_FeedForward, pertubaciones:bool):

    '''
    Función por el cual se implementa un regulador y opcionalmente se pueden simular perturbaciones una vez en régimen permananente

    Args:

    regulador (PI_FeedForward): regulador seleccionado para ejecutar el control.
    perturbaciones (bool): condición para simular o no perturbaciones.
    '''
 
    nivel_historico = []
    valvula = []
    setpoint = []
    cv_historico = []

    #Se inicia una gráfica en tiempo real para visualizar las variables de interes.
    plt.ion()
    fig, ax = plt.subplots()
    ax.set_xlabel('Tiempo (segundos)')
    ax.set_ylabel('Valor')
    ax.set_title('Gráfica en tiempo real')

    # Función para actualizar el gráfico
    def update_plot():
        ax.clear()

        ax.plot(nivel_historico, label='Nivel del depósito')
        ax.plot(valvula, label='Válvula')
        ax.plot(setpoint, label='SP')
        ax.plot(cv_historico, label='CV')

        ax.legend()
        ax.set_xlabel('Tiempo (segundos)')
        ax.set_ylabel('Valor')
        ax.set_title('Gráfica en tiempo real')

        plt.pause(0.01)


    #Se enciende la bomba, pero en parado
    bomba.power = True
    bomba.speed = 0

    #Se ejecuta el regulador PI y se guardan los datos de las variables de interés durante el tiempo necesario para alcanzar el régimen permante
    for _ in range(120):

        inicio = time.time()

        nivel = deposito.nivel

        cv = regulador.control(nivel, 50)
        bomba.speed = cv

        nivel_historico.append(nivel)        
        cv_historico.append(cv)
        valvula.append(discharge_valve.position)
        setpoint.append(50)

        update_plot()
        time.sleep(1 - (inicio-time.time()))



    if pertubaciones:
        #Simulamos consumos si selecciona esa opción, se sigue empleando el regulador y registrando las vriables de interés
        for i in range(600):

            inicio = time.time()

            nivel = deposito.nivel
            cv = regulador.control(nivel, 50, disturbance = (50 - discharge_valve.position))
            bomba.speed = cv
            discharge_valve.position = consumos600_pb[i]

            cv_historico.append(cv)
            nivel_historico.append(nivel)
            valvula.append(discharge_valve.position)
            setpoint.append(50)

            update_plot()
            time.sleep(1 - (inicio-time.time()))

    

    #Se guardan los datos y se apaga la bomba
    bomba.power = False

    with open("data/laboratorio/nivel.pkl", "wb") as f:
        pickle.dump(nivel_historico, f)

    with open("data/laboratorio/valvula.pkl", "wb") as f:
        pickle.dump(valvula, f)

    with open("data/laboratorio/cv.pkl", "wb") as f:
        pickle.dump(cv, f)

def regulador_simple(regulador:PI_FeedForward):

    '''
    Función por el cual se ejecuta un regulador por tiempo indefinido.
    En caso de error se detiene su ejecución parando la bomba por seguridad.

    Args:

    regulador (PI_FeedForward): regulador seleccionado para ejecutar el control.
    '''
    
    bomba.power = True

    try:
        while True:

            inicio = time.time()

            bomba.speed = regulador.control(deposito.nivel, 50, disturbance = 50 - discharge_valve.position)
            
            time.sleep(1 - (inicio-time.time()))
    
    except:

        bomba.power = False


if __name__ == "__main__":

    pi_ff = PI_FeedForward(2.5, 62, 1, feedforward_gain=0.625)
    regulador_simple(pi_ff)
    opc_manager_control.disconnect()





#pid = PID(2.64, 18.25, 0, 1, 8)
#pid = PID(2.6, 28, 0, 1, 8)
#pid = PID(2.55, 50, 0, 1, 8)
#pid = PID_FeedForward(2.5, 62, 0, 1, 8)
#pid = PID_FeedForward(2.5, 62, 0, 1, 8, feedforward_gain=0)
#pid = PID_FeedForward(2.5, 62, 0, 1, 8, feedforward_gain=1)
#pid = PID_FeedForward(2.5, 62, 0, 1, 8, feedforward_gain=0.5)

































        



