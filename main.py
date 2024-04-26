import sys
import random
from functools import partial
from sudoku import Sudoku
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6 import QtWidgets, QtCore
from main_window import Ui_MainWindow


flag = 0

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setStyleSheet("background-color: rgb(85, 255, 255)")
        self.ui.btn_dark_light_mode.setStyleSheet("background-color: #192a32; font-size:11pt; color:'#ffffff'")
        self.ui.btn_dark_light_mode.clicked.connect(partial(self.dark_light_mode))
        self.ui.menu_new.triggered.connect(self.new_game)
        self.ui.menu_open_file.triggered.connect(self.open_file)
        self.ui.menu_puzzle_answer.triggered.connect(self.solve)
        self.ui.menu_help.triggered.connect(self.help)
        self.ui.menu_about.triggered.connect(self.about)
        self.ui.menu_exit.triggered.connect(self.exit)
        self.line_edits = [[None for i in range(9)] for j in range(9)]
        self.new_game()
    
    def new_game(self):
        
        self.puzzle = Sudoku(3, seed=random.randint(1, 1000)).difficulty(0.5)
        self.show_game()
        solve = self.puzzle.solve()

    def show_game(self):
        global cells
        global new_cell
        global puzzle_board
        cells = []
        
        for i in range(9):
            for j in range(9):
            
                new_cell = QLineEdit()
                self.appearance(new_cell, "correct_light")
                
                if self.puzzle.board[i][j] != None:
                    new_cell.setText(str(self.puzzle.board[i][j]))
                    new_cell.setReadOnly(True)
                self.ui.grid_layout.addWidget(new_cell, i, j)
                
                new_cell.textChanged.connect(partial(self.validation, i, j))
                self.line_edits[i][j] = new_cell
                cells.append(new_cell)
           
    def appearance(self, cell, status):
        cell.setAlignment(QtCore.Qt.AlignCenter)
        for ii in range(9):
            for jj in range(9):
                if (ii in [0, 1, 2] and jj in [3, 4, 5]) or (ii in [3, 4, 5] and jj in [0, 1, 2]) or (ii in [3, 4, 5] and jj in [6, 7, 8]) or (ii in [6, 7, 8] and jj in [3, 4, 5]):
                    if status == "correct_light":
                        cell.setStyleSheet("background-color: #ffffff; height:50px;font-family:'Segoe UI Black'; font-size:20pt;")
                    elif status == "incorrect_light":
                        cell.setStyleSheet("background-color: #ff909b; height:50px;font-family:'Segoe UI Black'; font-size:20pt;")
                    elif status == "correct_dark":
                        cell.setStyleSheet("background-color: #25404d; height:50px;font-family:'Segoe UI Black'; font-size:20pt; color:'#f2b137'")
        
    def dark_light_mode(self):
        global flag
        if flag %2 == 0:
            self.ui.btn_dark_light_mode.setStyleSheet("background-color: #ffffff; font-size:10pt; color:'black'")
            self.ui.btn_dark_light_mode.setText("Light Mood")
            self.setStyleSheet("background-color: rgb(85, 255, 255)")
            for cell in cells:
                self.appearance(cell, "correct_dark")
            flag += 1
        elif flag %2 != 0:
            self.ui.btn_dark_light_mode.setStyleSheet("background-color: #192a32; font-size:10pt; color:'#ffffff'")
            self.ui.btn_dark_light_mode.setText("Dark Mood")
            self.setStyleSheet("background-color: rgb(85, 255, 255)")
            for cell in cells:
                self.appearance(cell, "correct_light")
            flag += 1

    def open_file(self):
        try:
            file_path = QFileDialog.getOpenFileName(self, "Open file...")[0]
            f = open(file_path, "r")
            big_text = f.read()
            rows = big_text.split("\n")
            puzzle_board = [[None for i in range(9)] for j in range(9)]
            for i in range(len(rows)):
                cells = rows[i].split(" ")
                for j in range(len(cells)):
                    puzzle_board[i][j] = int(cells[j])

            for i in range(9):
                for j in range(9):
                    new_cell = QLineEdit()
                    self.appearance(new_cell, "correct_light")
                    if puzzle_board[i][j] != 0:
                        new_cell.setText(str(puzzle_board[i][j]))
                        new_cell.setReadOnly(True)
                    self.ui.grid_layout.addWidget(new_cell, i, j)
                    new_cell.textChanged.connect(partial(self.validation, i, j))
                    self.line_edits[i][j] = new_cell
        except:
            msg = QMessageBox()
            msg.setText('❌ An error occurred! ❌')
            msg.exec()

    def check(self, i, j, text):
        for i1 in range(0, 9):
            for j1 in range(0, 9):
                num = self.line_edits[i1][j1].text()
                if num == text and i == i1 and j != j1:
                    self.line_edits[i][j].setStyleSheet("background-color: #ff909b; height:50px;font-family:'Segoe UI Black'; font-size:20pt;")
        
        for i2 in range(0, 9):
            for j2 in range(0, 9):
                num = self.line_edits[i2][j2].text()
                if num == text and i != i2 and j == j2:
                    self.line_edits[i][j].setStyleSheet("background-color: #ff909b; height:50px;font-family:'Segoe UI Black'; font-size:20pt;")   

        if 0 <= i < 3 and 0 <= j < 3 :
            for i3 in range(0, 3):
                for j3 in range(0, 3):
                    num = self.line_edits[i3][j3].text()
                    if num == text and i != i3 and j != j3:
                        self.line_edits[i][j].setStyleSheet("background-color: #ff909b; height:50px;font-family:'Segoe UI Black'; font-size:20pt;")   

        if 0 <= i < 3 and 3 <= j < 6 :
            for i4 in range(0, 3):
                for j4 in range(3, 6):
                    num = self.line_edits[i4][j4].text()
                    if num == text and i != i4 and j != j4:
                        self.line_edits[i][j].setStyleSheet("background-color: #ff909b; height:50px;font-family:'Segoe UI Black'; font-size:20pt;")   

        if 0 <= i < 3 and 6 <= j < 9 :
            for i5 in range(0, 3):
                for j5 in range(6, 9):
                    num = self.line_edits[i5][j5].text()
                    if num == text and i != i5 and j != j5:
                        self.line_edits[i][j].setStyleSheet("background-color: #ff909b; height:50px;font-family:'Segoe UI Black'; font-size:20pt;")   

        if 3 <= i < 6 and 0 <= j < 3 :
            for i6 in range(3, 6):
                for j6 in range(0, 3):
                    num = self.line_edits[i6][j6].text()
                    if num == text and i != i6 and j != j6:
                        self.line_edits[i][j].setStyleSheet("background-color: #ff909b; height:50px;font-family:'Segoe UI Black'; font-size:20pt;")   

        if 3 <= i < 6 and 3 <= j < 6 :
            for i7 in range(3, 6):
                for j7 in range(3, 6):
                    num = self.line_edits[i7][j7].text()
                    if num == text and i != i7 and j != j7:
                        self.line_edits[i][j].setStyleSheet("background-color: #ff909b; height:50px;font-family:'Segoe UI Black'; font-size:20pt;")   

        if 3 <= i < 6 and 6 <= j < 9 :
            for i8 in range(3, 6):
                for j8 in range(6, 9):
                    num = self.line_edits[i8][j8].text()
                    if num == text and i != i8 and j != j8:
                        self.line_edits[i][j].setStyleSheet("background-color: #ff909b; height:50px;font-family:'Segoe UI Black'; font-size:20pt;")        

        if 6 <= i < 9 and 0 <= j < 3 :
            for i9 in range(6, 9):
                for j9 in range(0, 3):
                    num = self.line_edits[i9][j9].text()
                    if num == text and i != i9 and j != j9:
                        self.line_edits[i][j].setStyleSheet("background-color: #ff909b; height:50px;font-family:'Segoe UI Black'; font-size:20pt;")   

        if 6 <= i < 9 and 3 <= j < 6 :
            for i10 in range(6, 9):
                for j10 in range(3, 6):
                    num = self.line_edits[i10][j10].text()
                    if num == text and i != i10 and j != j10:
                        self.line_edits[i][j].setStyleSheet("background-color: #ff909b; height:50px;font-family:'Segoe UI Black'; font-size:20pt;")   

        if 6 <= i < 9 and 6 <= j < 9 :
            for i11 in range(6, 9):
                for j11 in range(6, 9):
                    num = self.line_edits[i11][j11].text()
                    if num == text and i != i11 and j != j11:
                        self.line_edits[i][j].setStyleSheet("background-color: #ff909b; height:50px;font-family:'Segoe UI Black'; font-size:20pt;")                         

    def win_check(self):
        play_board = [[None for i in range(9)] for j in range(9)]
        answer_board = [[None for i in range(9)] for j in range(9)]
        solve = self.puzzle.solve()
        for ii in range(9):
            for jj in range(9):
                play_board[ii][jj] = self.line_edits[ii][jj].text()
                answer_board[ii][jj] = str(solve.board[ii][jj])

        if play_board == answer_board:
           msg_box=QMessageBox()
           msg_box.setText("🎉 Congragulation !🎉  😍 You Win ! ✅ ")
           msg_box.exec()
                  

    def solve(self):
        solve = self.puzzle.solve()
        print(solve.board)
        self.puzzle = Sudoku(3, 3, board=solve.board)
        msg_box=QMessageBox()
        msg_box.setText(" 🫡 The Sudoku Game is Solved ! ✅")
        self.show_game()
        msg_box.exec()

    def validation(self, i, j, text):
        if text not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            self.line_edits[i][j].setText("")

        self.check(i, j, text)
        self.win_check()

    def help(self):
        QMessageBox.information(self, "Help", 'How to play sudoku:\n  A 9×9 square must be filled in with numbers from 1-9 \n with no repeated numbers in each line, horizontally or vertically. \n To challenge you more, there are 3×3 squares marked out in the grid,\n and each of these squares can not have any repeat numbers either')

    def about(self):
        QMessageBox.information(self, "About", "This is a Sudoku game. Fill the board with numbers 1-9 such that each row, column, and 3x3 subgrid contains all of the digits 1-9.")


    def close(self):
        exit(0)

    def exit(self):
        exit(0)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    
    app.exec()