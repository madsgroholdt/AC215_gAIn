import os
import string
import pandas as pd


def csv_to_txt(input_csv, output_txt):
    df = pd.read_csv(input_csv)

    with open(output_txt, "w") as f:
        for _, row in df.iterrows():
            date = row.iloc[0]  # first column is 'date'
            date = pd.to_datetime(date)
            formatted_date = date.strftime("%A, %B %d")
            day_suffix = (
                "th"
                if 11 <= date.day <= 13
                else {1: "st", 2: "nd", 3: "rd"}.get(date.day % 10, "th")
            )
            formatted_date += f"{day_suffix} {date.year}"

            # header for each entry
            f.write(
                f"On {formatted_date}, I had the following health and activity "
                "metrics:\n"
            )

            # get metric values
            for title in df.columns[1:]:
                value = row[title]
                if pd.isna(value):
                    continue

                left_p = title.find("(")
                right_p = title.find(")")
                metric = ""
                if left_p != right_p and left_p != -1:
                    metric = title[left_p + 1: right_p]

                if metric:
                    f.write(f"{string.capwords(title)} was {value} {metric}\n")
                else:
                    f.write(f"{string.capwords(title)} was {value}\n")

            f.write("\n")


if __name__ == "__main__":
    cwd = os.getcwd()
    csv_folder_path = "/csv_data/"
    txt_folder_path = "/txt_data/"
    for filename in os.listdir(cwd + csv_folder_path):
        if filename.endswith(".csv"):
            csv_file = os.path.join(cwd + csv_folder_path, filename)
            txt_file = os.path.join(
                cwd + txt_folder_path, filename.replace(".csv", ".txt")
            )

            csv_to_txt(csv_file, txt_file)
            print(f"Created txt file for {filename}")
