import os
import re
from datetime import datetime, timedelta

def calculate_playtime():
    log_list = os.listdir('data')

    # Compile regex patterns for repeated use
    join_pattern = re.compile(r"\[([01]?[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])\] \[Server thread\/INFO\]: ([^\s]+) joined the game")
    leave_pattern = re.compile(r"\[([01]?[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])\] \[Server thread\/INFO\]: ([^\s]+) left the game")
    # JOIN REGEX: \[([01]?[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])\] \[Server thread\/INFO\]: ([^\s]+) joined the game
    # LEAVE REGEX: \[([01]?[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])\] \[Server thread\/INFO\]: ([^\s]+) left the game

    player_times = {}
    for log in log_list:
        logDate = log.split('-')
        log_contents = open(f"./data/{log}", "r", encoding='utf-8').read()
        join_times = join_pattern.findall(log_contents)
        leave_times = leave_pattern.findall(log_contents)
        
        # Adds each join time to user dict
        for join_info in join_times:
            username = join_info[-1]
            if username not in player_times:
                player_times[username] = {'join': [], 'leave': []}
            
            # Constructs datetime from the log
            current_time = datetime(int(logDate[0]), int(logDate[1]), int(logDate[2]), int(join_info[0]), int(join_info[1]), int(join_info[2]))
            player_times[username]['join'].append(current_time)
        
        # Adds each leave time to user dict
        for leave_info in leave_times:
            username = leave_info[-1]    
            if username not in player_times:
                player_times[username] = {'join': [], 'leave': []}    
            # Constructs datetime from the log
            current_time = datetime(int(logDate[0]), int(logDate[1]), int(logDate[2]), int(leave_info[0]), int(leave_info[1]), int(leave_info[2]))
            player_times[username]['leave'].append(current_time)

    # Calculates Time played for each user and prints
    for curr_player, curr_times in player_times.items():
        curr_player_time_played = timedelta()
        for join_time, leave_time in zip(curr_times['join'], curr_times['leave']):
            curr_player_time_played += leave_time - join_time
        player_hours, remainder = divmod(curr_player_time_played.seconds, 3600)
        player_minutes, seconds = divmod(remainder, 60)
        print(f"{curr_player} has played for {player_hours}:{player_minutes}:{seconds}")
        
if __name__ == "__main__":
    calculate_playtime()



# Checking for non corresponding times
# for i in range(len(player_times['Usdiez']['join'])):
#     print(player_times['Usdiez']['join'][i], player_times['Usdiez']['leave'][i])
#     if (player_times['Usdiez']['join'][i] > player_times['Usdiez']['leave'][i]):
#         print("BAD!")

# for curr_player, curr_times in player_times.items():
#     print(f"{curr_player}'s TIMES: ")
#     for join_time, leave_time in zip(curr_times['join'], curr_times['leave']):
#         print(f"Joined at {join_time}, and left at {leave_time}")

