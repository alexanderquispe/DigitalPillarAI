import pandas as pd

csv_path = "data/csv/"
# data\csv\projectid_fy_data.csv
# This code is reading a CSV file named "00_projectid_fy_data.csv" located in the directory specified
# by `csv_path`. It then assigns the contents of the CSV file to the variable `project_data`.
main_files = csv_path + "00_projectid_fy_data.csv"
project_data = pd.read_csv(main_files)
project_data.rename(
    columns={
        "Project_Project Id": "projectid",
        "Project Key Dates_Approval FY": "approval_fy",
    },
    inplace=True,
)


all_data = pd.read_csv(csv_path + "00_all_country_data1.csv")
all_data = all_data.dropna(subset="projectid").drop_duplicates(
    subset="projectid", keep="first"
)

# The line `filtered_data = project_data.merge(all_data, on="projectid", how="inner")` is performing a
# merge operation between two pandas DataFrames `project_data` and `all_data` based on the common
# column "projectid".
filtered_data = project_data.merge(all_data, on="projectid", how="inner")

filtered_data.to_csv(csv_path + "01_merged_data_with_powerBI.csv", index=False)
