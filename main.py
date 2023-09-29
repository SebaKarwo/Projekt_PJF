import requests
import sys
from PyQt6 import uic
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import QMainWindow, QApplication, QListView, QPushButton, QTextEdit, QLabel, QWidget
import webbrowser



api_url = 'https://food2fork.ca/api/recipe/search/?query='


headers = {
    'Authorization': 'Token 9c8b06d329136da358c2d00e76946b0111ce2c48'
}

actual_food = 0
data = {}
dishes = []
def get_food_data(ingredients : str):

    url = api_url + ingredients
    response = requests.get(url,headers=headers)

    if response.status_code == 200:
        data = response.json()
        print(data)
        return data
    else:
        print("Błąd podczas komunikacji z API. Kod odpowiedzi:", response.status_code)
        print(response.text)


def food_supplies(items):
    model = QStandardItemModel()
    model.appendRow(QStandardItem(f"nazwa: {items['title']}"))
    model.appendRow(QStandardItem(f"ocena: {items['rating']}"))
    model.appendRow(QStandardItem("skladniki:"))
    for i in items['ingredients']:
        model.appendRow(QStandardItem(i))
    list_View.setModel(model)

def next_food():
    global actual_food
    global dishes
    actual_food = actual_food + 1
    if actual_food > len(dishes)-1:
        actual_food = 0

    background_image_url = dishes[actual_food]['featured_image']
    get_photo(background_image_url)
    change_photo(img2)

    food_supplies(dishes[actual_food])
    autor.setText(dishes[actual_food]['publisher'])
    data_dodania.setText(dishes[actual_food]['date_added'])

def prev_food():
    global actual_food
    global dishes
    actual_food = actual_food - 1
    if actual_food < 0:
        actual_food = len(dishes) - 1

    background_image_url = dishes[actual_food]['featured_image']
    get_photo(background_image_url)
    change_photo(img2)

    food_supplies(dishes[actual_food])
    autor.setText(dishes[actual_food]['publisher'])
    data_dodania.setText(dishes[actual_food]['date_added'])

def get_photo(url):
    response = requests.get(url)

    if response.status_code == 200:
        with open('zdjecie.jpg', 'wb') as file:
            file.write(response.content)
        return True
    else:
        return False

def change_photo(img : QWidget):
    img.setStyleSheet(f"""
        background-image: url('zdjecie.jpg');
        background-position: center; 
        background-repeat: no-repeat; 
        background-attachment: fixed; 
        background-size: cover; 
        """)
def search_button():
    global actual_food
    global dishes

    actual_food = 0
    tekst = items.toPlainText()

    data = get_food_data(tekst)
    dishes = data['results']

    item_count.setText(str(data['count']))
    if data['count']==0:
        return None

    results.setEnabled(True)
    next.setEnabled(True)
    prev.setEnabled(True)


    background_image_url = data['results'][0]['featured_image']
    get_photo(background_image_url)
    change_photo(img2)

    food_supplies(dishes[0])
    autor.setText(dishes[0]['publisher'])
    data_dodania.setText(dishes[0]['date_added'])

def go_link():

    url = dishes[actual_food]['source_url']
    webbrowser.open(url)


app = QApplication(sys.argv)


ui_file = "interface.ui"
window = uic.loadUi(ui_file)


list_View = window.findChild(QListView, "listView")
items = window.findChild(QTextEdit, 'items')

item_count = window.findChild(QLabel, 'item_count')
autor = window.findChild(QLabel, 'autor')
data_dodania = window.findChild(QLabel, 'data_dodania')

results = window.findChild(QWidget, 'results')

img2 = window.findChild(QWidget, 'img2')

link = window.findChild(QPushButton, 'link')
link.clicked.connect(go_link)

search = window.findChild(QPushButton, "search")
search.clicked.connect(search_button)


next = window.findChild(QPushButton, "next")
next.clicked.connect(next_food)

prev = window.findChild(QPushButton, "prev")
prev.clicked.connect(prev_food)

main_window = QMainWindow()
main_window.setCentralWidget(window)

main_window.show()

sys.exit(app.exec())




