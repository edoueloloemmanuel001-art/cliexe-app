# Refactored Code for Android with Firebase REST API

import requests

# Firebase Database URL
FIREBASE_URL = 'https://your-firebase-url.firebaseio.com/'

# Function to get data from Firebase

def get_data(path):
    response = requests.get(f'{FIREBASE_URL}{path}.json')
    return response.json()

# Function to post data to Firebase

def post_data(path, data):
    response = requests.post(f'{FIREBASE_URL}{path}.json', json=data)
    return response.json()

# Function to update data in Firebase

def update_data(path, data):
    response = requests.patch(f'{FIREBASE_URL}{path}.json', json=data)
    return response.json()

# Function to delete data from Firebase

def delete_data(path):
    response = requests.delete(f'{FIREBASE_URL}{path}.json')
    return response.status_code

# Example usage
if __name__ == '__main__':
    data_to_post = {'name': 'John Doe', 'age': 30}
    print('Posting data:', post_data('users/', data_to_post))

    print('Getting data:', get_data('users/'))
