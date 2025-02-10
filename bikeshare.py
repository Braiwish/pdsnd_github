import pandas as pd
import time

CITY_DATA = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv",
}

MONTHS = ["january", "february", "march", "april", "may", "june"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


def get_filters():
    """Get user input for city, month, and day to analyze."""
    print("Hello! Let's explore some US bikeshare data!")

    while True:
        city = input("Enter city (Chicago, New York City, Washington): ").lower()
        if city in CITY_DATA:
            break
        print("Invalid city. Please try again.")

    while True:
        month = input("Enter month (all, january, february, ..., june): ").lower()
        if month in ["all"] + MONTHS:
            break
        print("Invalid month. Please try again.")

    while True:
        day = input("Enter day of week (all, monday, tuesday, ..., sunday): ").lower()
        if day in ["all"] + DAYS:
            break
        print("Invalid day. Please try again.")

    print("-" * 40)
    return city, month, day


def load_data(city, month, day):
    """Load data for the specified city and filters by month and day."""
    df = pd.read_csv(CITY_DATA[city])

    # Convert Start Time to datetime
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # Extract month, day of week, and hour
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.day_name().str.lower()
    df["hour"] = df["Start Time"].dt.hour

    # Filter by month if applicable
    if month != "all":
        month_num = MONTHS.index(month) + 1
        df = df[df["month"] == month_num]

    # Filter by day of week if applicable
    if day != "all":
        df = df[df["day_of_week"] == day]

    return df


def time_stats(df):
    """Display statistics on the most frequent times of travel."""
    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    if df.empty:
        print("No data available for the selected filters.")
        return

    common_month = df["month"].mode()[0]
    print(f"Most common month: {MONTHS[common_month - 1].title()}")

    common_day = df["day_of_week"].mode()[0]
    print(f"Most common day of week: {common_day.title()}")

    common_hour = df["hour"].mode()[0]
    print(f"Most common hour: {common_hour}:00")

    print("-" * 40)


def station_stats(df):
    """Display statistics on the most popular stations and trip."""
    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    if df.empty:
        print("No data available for the selected filters.")
        return

    common_start = df["Start Station"].mode()[0]
    print(f"Most common start station: {common_start}")

    common_end = df["End Station"].mode()[0]
    print(f"Most common end station: {common_end}")

    common_trip = df.groupby(["Start Station", "End Station"]).size().idxmax()
    print(f"Most common trip: {common_trip[0]} to {common_trip[1]}")

    print("-" * 40)


def trip_duration_stats(df):
    """Display statistics on the total and average trip duration."""
    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    if df.empty:
        print("No data available for the selected filters.")
        return

    total_travel = df["Trip Duration"].sum()
    avg_travel = df["Trip Duration"].mean()

    # Convert total seconds to readable format
    mins, sec = divmod(total_travel, 60)
    hrs, mins = divmod(mins, 60)
    days, hrs = divmod(hrs, 24)

    print(
        f"Total travel time: {int(days)} days, {int(hrs)} hours, {int(mins)} minutes, {int(sec)} seconds"
    )
    print(f"Average travel time: {avg_travel:.2f} seconds")

    print("-" * 40)


def user_stats(df):
    """Display statistics on bikeshare users."""
    print("\nCalculating User Stats...\n")
    start_time = time.time()

    if df.empty:
        print("No data available for the selected filters.")
        return

    print("User Type Counts:")
    print(df["User Type"].value_counts().to_string())

    if "Gender" in df.columns:
        print("\nGender Counts:")
        print(df["Gender"].value_counts().to_string())
    else:
        print("\nGender information not available for this city.")

    if "Birth Year" in df.columns:
        print("\nBirth Year Statistics:")
        print(f"Earliest: {int(df['Birth Year'].min())}")
        print(f"Most Recent: {int(df['Birth Year'].max())}")
        print(f"Most Common: {int(df['Birth Year'].mode()[0])}")
    else:
        print("\nBirth year information not available for this city.")

    print("-" * 40)


def display_data(df):
    """Displays raw data in chunks of 5 rows upon user request."""
    start_loc = 0
    while True:
        # Check if there's data to display
        chunk = df.iloc[start_loc : start_loc + 5]
        if chunk.empty:
            print("No more data to display.")
            break

        # Prompt user
        if start_loc == 0:
            prompt = "Do you want to see the first 5 rows of data? (yes/no): "
        else:
            prompt = "Do you want to see the next 5 rows of data? (yes/no): "

        user_input = input(prompt).lower().strip()
        if user_input == "yes":
            print(chunk)
            start_loc += 5
        elif user_input == "no":
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

        # Check if reached the end of the data
        if start_loc >= len(df):
            print("No more data to display.")
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if df.empty:
            print("No data available for the selected filters.")
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            display_data(df)

        restart = input("\nWould you like to restart? (yes/no): ")
        if restart.lower() != "yes":
            break


if __name__ == "__main__":
    main()
