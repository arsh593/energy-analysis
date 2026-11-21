import pandas as pd

readings = pd.read_csv(
    "D:/learning to ML/energy_analysis/tests/data/readings.csv"
)

rooms = pd.read_csv(
    "D:/learning to ML/energy_analysis/tests/data/rooms.csv"
)

class CleanData():
    def __init__(self, readings, rooms):
        self.readings = readings
        self.rooms = rooms
        self.cleaned_readings = None
        self.report = {}

    def clean_readings(self):
        cleaned = self.readings.copy()
        
        entrance = len(self.readings)
        self.report["entrance"] = entrance

        cleaned = cleaned.drop_duplicates()
        
        delete_duplicates = entrance - len(cleaned)
        self.report["delete_duplicates"] = delete_duplicates

        cleaned = cleaned.dropna(subset=["morning_kwh", "day_kwh", "evening_kwh"])
        
        delete_nans = entrance - len(cleaned) - delete_duplicates
        self.report["delete_nans"] = delete_nans
        
        mask = ~((cleaned["morning_kwh"] < 0)
                | (cleaned["day_kwh"] < 0)
                | (cleaned["evening_kwh"] < 0)
        )
        
        cleaned = cleaned.loc[mask]

        self.report["negative_values"] = entrance - len(cleaned) - delete_nans - delete_duplicates
        self.report["remained"] = len(cleaned)

        self.cleaned_readings = cleaned
        return self.cleaned_readings

    def clean_readings_check(self):
        clean = self.clean_readings()
        conflict_mask = clean.duplicated(subset=["date", "room_id"], keep=False)

        if conflict_mask.any():
            conflict = clean.loc[conflict_mask].iloc[0]
            raise ValueError(
                f"Разные показания за {conflict["date"]} "
                f"для комнаты {conflict["room_id"]}"
            )
    
    def check_rooms(self):
        conflict_mask = self.rooms.duplicated(subset=["room_id"])
        if conflict_mask.any():
            raise ValueError(
                f"В справочнике помещений на один ID приходится больше одной строки"
            )

    def check_unknown_room(self):
        mask = ~self.cleaned_readings["room_id"].isin(self.rooms["room_id"])
        unknown = self.cleaned_readings.loc[mask, "room_id"]
        if mask.any():
            raise ValueError(
                f"Обнаружены неизвестный(ые) ID в readings: {unknown.tolist()}"
            )
    
    def save_report(self):
        with open("report.txt", "w", encoding="utf-8") as file:
            file.write("Поступило строк: " + str(self.report["entrance"]) + "\n")
            file.write("Удалено дубликатов: " + str(self.report["delete_duplicates"]) + "\n")
            file.write("Удалено строк где нету показаний: " + str(self.report["delete_nans"]) + "\n")
            file.write("Удалено строк где показания отрицательные: " + str(self.report["negative_values"]) + "\n")
            file.write("Осталось строк: " + str(self.report["remained"]))
        

try:
    data = CleanData(readings, rooms)
    data.clean_readings()
    data.save_report()
    print(data.report)
except ValueError as error:
    print(error)

