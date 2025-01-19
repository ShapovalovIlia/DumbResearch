import pandas as pd
import json
import csv


def parse_user_messages_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    user_messages = []
    st = None

    for item in data:
        if (
            item.get("type") == "user_message"
            and item.get("message", {}).get("role") == "user"
        ):
            content = item["message"].get("content", "")
            time_info = item.get("time", {})
            begin_time = time_info.get("end")

            prosody = item.get("models", {}).get("prosody", {})
            scores = prosody.get("scores", {})
            if st is None:
                st = begin_time

            user_messages.append(
                {
                    "time": (begin_time - st) / 600,
                    "thought_data": content,
                    "action_data": "",
                    "boredom": scores.get("boredom"),
                    "interest": scores.get("interest"),
                    "confusion": scores.get("confusion"),
                    "concentration": scores.get("concentration"),
                }
            )

    return user_messages


def save_to_csv(data, output_file):
    with open(output_file, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "time",
                "thought_data",
                "action_data",
                "boredom",
                "interest",
                "confusion",
                "concentration",
            ],
        )
        writer.writeheader()
        writer.writerows(data)


def save_to_exel(*, csv_file: str, excel_file: str):
    data = pd.read_csv(csv_file)
    data.to_excel(excel_file, index=False)


if __name__ == "__main__":
    user_data = parse_user_messages_from_file("data/ERT_output/nonAcademic1.json")
    csv_path = "data/processedData/hume/"
    file_name = "nonAcademic1"
    save_to_csv(user_data, csv_path + file_name + ".csv")
    save_to_exel(
        csv_file=csv_path + file_name + ".csv",
        excel_file=csv_path + file_name + ".xlsx",
    )
