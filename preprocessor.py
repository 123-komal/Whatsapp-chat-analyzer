import re
import pandas as pd

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{2}\s*(?:AM|PM)\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # convert message_date type
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M %p - ')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Initialize lists to store users and messages
    users = []
    messages = []

    # Iterate over messages in the 'user_message' column of the DataFrame
    for message in df['user_message']:
        # Split the message using a regex pattern that captures emoji characters
        entry = re.split(r'(?<=.)\s*:\s*', message, maxsplit=1)
        if len(entry) > 1:
            # If the split operation produced enough elements, extract user and message
            users.append(entry[0])
            messages.append(entry[1])
        else:
            # If the split operation didn't produce enough elements, consider it as a group notification
            users.append('group_notification')
            messages.append(entry[0])

    # Add 'user' and 'message' columns to the DataFrame
    df['user'] = users
    df['message'] = messages

    # Drop the original 'user_message' column
    df.drop(columns=['user_message'], inplace=True)

    df['Year'] = df['date'].dt.year
    df['daily_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    df['Month_num'] = df['date'].dt.month
    df['Month'] = df['date'].dt.month_name()
    df['Day'] = df['date'].dt.day
    df['Hour'] = df['date'].dt.hour
    df['AM/PM'] = df['date'].dt.strftime("%p")
    df['Minute'] = df['date'].dt.minute

    period = []
    for hour, am_pm in zip(df["Hour"], df["AM/PM"]):
        if am_pm == 'AM':
            if hour == 12:
                period.append("0-1")
            else:
                period.append(str(hour) + "-" + str(hour + 1))
        else:
            if hour == 12:
                period.append("12-13")
            else:
                period.append(str(hour) + "-" + str(hour + 1))

    df['Period'] = period
    return df
