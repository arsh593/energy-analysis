import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

def plot_average_room(df, path):
    fig, ax = plt.subplots(figsize=(9, 5))

    ax.barh(df["room_name"], df["avg_daily_kwh"])

    ax.set_title("Средний суточный расход по помещениям")
    ax.set_ylabel("Назвение помещения")
    ax.set_xlabel("Средний расход, кВт*ч")

    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")

    plt.show()

def plot_summary_on_date(df, path):
    fig, ax = plt.subplots(figsize=(9, 5))

    incomplete = df.loc[df["room_count"] < 4]

    dates = pd.to_datetime(df["date"])
    ax.plot(dates, df["total_kwh"])
    ax.plot(
        dates.loc[incomplete.index],
        incomplete["total_kwh"],
        marker="o",
        linestyle="None",
        color="orange",
        label="Неполные данные",
    )
    ax.legend()

    ax.set_title("Общий расход по датам, с обозначением неполных дней")
    ax.set_xlabel("Дата")
    ax.set_ylabel("Расход, кВт*ч")
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m"))
    ax.tick_params(axis="x", labelrotation=0)

    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")

    plt.show()

def plot_distribution_of_daily(df, path, room_id=1):
    fig, ax = plt.subplots(figsize=(9, 5))
    
    room_mask = df["room_id"] == room_id
    room_name = df.loc[room_mask, "room_name"].iloc[0]
    room_daily_kwh = df.loc[room_mask, "daily_kwh"]    
    
    ax.hist(room_daily_kwh, bins=6, edgecolor="black")
    ax.set_title(f"Выбранная комната: {room_name}")
    ax.set_xlabel("Суточный расход, кВт*ч")
    ax.set_ylabel("Количество дней")

    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")

    plt.show()

