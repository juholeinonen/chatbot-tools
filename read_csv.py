import numpy as np
import pandas as pd

chat_csv = pd.read_csv("name.csv", sep=',', engine='python')

transcripts_column = df['Transcript']

with open("customer_service_train.txt", "w", encoding="utf-8") as output_file:
    for _, row in transcripts_column.iterrows():
        replies = row.split("//")
        for reply in replies:
            parts_of_reply = reply.split(":")
            reply_text = parts_of_reply[5:]
            if "User" in parts_of_reply[2]:
                output_file.write("User " + " ".join(reply_text) + "\n")
            else:
                output_file.write("Visitor " + " ".join(reply_text) + "\n")
