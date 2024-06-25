import os
import datetime

def ask_mood_input():
    valid_moods = {'happy', 'relaxed', 'apathetic', 'sad', 'angry'}
    while True:
        user_input = input("Enter your current mood (happy, relaxed, apathetic, sad, angry): ").strip().lower()
        if user_input in valid_moods:
            return user_input
        else:
            print("Invalid mood. Please enter one of: happy, relaxed, apathetic, sad, angry.")

def translate_mood_to_integer(mood):
    mood_map = {
        'happy': 2,
        'relaxed': 1,
        'apathetic': 0,
        'sad': -1,
        'angry': -2
    }
    return mood_map[mood]

def store_mood_diary(mood_integer):
    today = datetime.date.today()
    data_dir = 'data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    diary_file = os.path.join(data_dir, 'mood_diary.txt')
    with open(diary_file, 'a') as f:
        f.write(f"{today}: {mood_integer}\n")

def assess_mood():
    today = datetime.date.today()
    today_str = str(today)
    diary_file = os.path.join('data', 'mood_diary.txt')
    
    # Check if mood has already been entered today
    with open(diary_file, 'r') as f:
        lines = f.readlines()
        for line in reversed(lines):
            if today_str in line:
                print("Sorry, you have already entered your mood today.")
                return
    
    # Ask for mood input and store in diary
    mood = ask_mood_input()
    mood_integer = translate_mood_to_integer(mood)
    store_mood_diary(mood_integer)
    
    # Check if there are at least 7 entries in the diary
    if len(lines) < 7:
        print("Not enough entries for diagnosis yet.")
        return
    
    # Retrieve last 7 entries
    last_7_entries = lines[-7:]
    mood_values = [int(entry.split(': ')[1]) for entry in last_7_entries]
    average_mood = round(sum(mood_values) / len(mood_values))
    
    # Diagnose mood disorder
    if mood_values.count(2) >= 5:
        diagnosis = "manic"
    elif mood_values.count(-1) >= 4:
        diagnosis = "depressive"
    elif mood_values.count(0) >= 6:
        diagnosis = "schizoid"
    else:
        diagnosis_map = {
            2: "happy",
            1: "relaxed",
            0: "apathetic",
            -1: "sad",
            -2: "angry"
        }
        diagnosis = diagnosis_map[average_mood]
    
    print(f"Your diagnosis: {diagnosis.capitalize()}!")

