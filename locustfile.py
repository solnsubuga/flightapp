from locust import HttpLocust, TaskSet, task
import logging
import json


class APIUserBehavior(TaskSet):
    def __init__(self, parent):
        super(APIUserBehavior, self).__init__(parent)
        self.username = 'locust'
        self.password = 'locust_pass'
        self.email = 'user@locust.io'
        self.token = None
        self.headers = {}

    def on_start(self):
        self.token = self.login()
        self.headers = {
            'Authorization': 'Bearer {token}'.format(token=self.token)}

    def on_stop(self):
        pass

    def login(self):
        response = self.client.post(
            '/api/auth/signin/', {'username': self.username, 'password': self.password})
        return json.loads(response._content)['token']

    @task(1)
    def get_flights(self):
        self.client.get('/api/flights/', headers=self.headers)

    @task(2)
    def make_flight_reservation(self):
        flights_response = self.client.get(
            '/api/flights/', headers=self.headers)
        flights_data = json.loads(flights_response._content)
        if flights_data:
            flight = flights_data[0]
            self.client.post('/api/flights/reservations', {
                'flight_number': flight['number'],
                'seat_number': flight['available_seats'][0]['number']
            }, headers=self.headers)


class APIUser(HttpLocust):
    task_set = APIUserBehavior
    min_wait = 5000
    max_wait = 9000
