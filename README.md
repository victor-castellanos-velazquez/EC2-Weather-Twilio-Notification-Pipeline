# EC2-Weather-Twilio-Notification-Pipeline

This project is an automated weather notification system that uses AWS EC2 to query weather data for a specific municipality and sends notifications via Twilio. The project is developed in Python and is designed to run on an AWS EC2 instance. The system leverages a weather API to get real-time weather information and Twilio's API to send SMS notifications to a specified phone number.

## Features

- Fetches real-time weather data for a given location using a Weather API.
- Sends weather alerts via SMS using Twilio's API.
- Designed to run on AWS EC2 for automation and scalability.
- Easy to configure for different municipalities by updating JSON file data.

## Project Structure

wapi_project/ │ 
	├── ec2_project/ │ 
	├── consulta.json # Contains municipality coordinates and names. │ 
	├── credenciales.py # Stores API keys and credentials for Twilio and Weather API. │ 
	├── pronostico_clima.py # Main script to fetch weather and send SMS. │ 
	├── requirements.txt # List of dependencies for the project. │ 
	├── README.md # Project documentation.


## Prerequisites

Before setting up the project, ensure you have the following:

- AWS EC2 instance running Ubuntu.
- Python 3.x installed.
- Twilio account with valid API credentials.
- Access to a weather API (e.g., OpenWeather, WeatherAPI).
- PEM file for SSH access to the EC2 instance.

## Setup Instructions

1. **Clone the repository** to your EC2 instance.

   ```bash
   git clone https://github.com/yourusername/wapi_project.git
   cd wapi_project/ec2_project

2. **Create and activate a virtual environment.
   python3 -m venv venv
   source venv/bin/activate

3. **Install the required packages using pip.
   pip install -r requirements.txt

4. **Update credentials and location data.
	- Modify the credenciales.py file with your Twilio credentials, Weather API key, and other required parameters.
	- Modify consulta.json with the location's latitude and longitude for which you want to fetch the weather.
			

5. **Run the script to fetch the weather and send the SMS notification.
	python pronostico_clima.py

Files Description
	- consulta.json: This file contains the coordinates (latitude, longitude) and name of the municipality for which you want to retrieve weather information.

Example:

	{
  	"Locacion": {
        "name": "City",
        "lat": 00.000000,
        "lon": -00.00000
  }
}

	- credenciales.py: This file holds sensitive credentials such as your Twilio account SID, authentication token, phone numbers, and Weather API key.

r_user = "your_database_user"
r_password = "your_database_password"
r_host = "your_database_host"
r_port = 5432
r_dbname = "your_database_name"
api_key = "your_api_key"
twilio_account_sid = "your_twilio_sid"
twilio_auth_token = "your_twilio_token"
f_phone_number = "your_twilio_phone"
t_phone_number = "recipient_phone"
api_key_wapi = "your_weather_api_key"


	- pronostico_clima.py: The core script that fetches weather information and sends it via Twilio SMS.

Future Enhancements
	- Add support for multiple municipalities.
	- Implement scheduling with AWS Lambda or Apache Airflow for periodic weather checks.
	- Add error handling for API failures and network issues.
	- Use AWS Secrets Manager to securely store credentials
