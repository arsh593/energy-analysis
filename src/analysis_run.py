PRICE = 7

import pandas as pd
from .data_processing import CleanData
from .calculations import Calculate
from .visualization import plot_average_room, plot_summary_on_date, plot_distribution_of_daily
from pathlib import Path

def run_analysis():
    src_dir = Path(__file__).resolve().parent
    output_dir = src_dir.parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    readings = pd.read_csv(src_dir / "readings.csv")
    rooms = pd.read_csv(src_dir / "rooms.csv")
    
    clean = CleanData(readings, rooms)
    cleaned = clean.clean_readings()
    clean.clean_readings_check()
    clean.check_rooms()
    clean.check_unknown_room()
    clean.save_report(output_dir / "report.txt")

    calc = Calculate(cleaned, rooms)
    calc.pd_to_np()
    calc.daily_totals()
    calc.average_time_of_day()
    calc.add_daily_totals()
    calc.merge_result()
    calc.calculate_daily(PRICE)
    calc.save_daily_summary(output_dir / "daily_summary.csv")
    calc.save_room_summary(output_dir / "room_summary.csv")
    df = calc.result
    df_room = calc.room_sum
    df_daily = calc.daily_sum

    plot_average_room(df_room, output_dir / "average_room.png")
    plot_summary_on_date(df_daily, output_dir / "date_summary.png")
    plot_distribution_of_daily(df, output_dir / "result_destribution.png", 1)


