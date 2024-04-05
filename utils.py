import schedule
import time, threading
from datetime import datetime, timedelta
from models import user_events, notification_sent

def notify_user(user_id, training_program_id, time_stamp):
    # Check if training duration is more than 30 minutes
    # and trigger notification to /v1/notify endpoint
    program_end_time = datetime.strptime(time_stamp, '%Y-%m-%d %H:%M:%S')
    current_time = datetime.now()
    minutes_trained = (current_time - program_end_time).total_seconds() // 60

    if minutes_trained > 30:
        notification_message = f"Congratulations! You've completed your training program ({training_program_id}) by training for {minutes_trained} minutes."
        # Call /v1/notify endpoint with notification_message
        print(notification_message)
        

def check_training_start_notification(user_id, time_stamp):
    # Check if app launch duration is more than 10 minutes
    # and trigger notification to /v1/notify endpoint
    current_time = datetime.now()
    for user_id, event_data in user_events.items():
         if event_data.get('event_type') == 'app_launch' and 'time_stamp' in event_data:
            app_launch_time = datetime.strptime(event_data['time_stamp'], '%Y-%m-%d %H:%M:%S')
            app_launch_unix_timestamp = app_launch_time.timestamp()
            if (current_time - app_launch_time) > timedelta(minutes=10):
                if user_id not in notification_sent:
                    # Call /v1/notify endpoint with notification_message
                    notification_message = "Start your training now! It's a great time to get started."
                    print(f"Sending notification to user {user_id}: {notification_message}")
                    notification_sent.append(user_id)


def start_scheduler(user_id, time_stamp):
    # Continuously check for training start notifications for a specific user
    schedule.every(1).minutes.do(check_training_start_notification, user_id, time_stamp)
    while True:
        schedule.run_pending()
        time.sleep(1)