import re
import os
import json
from collections import defaultdict
from datetime import datetime

HISTORY_FILE_PATH = 'whatsapp_stat/files/history_stat.json'
MEDIA = ["<המדיה לא נכללה>"]
UNSTAT_MESSAGES = []
WITHOUT_WORDS =['לא', 'מה', 'מדיה', 'זה', 'את', 'של', 'על', 'יש', 'אתה', 'עם', 'אני', 'אין', 'הוא', 'אבל', 'איזה', 'גם', 'כל', 'לי', 'רק', 'היה', 'אם', 'טוב', 'חייב', 'כן']

class ChatStats:
    def __init__(self, filepath = 'whatsapp_stat/files/chat_brothers.txt'):
        self.filepath = filepath
        self.chat_name = filepath.split("/")[-1].split(".")[0]
        self.hour_dict = defaultdict(int)
        self.month_dict = defaultdict(int)
        self.year_dict = defaultdict(int)
        self.date_dict = defaultdict(int)
        self.name_dict = defaultdict(int)
        self.person_word_count_dict = defaultdict(lambda: defaultdict(int))
        self.person_next_message = defaultdict(lambda: defaultdict(int))
        self.two_word_dict = defaultdict(lambda: defaultdict(int))
        self.three_word_dict = defaultdict(lambda: defaultdict(int))
        self.name_mapping = {}
        self.data = self._load_data()
        if self.data:
            self.save_statistics_to_json()

    def save_statistics_to_json(self):
        """Save hour, year, month, and person statistics to history.json if it does not already exist."""
        if os.path.exists(HISTORY_FILE_PATH):
            # Prepare data for JSON
            data ={
                    "hour_dict": json.dumps(self.hour_dict),
                    "month_dict": json.dumps(self.month_dict),
                    "year_dict": json.dumps(self.year_dict),
                    "name_dict": json.dumps(self.name_dict),
                }
            existing_data={}
            with open(HISTORY_FILE_PATH, 'r', encoding='utf-8') as file:
                existing_data = json.load(file)
            if self.chat_name in existing_data:
                return
            existing_data[self.chat_name] = data
            with open(HISTORY_FILE_PATH, 'w', encoding='utf-8') as file:
                json.dump(existing_data, file, ensure_ascii=False, indent=4)
        else:
            print("history.json not exists. No changes made.")

    def _load_data(self):
        """Load and parse the chat data from the file."""
        data = []
        current_message = {}

        with open(self.filepath, 'r', encoding='utf-8') as file:
            last_person=None
            for line_num, line in enumerate(file, start=1):
                # Check if the line starts with a date and time pattern
                match = re.match(
                    r'(?P<date>\d{1,2}\.\d{1,2}\.\d{4}), (?P<time>\d{1,2}:\d{2}) - (?P<person>.*?): (?P<message>.*)',
                    line
                )
                
                if match:
                    # If there's an ongoing message, save it to the data list before starting a new one
                    if current_message:
                        data.append(current_message)
                    
                    try:
                        person_raw = match.group('person').strip()
                        person = self._get_person(person_raw)
                        if person == 'dont':
                            continue
                        current_message =self._update_dicts(match,person,last_person)
                        last_person=person
                    except Exception as e:
                        print(f"Error parsing line {line_num}: {line}. Error: {e}")
                        current_message = {}  # Reset if there's an error
                else:
                    # If the line doesn't start a new message, it's a continuation of the current one
                    # print(f'data is {current_message}')
                    # print(f'line {line_num}: {line}')
                    if current_message:
                        current_message["message"] += f" {line.strip()}"

            # Append the last message if it exists
            if current_message:
                data.append(current_message)

        return data
    def _get_person(self, person):
        if person not in self.name_mapping:
            new_name = input(f"Enter the name to replace '{person}': ")
            if new_name=='':
                self.name_mapping[person] = person
            else:
                self.name_mapping[person] = new_name
        return self.name_mapping[person]
    
    def _update_dicts(self,match,person , last_person):
        date_str = match.group('date')
        time_str = match.group('time')
        message = match.group('message').strip()
        
        date = datetime.strptime(date_str, "%d.%m.%Y").date()
        time = datetime.strptime(time_str, "%H:%M").time()
        hour = time.hour
        month = date.month
        year = date.year
        
        # Update statistics
        self.hour_dict[hour] += 1
        self.month_dict[month] += 1
        self.year_dict[year] += 1
        self.date_dict[date] += 1
        self.name_dict[person] += 1
        if last_person:
            self.person_next_message[last_person][person]+=1

        self._process_message(person, message)
        return  {
                "date": date,
                "time": time,
                "person": person,
                "message": message
            }
    def _process_message(self,person,message):
        if message in MEDIA:
            self.person_word_count_dict["שליחה של מדיה"][person] += 1
            self.person_word_count_dict["מדיה"]["count"] += 1
            return
        
        cleaned_message = ''.join(char for char in message if char.isalpha() or char == ' ')

        # Split the message into words, filtering out any words with length <= 1
        words = [word for word in cleaned_message.split() if len(word) > 1]
        
        for i in range(len(words)):
            word = words[i]
            # Update single word statistics
            self.person_word_count_dict[word][person] += 1
            self.person_word_count_dict[word]['count'] += 1

            # Update two-word phrase statistics
            if i < len(words) - 1:
                two_word_phrase = f"{words[i]} {words[i+1]}"
                self.two_word_dict[two_word_phrase][person] += 1
                self.two_word_dict[two_word_phrase]['count'] += 1

            # Update three-word phrase statistics
            if i < len(words) - 2:
                three_word_phrase = f"{words[i]} {words[i+1]} {words[i+2]}"
                self.three_word_dict[three_word_phrase][person] += 1
                self.three_word_dict[three_word_phrase]['count'] += 1