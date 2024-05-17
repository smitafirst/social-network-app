import requests

# Step 1: Obtain a Token
login_url = 'http://your-domain.com/api/login/'
login_data = {'email': 'user@example.com', 'password': 'password'}
login_response = requests.post(login_url, data=login_data)

# Check if login was successful and a token was returned
if login_response.status_code == 200:
    token = login_response.json().get('token')
    print(f'Token: {token}')
    
    # Step 2: Make an Authenticated Request
    headers = {'Authorization': f'Token {token}'}
    protected_url = 'http://your-domain.com/api/friends/'
    
    response = requests.get(protected_url, headers=headers)
    
    # Print the response from the protected endpoint
    print(response.json())
else:
    print(f'Login failed: {login_response.json()}')
