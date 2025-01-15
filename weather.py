import streamlit as st
import requests
from bs4 import BeautifulSoup

# Function to fetch weather information
def fetch_weather(location):
    try:
        url = f"https://www.weather-forecast.com/locations/{location}/forecasts/latest"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        weather_info = soup.find("span", {"class": "phrase"})
        return weather_info.text if weather_info else "Weather data unavailable"
    except Exception as e:
        return f"Error fetching weather: {e}"

# Function to display weather for Seven Sisters
def show_weather_seven_sisters():
    st.title("Weather in the Seven Sisters of Northeast India 🌤️")
    st.subheader("Get the latest weather updates for the Seven Sisters states:")
    
    states = {
        "Arunachal Pradesh": "Itanagar",
        "Assam": "Guwahati",
        "Manipur": "Imphal",
        "Meghalaya": "Shillong",
        "Mizoram": "Aizawl",
        "Nagaland": "Kohima",
        "Tripura": "Agartala"
    }

    selected_state = st.selectbox("Select a state:", list(states.keys()))
    if selected_state:
        location = states[selected_state].replace(" ", "-")
        st.write(f"Fetching weather for {selected_state} ({states[selected_state]})...")
        weather = fetch_weather(location)
        st.write(f"**Weather in {selected_state}:** {weather}")

# Run the app
if __name__ == "__main__":
    show_weather_seven_sisters()
