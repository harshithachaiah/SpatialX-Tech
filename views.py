
from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import schedule
import time, threading
from models import store_event,user_events
from utils import notify_user, check_training_start_notification,start_scheduler


notification_sent = []

app = Flask(__name__)


@app.route('/v1/event', methods=['POST'])
def handle_event():
    # Handle the event which is sent through the frontend (currently postman app)
    event = request.json
    print("Received Event: ", event)
    process_event(event)
    return jsonify({'message': user_events}), 200
    

def process_event(event):
    # based on the type of the event call specific  functions to process it
    event_type = event.get('event_type')
    if event_type == 'app_launch':
        handle_app_launch(event)
    elif event_type == 'training_program_started':
        handle_training_program_started(event)
    elif event_type == 'training_program_cancelled':
        handle_training_program_cancelled(event)
    elif event_type == 'training_program_finished':
        handle_training_program_finished(event)
    else:
        handle_unknown_event(event)


def handle_app_launch(event):
    # Handle app launch of the application by storing new entry and continous
    # checking for notifications every minute (Notify user after 10 mins using scheduler)
    user_id = event.get('user_id')
    device_id = event.get('device_id')
    time_stamp = event.get('time_stamp')
    store_event(user_id, event)
    threading.Thread(target=start_scheduler, args=(user_id, time_stamp)).start()

    

def handle_training_program_started(event):
    # Handle start of training program and storing new entry 
    user_id = event.get('user_id')
    training_program = event.get('training_program')
    training_program_id = training_program.get('id')
    time_stamp = event.get('time_stamp')
    store_event(user_id, event)
    print(f"{user_id} Started the training program : {training_program_id} at {time_stamp}")

def handle_training_program_cancelled(event):
    # Handle cancellation of training program and storing new entry 
    user_id = event.get('user_id')
    training_program = event.get('training_program')
    training_program_id = training_program.get('id')
    time_stamp = event.get('time_stamp')
    store_event(user_id, event)
    print(f"{user_id} Cancelled the training program : {training_program_id} at {time_stamp}")

def handle_training_program_finished(event):
    # Handle completion of training and storing new entry
    # checking for notifications is sent after 30mins
    user_id = event.get('user_id')
    training_program = event.get('training_program')
    training_program_id = training_program.get('id')
    time_stamp = event.get('time_stamp')
    store_event(user_id, event)
    notify_user(user_id, training_program_id, time_stamp)

def handle_unknown_event(event):
    # handle unknown events 
    pass


if __name__ == '__main__':
    app.run(debug=True)