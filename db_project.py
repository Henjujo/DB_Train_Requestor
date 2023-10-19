'''Simple application that fetches DB data and presents requested train data in a nice window'''

import tkinter as tk
import sys
from tkinter import ttk, StringVar, Entry, Frame
from deutsche_bahn_api import api_authentication as auth, station_helper, timetable_helper, train
import tkscrolledframe

def traintostring(zug: train.Train):
    '''Converts train information into displayable string'''
    try:
        linie = zug.train_line
    except AttributeError:
        linie = "NaN"
    try:
        arrival = zug.arrival
    except AttributeError: #Train doesnt arrive????
        arrival = "NaN"
    try:
        departure = zug.departure
    except AttributeError:
        departure = "NaN"
    try:
        traintype = zug.train_type
    except AttributeError:
        traintype = "NaN"
    try:
        train_number = zug.train_number
    except AttributeError:
        train_number = "NaN"
    try:
        stations = zug.stations
    except AttributeError:
        stations = "NaN"
    try:
        platform = zug.platform
    except AttributeError:
        platform = "NaN"
    try:
        trip_type = zug.trip_type
    except AttributeError:
        trip_type = "NaN"

    return "Zug-ID: " + train_number + ", Zugtyp: " + traintype + ", Ankunft: " + arrival + ", Abfahrt: " + departure + ", Linie: " + linie + ", Stationen: " + stations + ", Gleis: " + platform + ", Fahrt: " + trip_type

API_KEY_1 = "" #Insert key #1 here
API_KEY_2 = "" #Insert key #2 here

def frame_call():
    '''Basically the main method'''
    api = auth.ApiAuthentication(API_KEY_1, API_KEY_2)
    try:
        assert api.test_credentials() is True
    except AssertionError:
        print("API Key is not correct! Please update.")
        sys.exit()

    ### BACKEND-PART ###

    stationhelper = station_helper.StationHelper()
    stationhelper.load_stations()

    ### TKINTER PART ###

    root = tk.Tk()
    root.title('DB Application')
    root.geometry('720x540')
    off_label = ttk.Label(root, text="DB Applikation")
    off_label.grid(column=0, row=0)
    fill_label = ttk.Label(root, text=" ")
    fill_label.grid(column=0, row=1)

    # Get station
    combobox = ttk.Combobox(root)
    def station_method(string: str):
        liste = stationhelper.find_stations_by_name(string.title())
        my_list = []
        for entry in liste:
            my_list.append(entry.NAME)
        combobox['values'] = tuple(my_list)
        combobox.grid(column=0, row=5)

    station_label = ttk.Label(root, text="Gesuchte Station: ")
    station_label.grid(column=0, row=2)

    stringvar1 = StringVar()
    station_field = Entry(root, textvariable=stringvar1)
    station_field.grid(column=0, row=3)

    station_button = ttk.Button(root, name="stationen finden",
                                command=lambda: station_method(station_field.get()))
    station_button.grid(column=0, row=4)

    filler_label = ttk.Label(root, text="   ")
    filler_label.grid(column=1, row=0)

    # Then get time tables

    def time_method(string, time = None):
        station = stationhelper.find_stations_by_name(string)[0]
        timetablehelper = timetable_helper.TimetableHelper(station, api)
        my_string = ""
        for entry in timetablehelper.get_timetable(time):
            my_string += traintostring(entry) + '\n'
        root_2 = tk.Tk()
        root_2.resizable(True, True)
        scrolledframe = tkscrolledframe.ScrolledFrame(root_2, width=640, height=480)
        scrolledframe.pack(side="top", expand=1, fill="both")
        inner_frame = scrolledframe.display_widget(Frame)
        label = ttk.Label(inner_frame, text=my_string)
        #label.grid(row=0, column=0)
        label.pack(side="top", expand=1, fill="none")

        root_2.mainloop()

    time_label = ttk.Label(root, text="Gewuenschte Stunde (leer = aktuelle Stunde; Input < 23): ")
    time_label.grid(column=2, row=2)

    stringvar2 = StringVar()
    time_field = Entry(root, textvariable=stringvar2)
    time_field.grid(column=2, row=3)

    time_button = ttk.Button(root, name="fahrplan finden",
                             command=lambda: time_method(combobox.get(), time_field.get()))
    time_button.grid(column=2, row=4)

    root.mainloop()

if __name__ == '__main__':
    frame_call()
