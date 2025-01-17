from os import times

import pandas as pd
import datetime














if __name__ == '__main__':
    filename = "Person Time Entries.csv"
    log_file = "Log"
    timesheet_data = pd.read_csv(filename)
    timesheet_data = timesheet_data[["Date", "Project Name", "Worked Hours"]]
    print(timesheet_data)
    duplicated_dates = timesheet_data["Date"].duplicated()
    duplicated_projects = timesheet_data["Project Name"].duplicated()

    print(duplicated_dates)

    new_data = []
    new_row = []

    for index, row in timesheet_data.iterrows():
        if not duplicated_dates[index] or "TOIL" in row["Project Name"] or "Holiday" in row["Project Name"]:
            new_data.append(new_row)
            if "Leave" in row["Project Name"]:
                if "TOIL" in row["Project Name"]:
                    Project = "TOIL"
                else:
                    Project = "Other Leave"
            elif "Holiday" in row["Project Name"]:
                Project = "Holiday"
            else:
                Project = "Worked"
            day = pd.to_datetime(row['Date']).day_name()

            new_row = [pd.to_datetime(row["Date"]), day, Project, row["Worked Hours"]]

        else:
            new_row[3] += row["Worked Hours"]

    del new_data[0]
    new_data = pd.DataFrame(new_data, columns = ["Date", "Day", "Activity", "Hours"])
    print()
    print(new_data)
    print()
    #print(pd.to_datetime(new_data["Date"][0]))

    #print(pd.to_datetime(new_data["Date"][0]).weekday())
    finished = True
    while finished:
        finished = False
        new_data_again = []
        for index, row in new_data.iterrows():
            if index != new_data.shape[0]-1:
                next_day = row["Date"] + pd.Timedelta(days=1)
                if new_data.loc[index + 1]['Date'] != next_day:
                    finished = True
                    new_data_again.append([next_day, next_day.day_name(), "Missing", 0])

        new_data_again = pd.DataFrame(new_data_again, columns = ["Date", "Day", "Activity", "Hours"] )
        print(f"\nAdding data: \n{new_data_again}")
        new_data = pd.concat(objs=[new_data, new_data_again], axis=0).sort_values(by="Date").reset_index(drop=True)
        print("\nNew Data:\n")

        print(new_data)

        print("Complete\n\n")

    print(f"\nNew data frame below:\n{new_data}")




