class PI_FeedForward():
    def __init__(self, KP:float, TI:float, ts:float, feedforward_gain: float = 0):

        # Inicialización de parámetros
        self._KP = KP
        self._TI = TI
        self._ts = ts
        self._feedforward_gain = feedforward_gain

        # Cálculo coeficiente
        self._C1 = ts / (2 * TI)

        # Inicialización de variables
        self._error = 0
        self._error_anterior = 0
        self._integral = 0
        self._integral_anterior = 0


    def control(self, PV:float, SP:float, disturbance: float = 0) -> float:

        # Cálculo del error
        self._error = SP - PV

        # Cálculo de términos PI
        self._integral = self._C1 * (self._error + self._error_anterior) + self._integral_anterior

        # Cálculo de término feedforward
        FF = self._feedforward_gain * disturbance

        # Cálculo de la acción de control
        CV = self._KP * (self._error + self._integral) - FF

        # Actualización de variables
        self._error_anterior = self._error
        self._integral_anterior = self._integral

        #Restricción entre 0 y 100 de la acción de control
        return CV if 0 < CV < 100 else 0 if CV < 0 else 100 




