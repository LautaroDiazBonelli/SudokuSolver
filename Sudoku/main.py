from kivy.app import App
from kivy.core.window import Window
from SudokuGUI import *


class SudokuApp(App):
    title = 'Sudøku'
    '''
    text_inputs es una lista que contiene a cada una de las celdas de sudoku
    empieza en [0] que es la esquina superior izquierda y termina en [81], la esquina
    inferiror derecha.
    '''
    text_inputs = []

    def build(self):
        return SudokuScreen()

    def get_pos(self):
        '''
        Busca a la celda cuyo texto sea '|'.
        :return: Su posicion
        '''
        for i in range(len(self.text_inputs)):
            if self.text_inputs[i].text == '|':
                self.text_inputs[i].text = ''
                return i

    def update(self, pos):
        '''
        Actualiza el tablero permitiendo
        que el algoritmo vea los números que se van poniendo
        y asi a marcarte errores teniendo en cuenta los números que
        ya pusiste.
        :param pos: positcion
        :return: None
        '''
        if self.text_inputs[pos].text != '' and self.text_inputs[pos].text != '|':
            bo_updated[pos // 9][pos % 9] = int(self.text_inputs[pos].text)


if __name__ == '__main__':
    Window.size = (300, 500)
    SudokuApp().run()
