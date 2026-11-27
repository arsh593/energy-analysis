import numpy as np
import pandas as pd


class Calculate():
    def __init__(self, cleaned, rooms):
        self.cleaned = cleaned
        self.rooms = rooms        
        self.ar_cleaned = None
        self.daily_cons = None
        self.average = None
        self.interim = None
        self.result = None
        self.room_sum = None
        self.daily_sum = None

    def pd_to_np(self):
        columns = ["morning_kwh", "day_kwh", "evening_kwh"]
        self.ar_cleaned = self.cleaned[columns].to_numpy()
        
        return self.ar_cleaned

    def daily_totals(self):
        self.daily_cons = self.ar_cleaned.sum(axis=1)
        return self.daily_cons

    def average_time_of_day(self):
        self.average = self.ar_cleaned.mean(axis=0)
        return self.average

    def add_daily_totals(self):
        total = self.cleaned.copy()
        total["daily_kwh"] = self.daily_cons
        self.interim = total
        
        return self.interim

    def merge_result(self):
        result = self.interim.merge(
            self.rooms,
            on="room_id",
            how="left",
            validate="many_to_one"
        )
        self.result = result
        
        return self.result

    def calculate_daily(self, price):
        self.result["daily_price"] = self.result["daily_kwh"] * price
        self.result["ratio"] = (self.result["daily_kwh"] / self.result["daily_limit_kwh"]) * 100
        self.result["status"] = "high"
        self.result["status"] = self.result["status"].where(
            self.result["ratio"] > 120,
            "normal"
        )

        return self.result

    def save_daily_summary(self, path):

        daily_sum = self.result.groupby("date", as_index=False).agg(
            total_kwh=("daily_kwh", "sum"),
            total_price=("daily_price", "sum"),
            room_count=("room_id", "count")
        )

        columns = ["date", "total_kwh", "total_price", "room_count"]
        daily_sum = daily_sum[columns]
        daily_sum.to_csv(path, index=False)
        self.daily_sum = daily_sum

    def save_room_summary(self, path): 
        room_sum = self.result.groupby(["room_id","room_name"], as_index=False).agg(
            valid_days=("date", "count"),
            total_kwh=("daily_kwh", "sum"),
            total_cost=("daily_price", "sum"),
            avg_daily_kwh=("daily_kwh", "mean"),
            high_days=("status", self.count_high),
            high_days_pct=("status", self.percentages_high)
        )
        columns = ["room_id", "room_name", "valid_days", "total_kwh", "avg_daily_kwh", "total_cost", "high_days", "high_days_pct"]
        room_sum = room_sum[columns]
        room_sum.to_csv(path, index=False)
        self.room_sum = room_sum

    @staticmethod    
    def count_high(x):
        mask_high = x == "high"
        return mask_high.sum()

    @staticmethod
    def percentages_high(x):
        sum_high = (x == "high").sum()
        return sum_high / len(x) * 100
        








    




