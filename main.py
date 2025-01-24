from os import times

import pandas as pd
import datetime




if __name__ == '__main__':
    filename = "Person Time Entries.csv"
    log_file = "Log"
    timesheet_data = pd.read_csv(filename)
    timesheet_data = timesheet_data[["Date", "Project Name", "Worked Hours"]]
    duplicated_dates = timesheet_data["Date"].duplicated()
    duplicated_projects = timesheet_data["Project Name"].duplicated()

    new_data = []
    new_row = []

    for index, row in timesheet_data.iterrows():
        if not duplicated_dates[index] or "TOIL" in row["Project Name"] or "Holiday" in row["Project Name"]:
            new_data.append(new_row)
            hours = row["Worked Hours"]
            if "Leave" in row["Project Name"]:
                if "TOIL" in row["Project Name"]:
                    Project = "TOIL"
                    hours = 0
                else:
                    Project = "Other Leave"
            elif "Holiday" in row["Project Name"]:
                Project = "Holiday"
            else:
                Project = "Worked"
            day = pd.to_datetime(row['Date']).day_name()

            new_row = [pd.to_datetime(row["Date"]), day, Project, hours]

        else:
            new_row[3] += row["Worked Hours"]

    del new_data[0]
    new_data = pd.DataFrame(new_data, columns = ["Date", "Day", "Activity", "Hours"])
    print(f"Formatted data:\n{new_data}")
    print("\nFilling missing data")
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

        if new_data_again != []:
            new_data_again = pd.DataFrame(new_data_again, columns = ["Date", "Day", "Activity", "Hours"] )
            new_data = pd.concat(objs=[new_data, new_data_again], axis=0).sort_values(by="Date").reset_index(drop=True)


    print("Complete")

    contracted_hours = []

    for index, row in new_data.iterrows():
        if row["Activity"] == "TOIl":
            row["Hours"] = 0

        if row["Day"] == "Friday":
            contracted_hours.append(7)
        elif row["Day"] == "Sunday" or row["Day"] == "Saturday":
            contracted_hours.append(0)
        else:
            contracted_hours.append(7.5)


    new_data["Contracted Hours"] = contracted_hours

    print(f"\nFull data:\n{new_data}")
    hours_worked = new_data["Hours"].sum()
    total_contracted_hours = new_data["Contracted Hours"].sum()
    print(f"\nTotal hours worked = {hours_worked}")
    print(f"Total contracted hours = {total_contracted_hours}")
    print(f"Total TOIL accrued = {hours_worked-total_contracted_hours}")


