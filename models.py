
# Temparory data structure to store user events
user_events = {}

# Array to store whether the user has been notified once after the launch of the application
notification_sent = []


# function to store the events of the user
def store_event(user_id, event):
    if user_id in user_events:
        # User ID exists, change the type field of the existing event
        user_events[user_id]['event_type'] = event['event_type']
        if 'training_program' in event:
            user_events[user_id]['training_program'] = event['training_program']
        elif 'training_program' in user_events[user_id]:
            # Remove the 'training_program' field from the existing event
            del user_events[user_id]['training_program']
    else:
        # User ID does not exist, add the new event
        user_events[user_id] = event
        

