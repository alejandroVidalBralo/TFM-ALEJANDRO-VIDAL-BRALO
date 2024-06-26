from opcua import Client, ua
from opcua.common.node import Node
import inspect, os


#Se determina desde donde se está importando este módulo
stack = inspect.stack()
frame = stack[1]  
module = inspect.getmodule(frame[0]).__file__
modulo_importador = os.path.basename(module)

#Según el script que esté importando este código se incializarán las variables para MEDUSA#4 o la planta de controles varios.
if modulo_importador == "medusa.py":

    class BombaHidraulica():
        '''Clase que permite comandar una bomba hidráulica.

        Args:
            nodo_encendido (Node): Nodo OPC UA que controla el encendido de la bomba.
        '''

        def __init__(self, nodo_encendido: Node):
            '''Inicializa la bomba con el nodo de encendido.'''
            self._power_node = nodo_encendido

        @property
        def power(self):
            '''Obtiene el estado de encendido de la bomba.

            Returns:
                bool: Verdadero si la bomba está encendida, falso en caso contrario.
            '''
            return self._power_node.get_value()
        
        @power.setter
        def power(self, power: bool):
            '''Establece el estado de encendido de la bomba.

            Args:
                power (bool): Verdadero para encender la bomba, falso para apagarla.
            '''
            self._power_node.set_value(OPC_Manager.valor_bool(power))

    class ValvulaProporcional():
        '''Clase que permite comandar una válvula proporcional.

        Args:
            nodo_comando (Node): Nodo OPC UA que controla el comando de la válvula.
            nodo_estado (Node): Nodo OPC UA que controla el estado de la válvula.
        '''

        def __init__(self, nodo_comando: Node, nodo_estado: Node):
            '''Inicializa la válvula con los nodos de comando y estado.'''
            self._command_node = nodo_comando
            self._state_node = nodo_estado

        @property
        def position(self):
            '''Obtiene la posición de la válvula.

            Returns:
                int: Posición actual de la válvula.
            '''
            return self._state_node.get_value()
        
        @position.setter
        def position(self, position: int):
            '''Establece la posición de la válvula.

            Args:
                position (int): Posición deseada de la válvula.
            '''
            position = int(position)
            if 100 >= position >= 0:
                self._command_node.set_value(OPC_Manager.valor_float(position))
            
            elif position > 100:
                self._command_node.set_value(OPC_Manager.valor_float(100))

            elif position < 0:
                self._command_node.set_value(OPC_Manager.valor_float(0))
            
            else:
                print("Error: value out of limits.")

        @property
        def changing(self):
            '''Verifica si la válvula está cambiando de posición.

            Returns:
                bool: Verdadero si la válvula está cambiando de posición, falso en caso contrario.
            '''
            if int(self._state_node.get_value()) == int(self._command_node.get_value()):
                return True
            return False

    class Deposito():
        '''Clase que permite obtener el nivel de un depósito.

        Args:
            nodo_nivel (Node): Nodo OPC UA que controla el nivel del depósito.
        '''

        def __init__(self, nodo_nivel: Node):
            '''Inicializa el depósito con el nodo de nivel.'''
            self._nivel_node = nodo_nivel

        @property
        def nivel(self):
            '''Obtiene el nivel del depósito.

            Returns:
                float: Nivel actual del depósito.
            '''
            nivel_original = self._nivel_node.get_value()
            nivel_ajustado = ((nivel_original - 2000) / 60) if nivel_original >= 2000 else 0
            nivel_ajustado = min(max(nivel_ajustado, 0), 100)  
            return nivel_ajustado

    class Caudalimetro():
        '''Clase que permite obtener el caudal de un caudalímetro.

        Args:
            nodo_caudal (Node): Nodo OPC UA que controla el caudal del caudalímetro.
        '''

        def __init__(self, nodo_caudal: Node):
            '''Inicializa el caudalímetro con el nodo de caudal.'''
            self._caudal_node = nodo_caudal

        @property
        def caudal(self):
            '''Obtiene el caudal del caudalímetro.

            Returns:
                float: Caudal actual del caudalímetro.
            '''
            return self._caudal_node.get_value()

    class OPC_Manager():
        '''Clase que permite gestionar la comunicación OPC UA con un servidor.

        Args:
            opc_server_address (str): Dirección del servidor OPC UA.
        '''

        _instance = None

        def __new__(cls, *args, **kwargs):
            '''Crea una nueva instancia de OPC_Manager si no existe ninguna.'''
            if cls._instance is None:
                cls._instance = super().__new__(cls, *args, **kwargs)
            return cls._instance
        
        def __init__(self, opc_server_address = "opc.tcp://192.168.0.10:49320"):
            '''Inicializa la comunicación OPC UA con el servidor.'''
            self._client = Client(opc_server_address)
            self._client.connect()

            root_node = self._client.get_root_node()
            plc1_objects = root_node.get_child(["0:Objects"]).get_child(["2:CITEEC"]).get_child(["2:PLC1"])
            plc3_objects = root_node.get_child(["0:Objects"]).get_child(["2:CITEEC"]).get_child(["2:PLC3"])
            
            self.bomba1 = plc1_objects.get_child(["2:Bombas_DB"]).get_child(["2:Bomba_B-B001"]).get_child(["2:CMD_ON"])
            self.bomba2 = plc1_objects.get_child(["2:Bombas_DB"]).get_child(["2:Bomba_B-B002"]).get_child(["2:CMD_ON"])

            self.fvb001 = plc1_objects.get_child(["2:Válvulas_DB"]).get_child(["2:Válvula_B-FV001"]).get_child(["2:OPpositionSP"])
            self.fvb002 = plc1_objects.get_child(["2:Válvulas_DB"]).get_child(["2:Válvula_B-FV002"]).get_child(["2:OPpositionSP"])
            self.fvc003 = plc3_objects.get_child(["2:Válvulas_DB"]).get_child(["2:Válvula_C-FV003"]).get_child(["2:OPpositionSP"])
            self.fvc002 = plc3_objects.get_child(["2:Válvulas_DB"]).get_child(["2:Válvula_C-FV002"]).get_child(["2:OPpositionSP"])

            self.ftc002 = plc3_objects.get_child(["2:Estados_DB"]).get_child(["2:Caudal_CFT002"])

            self.ltc001 = plc3_objects.get_child(["2:C-LT001_Nivel_Depósito_Cabecera"])

        def disconnect(self):
            '''Desconecta la comunicación OPC UA con el servidor.'''
            self._client.disconnect()

        @staticmethod
        def valor_float(valor):
            '''Convierte un valor a float para OPC UA.

            Args:
                valor (float): Valor a convertir.

            Returns:
                DataValue: Valor convertido a float para OPC UA.
            '''
            return ua.DataValue(ua.Variant(valor, ua.VariantType.Float))
        
        @staticmethod
        def valor_int(valor):
            '''Convierte un valor a int para OPC UA.

            Args:
                valor (int): Valor a convertir.

            Returns:
                DataValue: Valor convertido a int para OPC UA.
            '''
            return ua.DataValue(ua.Variant(valor, ua.VariantType.UInt16))
        
        @staticmethod
        def valor_bool(valor):
            '''Convierte un valor a bool para OPC UA.

            Args:
                valor (bool): Valor a convertir.

            Returns:
                DataValue: Valor convertido a bool para OPC UA.
            '''
            return ua.DataValue(ua.Variant(valor, ua.VariantType.Boolean))

    opc_manager_control = OPC_Manager()

    valvula_entrada = ValvulaProporcional(opc_manager_control.fvb001, opc_manager_control.fvb001)
    valvula_recirculacion = ValvulaProporcional(opc_manager_control.fvb002, opc_manager_control.fvb002)
    valvula_salida_dep = ValvulaProporcional(opc_manager_control.fvc003, opc_manager_control.fvc003)
    valvula_grandes = ValvulaProporcional(opc_manager_control.fvc002, opc_manager_control.fvc002)
    bomba1 = BombaHidraulica(opc_manager_control.bomba1)
    bomba2 = BombaHidraulica(opc_manager_control.bomba2)
    deposito = Deposito(opc_manager_control.ltc001)
    caudalimetro_grandes = Caudalimetro(opc_manager_control.ftc002)

