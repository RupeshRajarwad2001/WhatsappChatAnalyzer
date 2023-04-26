import re
import pandas as pd
def preprocessor():
    path='name.txt'

    data = {'Date': [], 'user': [], 'Message': []}

    # Loop through the lines in the WhatsApp chat txt file
    with open(path,encoding="utf8") as file:

        for line in file:
            print(line)

            line = line.strip()
            line = line.replace('\u202f', ' ')
            line = line.replace('pm', 'PM ')
            line = line.replace('am', 'AM ')

            if re.match(r'^\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{1,2}\s(A|P)M\s-\s', line):
                split_line = line.split(' - ')
                datetime = split_line[0]

                sender_message = split_line[1]
                # print(sender_message)
                # sender = re.findall(r'^([\w\s]+?):', sender_message)
                # print(sender)

                sender = re.findall(r'^([^:]+):', sender_message)
                # print(sender)

                message = re.findall(r':\s(.+)', sender_message)
                date, time = datetime.split(',')
                data['Date'].append(datetime)

                # data['AM/PM'].append(time.split(' ')[2])
                if len(sender) == 0:
                    data['user'].append("group notification")
                    data['Message'].append(sender_message)
                else:
                    data['user'].append(sender[0])
                    #data['Message'].append(message[0])
                    if len(message) == 0:

                        data['Message'].append("")
                    else:
                        data['Message'].append(message[0])

    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    df['year'] = df['Date'].dt.year
    df['month_num'] = df['Date'].dt.month
    df['Only_date']=df['Date'].dt.date
    df['month'] = df['Date'].dt.month_name()
    df['day'] = df['Date'].dt.day
    df['day_name'] = df['Date'].dt.day_name()
    df['hour'] = df['Date'].dt.hour
    df['minute'] = df['Date'].dt.minute


    return df