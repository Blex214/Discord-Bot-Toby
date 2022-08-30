import pygsheets
import os

def refresh():
    client = pygsheets.authorize()

    sh = client.open('Toby_Commands')
    wks = sh.sheet1

    os.remove('Toby_Commands.csv')
    wks.export(pygsheets.ExportType.csv)
