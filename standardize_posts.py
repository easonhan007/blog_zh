import json
from datetime import datetime, timezone, timedelta
import os
import sys

dir_path = './content/posts'

def format():
    for filename in os.listdir(dir_path):
        if filename.endswith('.md'):
            print(f"Formating {filename}")
            filepath = os.path.join(dir_path, filename)

            now = datetime.now(timezone.utc).astimezone()
            date_string = now.strftime('%Y-%m-%dT%H:%M:%S%z')
            date_string = date_string[:-2] + ':' + date_string[-2:]

            title = filename[:-3][:-33]
            data = {'title': title, 'draft': False, 'date': f'{date_string}'}
            json_data = json.dumps(data)
            with open(filepath, 'r+') as file:
                content = file.read()
                file.seek(0, 0)
                file.write(json_data.rstrip('\r\n') + '\n' + content)


def recover():
    for file in os.listdir(dir_path):
        if file.endswith(".md"):
            print(f"Recovering {file}")
            filepath = os.path.join(dir_path, file) # get the full path of the file
            with open(filepath, "r") as f: # open the file for reading
                lines = f.readlines() # get a list of all lines
                lines = lines[1:] # remove the first line from the list
            with open(filepath, "w") as f: # open the file for writing
                f.writelines(lines) # write the modified list to the file

if __name__ == '__main__':
    action = 'format'

    if len(sys.argv) < 2:
        exit('USAGE: python standardize_posts.py format|recover')
    else:
        action = sys.argv[-1].strip().lower()

    if action == 'recover':
        recover()
        exit(0)

    if action == 'format':
        format()
        exit(0)