elif modulo_importador == "laboratorio.py":

    class BombaHidraulica():
        '''Clase que permite comandar una bomba hidráulica equipada con un variador de frecuencia.

        Args:
            nodo_encendido (Node): Nodo OPC UA que controla el encendido de la bomba.
        '''


        def __init__(self, nodo_variador: Node, nodo_encendido: Node):
            self._variator_node = nodo_variador
            self._power_node = nodo_encendido

        @property
        def power(self):
            return self._power_node.get_value()
        
        @power.setter
        def power(self, power: bool):
            
            self._power_node.set_value(OPC_Manager.valor_bool(power))


        @property
        def speed(self):
            return self._variator_node.get_value()
        
        @speed.setter
        def speed(self, speed: float):

            if 100 >= speed >= 0:
                self._variator_node.set_value(OPC_Manager.valor_int(int(speed*100)))
            
            elif speed > 100:
                self._variator_node.set_value(OPC_Manager.valor_int(10000))

            elif speed < 0:
                self._variator_node.set_value(OPC_Manager.valor_int(0))
            
            else:
                print("Error: value out of limits.") 

    class ValvulaProporcional():

        def __init__(self, nodo_comando: Node):
            self._command_node = nodo_comando

        @property
        def position(self):
            return self._state_node.get_value()
        
        @position.setter
        def position(self, position: int):
            position = int(position)
            if 100 >= position >= 0:
                self._command_node.set_value(OPC_Manager.valor_int(position))
            
            elif position > 100:
                self._command_node.set_value(OPC_Manager.valor_int(100))

            elif position < 0:
                self._command_node.set_value(OPC_Manager.valor_int(0))
            
            else:
                print("Error: value out of limits.")

    class Deposito():

        def __init__(self, nodo_nivel: Node):
            self._nivel_node = nodo_nivel

        @property
        def nivel(self):
            return self._nivel_node.get_value()
    
    class OPC_Manager():

        _instance = None

        def __new__(cls, *args, **kwargs):
            if cls._instance is None:
                cls._instance = super().__new__(cls, *args, **kwargs)
            return cls._instance
        

        def __init__(self, opc_server_address = "opc.tcp://localhost:49320"):
            self._client = Client(opc_server_address)
            self._client.connect()

            root_node = self._client.get_root_node()
            plc_objects = root_node.get_child(["0:Objects"]).get_child(["2:MODBUS"]).get_child(["2:PLC"])

            self.nivel = plc_objects.get_child(["2:MATLAB_DEP3_NIVEL"])
            self.valv_21 = plc_objects.get_child(["2:MATLAB_FV21"])
            self.valv_22 = plc_objects.get_child(["2:MATLAB_FV22"])
            self.valv_21_estado = plc_objects.get_child(["2:SCD_Estado_FV21"])
            self.valv_22_estado = plc_objects.get_child(["2:SCD_Estado_FV22"])
            self.variador = plc_objects.get_child(["2:MATLAB_VELOCIDAD_VARIADOR"])
            self.power_bomba = plc_objects.get_child(["2:SCD_Marcha_Bomba"])



        def disconnect(self):
            self._client.disconnect()

        @staticmethod
        def valor_float(valor):
            return ua.DataValue(ua.Variant(valor, ua.VariantType.Float))
        
        @staticmethod
        def valor_int(valor):
            return ua.DataValue(ua.Variant(valor, ua.VariantType.UInt16))
        
        @staticmethod
        def valor_bool(valor):
            return ua.DataValue(ua.Variant(valor, ua.VariantType.Boolean))

    opc_manager_control = OPC_Manager()
    discharge_valve = ValvulaProporcional(opc_manager_control.valv_21, opc_manager_control.valv_21_estado)
    bomba = BombaHidraulica(opc_manager_control.variador, opc_manager_control.power_bomba)
    deposito = Deposito(opc_manager_control.nivel)


