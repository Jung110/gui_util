import sys
import os

import pandas as pd
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon

class PathToExcelApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.df=0
    def initUI(self):
        #Set widget
        ## 저장 버튼
        exportbtn = QPushButton('저장', self)
        exportbtn.clicked.connect(self.exportBtnClicked)
        ## 실행 버튼
        getBtn = QPushButton('실행' , self)
        getBtn.clicked.connect(self.getFileNameAndPwd)
        ## 경로 재설정 버튼
        setPathbtn = QPushButton('경로 재설정', self)
        setPathbtn.clicked.connect(self.setPathbtnClicked)
        ## 경로 보여주는 Line Edit
        self.dirName = os.getcwd()
        self.pathLine = QLineEdit()
        self.pathLine.setReadOnly(True)
        self.setPathbtnClicked()

        ## 실행 후 결과를 보여주는 TextEdit
        self.resultBox = QTextEdit("""
        사용할 경로 선택 후 에 실행 버튼을 누르면 해당 경로에 있는 파일명 , 경로 출력됨 
        
        """)
        self.resultBox.setMinimumHeight(500)
        self.resultBox.setReadOnly(True)



        # Set Layout
        ## horizon Layout
        buttonbox = QHBoxLayout()
        buttonbox.addStretch(3)
        buttonbox.addWidget(getBtn)
        buttonbox.addStretch(1)
        buttonbox.addWidget(exportbtn)
        buttonbox.addStretch(1)
        buttonbox.addWidget(setPathbtn)
        buttonbox.addStretch(3)
        ## vertical Layout
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.resultBox)
        vbox.addStretch(1)
        vbox.addWidget(self.pathLine)
        vbox.addLayout(buttonbox)
        vbox.addStretch(1)

        ## set Etc
        self.setLayout(vbox)
        self.setWindowTitle('PathToCSV')
        self.setWindowIcon(QIcon('vote.png'))
        self.resize(700, 600)
        self.show()

    # 저장 버튼이 눌렸을 때
    def exportBtnClicked(self):
        if type(self.df) ==int:
            dlg = QMessageBox.critical(
                self,
                "오류",
                "실행 부터 눌러라",
                buttons=QMessageBox.StandardButton.Yes
            )
        else:
            self.df.to_csv("./result.csv",index=False)


    # 경로 지정 버튼이 눌렸을 떄
    def setPathbtnClicked(self):
        tmp = QFileDialog.getExistingDirectory(self, 'set dir', self.dirName)
        if tmp!="":
            self.dirName = tmp
            self.pathLine.setText(self.dirName)

    # 실행 버튼이 눌렸을 때
    def getFileNameAndPwd(self):
        fn_list = []
        fd_list = []
        self.resultBox.clear()
        for (root, dirs, files) in os.walk(self.pathLine.text()):
            if len(files) > 0:
                for file_name in files:
                    self.resultBox.append(f"경로:{root}\n 파일 이름:{file_name}\n")
                    fn_list.append(file_name)
                    fd_list.append(root)
        self.df = pd.DataFrame()
        self.df['name'] = fn_list
        self.df['dir'] = fd_list


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = PathToExcelApp()
   sys.exit(app.exec())