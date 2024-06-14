from PyQt5.QtWidgets import (QApplication, QWidget, 
QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QHBoxLayout, QVBoxLayout,QInputDialog)

import json

app = QApplication([])


notes_win = QWidget()
notes_win.setWindowTitle('Smart Notes')
notes_win.resize(900, 600)



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
notes_win.setLayout(layout_notes)


def add_note():
    note_name, ok = QInputDialog.getText(notes_win, "Add note", "Note name: ")
    if ok and note_name != "":
        notes_data[note_name] = {"text" : "", "tags" : []}
        list_notes.addItem(note_name)
        list_tags.addItems(notes_data[note_name]["tags"]) 
        print(notes_data)

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes_data[key]["text"] = field_text.toPlainText()
        with open("notes_data.json", "w") as file:
            json.dump(notes_data, file, sort_keys=True, ensure_ascii=False)
        print(notes_data)
    else:
        print("Note to save is not selected!")

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes_data[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes_data)
        with open("notes_data.json", "w") as file:
            json.dump(notes_data, file, sort_keys=True, ensure_ascii=False)
        print(notes_data)
    else:
        print("Note to delete is not selected!")

def show_note():
    '''' '''
    key = list_notes.selectedItems()[0].text()
    field_text.setText(notes_data[key]["text"])
    list_tags.clear()
    list_tags.addItems(notes_data[key]["tags"])

def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes_data[key]["tags"]:
            notes_data[key]["tags"].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
        with open("notes_data.json", "w") as file:
            json.dump(notes_data, file, sort_keys=True, ensure_ascii=False)
        print(notes_data)
    else:
        print("Note to add a tag is not selected!")

def del_tag():
    if list_tags.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes_data[key]["tags"].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes_data[key]["tags"])
        with open("notes_data.json", "w") as file:
            json.dump(notes_data, file, sort_keys=True, ensure_ascii=False)
    else:
        print("Tag to delete is not selected!")

def search_tag():
    print(button_search.text())
    tag = field_tag.text()
    if button_search.text() == "Search notes by tag" and tag:
        print(tag)
        notes_filtered = {}
        for note in notes_data:
            if tag in notes_data[note]["tags"]: 
                notes_filtered[note]=notes_data[note]
        button_search.setText("Reset search")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
        print(button_search.text())
    elif button_search.text() == "Reset search":
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_data)
        button_search.setText("Search notes by tag")
        print(button_search.text())
    else:
        pass

#connecting event handling
list_notes.itemClicked.connect(show_note)

button_note_create.clicked.connect(add_note)
button_note_save.clicked.connect(save_note)
button_note_del.clicked.connect(del_note)

button_add.clicked.connect(add_tag)
button_del.clicked.connect(del_tag)
button_search.clicked.connect(search_tag)

notes_win.show()

with open("notes_data.json", "r") as file:
    notes_data = json.load(file)

list_notes.addItems(notes_data)

app.exec_()