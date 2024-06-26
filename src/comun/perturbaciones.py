import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from scipy.signal import convolve

#Se establecen los consumos y se adaptan a un rango de valores para cada planta.
consumos = [0.145, 0.091, 0.067, 0.223, 0.059, 0.049, 0.083, 0.477, 0.206, 0.176, 0.216, 0.319, 0.421, 0.339, 0.409, 0.405, 0.253, 0.352, 0.384, 0.232, 0.187, 0.163, 0.137, 0.195]
consumos_escalados = [(valor - min(consumos)) / (max(consumos) - min(consumos)) * (75 - 25) + 25 for valor in consumos] 
consumos_escalados_1200 = [(valor - min(consumos)) / (max(consumos) - min(consumos)) * (85 - 35) + 35 for valor in consumos] 

#Se distribuyen de forma uniforme los consumos escalados sobre un vector de ceros del tamaño final deseado
consumos600 = np.zeros(600)
consumos600[::25] = consumos_escalados

consumos1200 = np.zeros(1200)
consumos1200[::50] = consumos_escalados_1200



#Se realiza una interpolación para obtener todos los valores faltantes
indices = np.where(consumos600 != 0)[0]
interpoladora = interp1d(indices, consumos600[indices], kind='linear', fill_value='extrapolate')
consumos600 = interpoladora(np.arange(len(consumos600)))

indices = np.where(consumos1200 != 0)[0]
interpoladora = interp1d(indices, consumos1200[indices], kind='linear', fill_value='extrapolate')
consumos1200 = interpoladora(np.arange(len(consumos1200)))


#Se filtra la señal obtenida para suavizarla.
filtro_pb = np.ones(50)/50
consumos600_pad = np.pad(consumos600, (50,50), mode='edge')
consumos600_pb = convolve(consumos600_pad, filtro_pb, 'same')
consumos600_pb = consumos600_pb[50:650]

consumos1200_pad = np.pad(consumos1200, (50,50), mode='edge')
consumos1200_pb = convolve(consumos1200_pad, filtro_pb, 'same')
consumos1200_pb = consumos1200_pb[50:1250]



if __name__ == "__main__":

    #Se representa las curvas de consumo obtenidas filtradas y sin filtrar.
    plt.figure()
    plt.plot(consumos600)
    plt.plot(consumos600_pb)
    plt.plot(consumos1200)
    plt.plot(consumos1200_pb)
    plt.show()