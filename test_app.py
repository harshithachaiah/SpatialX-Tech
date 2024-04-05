import unittest
from models import user_events
from views import process_event
from app import app
from datetime import datetime


class TestApp(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def tearDown(self):
        pass

    def test_handle_event(self):
    # Test handle_event endpoint for app_launch event type add the the users
        response = self.client.post('/v1/event', json={
            "user_id": "foo1",
            "device_id": "bar",
            "event_type": "app_launch",
            "time_stamp": "2023-04-04 08:21:52"
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(user_events), 1)  # Check if the event is stored
        self.assertIn('foo1', data['message'])
        
        # training_program_started event type
        response = self.client.post('/v1/event', json={
                "user_id": "foo3",
                "device_id": "bar1",
                "event_type": "training_program_started",
                "training_program":{
                    "id": "2352",
                    "title": "7 Minutes of HIIT Training"
                },
                "time_stamp": "2021-02-28 16:23:25"
            })
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(user_events), 2)  # Check if the event is stored
        self.assertIn('foo3', data['message'])
        

        # training_program_finished event type
        response = self.client.post('/v1/event', json={
            "user_id": "foo6",
            "device_id": "bar1",
            "event_type": "training_program_finished",
            "training_program": {
                "id": "2352"
            },
            "time_stamp": "2023-04-04 12:40:43"
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(user_events), 3)  # Check if the event is stored
        self.assertIn('foo6', data['message'])
        
        # training_program_cancelled event type
        response = self.client.post('/v1/event', json={
            "user_id": "foo4",
            "device_id": "bar2",
            "event_type": "training_program_cancelled",
            "training_program": {
            "id": "2352"
            },
            "time_stamp": "2021-02-28 16:54:21"
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(user_events), 4)  # Check if the event is stored
        self.assertIn('foo4', data['message'])
        
        
        
        
        
        # Test the above senario with current time to check after 10 mis to reveive the notification
        # not to receive the congrdulations message since the user has not completed the program yet
        
    def test_handle_event_test1(self):
    # Test handle_event endpoint for app_launch event type add the the users
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response = self.client.post('/v1/event', json={
            "user_id": "foo1",
            "device_id": "bar",
            "event_type": "app_launch",
            "time_stamp": current_time
        })
    
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(user_events), 4)  # Check if the event is stored
        self.assertIn('foo1', data['message'])
        
        # training_program_started event type
        response = self.client.post('/v1/event', json={
                "user_id": "foo3",
                "device_id": "bar1",
                "event_type": "training_program_started",
                "training_program":{
                    "id": "2352",
                    "title": "7 Minutes of HIIT Training"
                },
                "time_stamp": current_time
            })
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(user_events), 4)  # Check if the event is stored
        self.assertIn('foo3', data['message'])
        

        # training_program_finished event type
        response = self.client.post('/v1/event', json={
            "user_id": "foo6",
            "device_id": "bar1",
            "event_type": "training_program_finished",
            "training_program": {
                "id": "2352"
            },
            "time_stamp": current_time
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(user_events), 4)  # Check if the event is stored
        self.assertIn('foo6', data['message'])
        
        # training_program_cancelled event type
        response = self.client.post('/v1/event', json={
            "user_id": "foo4",
            "device_id": "bar2",
            "event_type": "training_program_cancelled",
            "training_program": {
            "id": "2352"
            },
            "time_stamp": current_time
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(user_events), 4)  # Check if the event is stored
        self.assertIn('foo4', data['message'])
        
     

       
       
if __name__ == '__main__':
    unittest.main()
