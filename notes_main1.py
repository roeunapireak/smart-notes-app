1#start to create smart notes app

from PyQt5.QtWidgets import (QApplication, QWidget, 
QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QHBoxLayout, QVBoxLayout)

import json

app = QApplication([])

'''Notes in json'''
notes_data = {
    "Algorithmics" : {
        "text" : "This is top school in Cambodia.",
        "tags" : ["learn", "study", "programming"]
    },
    "Wing Bank" : {
        "text" : "This is top company in Cambodia",
        "tags" : ["money", "transfer"]
    },
    "ABA Bank" : {
        "text" : "This is top digital Bank in Cambodia",
        "tags" : ["e-money", "digital", "finance"]
    }
}

with open("notes_data.json", "w") as file:
    json.dump(notes_data, file, ensure_ascii=False) # ascii is text format



notes = QWidget()
notes.setWindowTitle('Smart Notes')
notes.resize(900, 600)



#application window widgets

# list of notes
list_notes = QListWidget()
list_notes_label = QLabel('List of notes')

button_note_create = QPushButton('Create note') 
button_note_save = QPushButton('Save note')
button_note_del = QPushButton('Delete note')


# list of tags
list_tags = QListWidget()
list_tags_label = QLabel('List of tags')

button_add = QPushButton('Add to note')
button_del = QPushButton('Untag from note')
button_search = QPushButton('Search notes by tag')

field_tag = QLineEdit('')
field_tag.setPlaceholderText('Enter tag...')

######################

field_text = QTextEdit()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)

######################

col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)

row_1 = QHBoxLayout()
row_2 = QHBoxLayout()

row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)

row_2.addWidget(button_note_save)

col_2.addLayout(row_1)
col_2.addLayout(row_2)

################

col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)

row_3 = QHBoxLayout()
row_3.addWidget(button_add)
row_3.addWidget(button_del)

row_4 = QHBoxLayout()
row_4.addWidget(button_search)

col_2.addLayout(row_3)
col_2.addLayout(row_4)


layout_notes = QHBoxLayout()
layout_notes.addLayout(col_1, stretch = 2)
layout_notes.addLayout(col_2, stretch = 1)
notes.setLayout(layout_notes)

def show_note():
    '''' '''
    key = list_notes.selectedItems()[0].text()
    field_text.setText(notes_data[key]["text"])
    list_tags.clear()
    list_tags.addItems(notes_data[key]["tags"])

#connecting event handling
list_notes.itemClicked.connect(show_note)

notes.show()

with open("notes_data.json", "r") as file:
    data = json.load(file)

list_notes.addItems(data)

app.exec_()