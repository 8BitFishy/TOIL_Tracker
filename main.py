from os import times

import pandas as pd
import datetime


if __name__ == '__main__':

    #Read timesheet csv
    filename = "Person Time Entries.csv"
    timesheet_data = pd.read_csv(filename)

    #filter for date, booking code and hours
    timesheet_data = timesheet_data[["Date", "Project Name", "Worked Hours"]]

    #get list of duplicated dates
    duplicated_dates = timesheet_data["Date"].duplicated()

    #initialise variables for data processing
    new_data = []
    new_row = []
    toil_used = 0

    #iterate through timesheet data
    for index, row in timesheet_data.iterrows():
        #if row is not a duplicated date or has TOIL or Holiday in the booking code (for half days taken)
        if not duplicated_dates[index] or "TOIL" in row["Project Name"] or "Holiday" in row["Project Name"]:
            #add the filtered data to the new data list
            new_data.append(new_row)
            if "Leave" in row["Project Name"]:
                if "TOIL" in row["Project Name"]:
                    #Filter out toil and increment toil used tally
                    Project = "TOIL"
                    toil_used += row["Worked Hours"]
                else:
                    #combine other leave types (e.g. sick leave etc) into separate category
                    Project = "Other Leave"
            #collect holiday days
            elif "Holiday" in row["Project Name"]:
                Project = "Holiday"
            else:
                Project = "Worked"

            #get day name from date column
            day = pd.to_datetime(row['Date']).day_name()

            #collect filtered data into new row
            new_row = [pd.to_datetime(row["Date"]), day, Project, row["Worked Hours"]]

        else:
            #if row is a duplicated date, add the worked hours to the previous 'new row' list
            new_row[3] += row["Worked Hours"]

    #delete the empty row created on entering iterate loop
    del new_data[0]

    #convert the filtered data into a dataframe
    new_data = pd.DataFrame(new_data, columns = ["Date", "Day", "Activity", "Hours"])

    print(f"Formatted data from your timesheet:\n{new_data}")
    print("\nFilling missing data")
    #print(pd.to_datetime(new_data["Date"][0]))

    #print(pd.to_datetime(new_data["Date"][0]).weekday())
    #initialise loop to close unless criteria causes it to continue
    finished = True
    while finished:
        finished = False
        #initialise new list for missing data (e.g. weekends, days with no hours booked)
        missing_data = []
        #iterate through dataframe
        for index, row in new_data.iterrows():
            #if not the final row in the dataframe
            if index != new_data.shape[0]-1:
                #find date of next calendar day
                next_day = row["Date"] + pd.Timedelta(days=1)
                #if next row is not next calendar day, a day is missing
                if new_data.loc[index + 1]['Date'] != next_day:
                    #continue the loop
                    finished = True
                    #add data for the missing day
                    day_name = next_day.day_name()
                    missing_data.append([next_day, day_name, "Missing", 0])
                    #alert user that a weekday is missing data (doesn't work other way around for some reason)
                    if day_name == "Saturday" or day_name == "Sunday":
                        pass
                    else:
                        print(f"Weekday with no data found: {day_name} - {next_day.date()}")

        #if missing data is not empty
        if missing_data != []:
            #convert the missing data into a dataframe with the same column titles
            missing_data = pd.DataFrame(missing_data, columns = ["Date", "Day", "Activity", "Hours"] )
            #add the two dataframes, sort by date and reset the index
            new_data = pd.concat(objs=[new_data, missing_data], axis=0).sort_values(by="Date").reset_index(drop=True)


    print("Complete")

    #iterate through days and add contracted hours
    contracted_hours = []
    for index, row in new_data.iterrows():
        if row["Day"] == "Friday":
            contracted_hours.append(7)
        elif row["Day"] == "Sunday" or row["Day"] == "Saturday":
            contracted_hours.append(0)
        else:
            contracted_hours.append(7.5)

    #add contracted hours as a new column in the dataframe
    new_data["Contracted Hours"] = contracted_hours

    #print the results
    print(f"\nFull data:\n{new_data}")

    hours_worked = new_data["Hours"].sum()
    total_contracted_hours = new_data["Contracted Hours"].sum()
    toil_accrued = hours_worked-total_contracted_hours

    print(f"\nTotal hours worked = {hours_worked}")
    print(f"Total contracted hours = {total_contracted_hours}")
    print(f"Total TOIL accrued = {toil_accrued}")
    print(f"Total TOIL used = {toil_used}")
    print(f"Total TOIL remaining = {toil_accrued-toil_used}")


