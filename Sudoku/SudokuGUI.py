from Sudoku import *
from main import *
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty, NumericProperty
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.button import Button


class SudokuTablero(GridLayout):
    '''
    El tablero, el conjunto de casillas
    '''

    def __init__(self, **kwargs):
        super(SudokuTablero, self).__init__(**kwargs)
        self.cargarBoard(board)

    def cargarBoard(self, bo):
        '''
        Es la funcion principal, sin esta el talbero jamas apareceria en pantalla
        :param bo: Tablero
        :return: None
        '''
        app = SudokuApp()
        for i in range(len(bo)):
            for j in range(len(bo[0])):
                if bo[i][j] == 0:
                    cuadradito = SudokuCelda()
                    self.add_widget(cuadradito)
                    app.text_inputs.append(cuadradito)
                else:
                    cuadradito = TextInput(
                        text=str(bo[i][j]), multiline=False, halign="left", readonly=True,
                        focus=False, allow_copy=False, font_size=25,
                    )
                    self.add_widget(cuadradito)
                    app.text_inputs.append(cuadradito)


class Timer(Label):
    '''
    El reloj de abajo
    '''
    seg = NumericProperty()
    min = NumericProperty()
    stop = True

    def aumentar_tiempo(self, interval):
        '''
        Se encarga de aumentar el tiempo del reloj
        por cada segundo que pasa
        :param interval: 1 seg
        :return:
        '''
        self.seg += 1
        if self.seg == 60:
            self.min += 1
            self.seg = 0

    def restartTimer(self):
        '''
        Reincia el contador
        :return: None
        '''
        self.seg = 0
        self.min = 0
        Clock.unschedule(self.aumentar_tiempo)
        Clock.schedule_interval(self.aumentar_tiempo, 1)

    def resumeTimer(self):
        '''
        Si el reloj esta en pausa, lo reanuda
        :return: None
        '''
        Clock.schedule_interval(self.aumentar_tiempo, 1)

    def stopTimer(self):
        '''
        Pone pausa al reloj
        :return: None
        '''
        if self.stop:
            Clock.unschedule(self.aumentar_tiempo)
            self.stop = False
        else:
            self.resumeTimer()
            self.stop = True


class stopButton(Button):
    '''
    El boton de stop timer y se encarga de cambiar la palabra
    del boton de 'Stop' si esta andando a 'Resume' si esta parado
    y bicecersa
    '''
    def on_release(self):
        if Timer.stop:
            self.text = 'Resume'
            Timer.stop = False
        else:
            self.text = 'Stop'
            Timer.stop = True


class SudokuScreen(FloatLayout, Timer):
    '''
    Es la parte de la User Interface donde estan los botones de abajo
    '''
    def __init__(self, **kwargs):
        super(SudokuScreen, self).__init__(**kwargs)

        Clock.schedule_interval(self.aumentar_tiempo, 1)
        self.aumentar_tiempo(0)

    def solveBoard(self):
        '''
        Resuelve el sudoku actual y te dice donde te equivocaste con colores
        :return: None
        '''
        global bo_copy
        app = SudokuApp()
        solve(bo_copy)
        self.stopTimer()
        for i in range(len(app.text_inputs)):
            if app.text_inputs[i].text == '':
                app.text_inputs[i].background_color = [244/255, 212/255, 96/255, 1]  #amarillo

            elif app.text_inputs[i].text != str(bo_copy[i // 9][i % 9]):
                app.text_inputs[i].background_color = [214/255,69/255,65/255,1]  #rojo
            app.text_inputs[i].text = str(bo_copy[i // 9][i % 9])


    def clearBoard(self):
        '''
        Vacia todas las celdas que el usuario haya puesto un numero.
        Es decir que reinicia el sudoku
        :return: None
        '''
        self.restartTimer()
        app = SudokuApp()
        for i in range(len(app.text_inputs)):
            if board[i//9][i%9] ==0:
                app.text_inputs[i].text = ''
            app.text_inputs[i].background_color = [1, 1, 1, 1]

    @staticmethod
    def check_if_not_yet_complete():
        '''
        Checkea si todabvia no se completo el sudoku, pero mo sabe si este esta resuelto o
        si simplemente esta lleno de numeros al azar
        :return: True si no esta todabvia completo
        '''
        app= SudokuApp
        for i in range(len(app.text_inputs)):
            if app.text_inputs[i].text == '' or app.text_inputs[i].text == '|':

                return True




class buttonPopup(Popup,Timer):
    '''
    Al darle doble click o doble tap a una celda se abre el menu
    que te permite seleccionar el numero para dicha celda
    '''
    button = ObjectProperty()
    def select(self,num):
        '''
        Al hacer click en uno de los botones se encarga de poner dicho
        numero en la celda presionada
        :param num: El num del boton presionado
        :return: None
        '''
        app = SudokuApp()
        pos = app.get_pos()
        if num !=0:
            self.is_valid(pos, num)
            app.text_inputs[pos].text = str(num)

        elif num==0:
            app.text_inputs[pos].background_color = [1,1,1,1]

        app.update(pos)

        if not SudokuScreen.check_if_not_yet_complete():
            completePopup().open()

        app.update(pos)
        self.dismiss()


    def on_dismiss(self):
        '''
        Se encarga de borrar el '|' en caso de que no se desee poner ningun numero
        en la celda
        :return:
        '''
        app = SudokuApp()
        pos = app.get_pos()
        if pos:
            if app.text_inputs[pos].text != str(range(1,10)):
                app.text_inputs[pos].text = ''

    @staticmethod
    def is_valid(pos, num):
        '''
        Si el numero puesto en la celda es incorrecto, esta se volvera de color rojo
        :param pos: posicion en text_inputs[?]
        :param num: Numero puesto en la celda
        :return: None
        '''
        app = SudokuApp
        coords = (pos // 9, pos % 9)
        ok = valid(bo_updated, coords, num)

        if not ok:
            app.text_inputs[pos].background_color = [1, 0, 0, 1]
        else:
            app.text_inputs[pos].background_color = [1, 1, 1, 1]




class completePopup(Popup):
    pass



class SudokuCelda(TextInput):
    '''
    Son las casillas que podes utilizar
    '''
    def on_text_validate(self):
        '''
        Si estas usandolo en PC se ejecuta al darle enter con una casilla
        seleccionada
        :return:
        '''
        if  not SudokuScreen.check_if_not_yet_complete():
            completePopup().open()

    def on_double_tap(self):
        '''
        Se llama cada vez que le des doble tap a una celda
        :return: Abre el popup con los botones del 1 al 9
        '''
        buttonPopup().open()
        self.text = '|'
