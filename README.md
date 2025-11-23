# 🌤️ Weather TUI ☔

A beautiful Terminal User Interface (TUI) for fetching real-time weather data for any city around the world. Built with Python and the Rich library for stunning terminal visuals.

## ✨ Features

- 🎨 **Beautiful Terminal Interface** - Colorful and intuitive UI powered by Rich
- 🌍 **Global Weather Data** - Get weather information for any city worldwide
- 📊 **Comprehensive Information** - Temperature, humidity, wind, UV index, pressure, and more
- 🌡️ **Visual Progress Bars** - Easy-to-read visual representations of weather metrics
- 🌅 **Sun Times** - Sunrise and sunset information with timezone support
- 🔄 **Interactive Menu** - Search multiple cities in one session
- ⚡ **Fast and Responsive** - Powered by parse.bot weather API

## 📸 Screenshots

### Initial View
![Initial View](how%20it%20looked%20initially.png)

### Entering City Name
![Enter City Name](how%20to%20enter%20the%20name%20of%20the%20city.png)

### Fetching Data
![Fetching Data](fetching%20the%20data%20for%20that%20city.png)

### Weather Display with Summary
![Weather Display](the%20query%20all%20parsed%20and%20ready%20to%20see%20and%20read%20with%20summary%20as%20well.png)

### Exiting the Application
![Exit](how%20to%20exit.png)

## 🚀 Getting Started

### Prerequisites 

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd "Weather TUI"
```

2. Install required dependencies:
```bash
pip install rich requests
```

3. Set up your API credentials:
   - Sign up at [parse.bot](https://parse.bot) to get your API key
   - Open `weather_tui_example.py` and replace the placeholders:
     - `YOUR_API_URL_HERE` with your parse.bot API URL
     - `YOUR_API_KEY_HERE` with your API key
   - Save the file as `weather_tui.py`

### Usage

Run the application:
```bash
python weather_tui.py
```

Or make it executable:
```bash
chmod +x weather_tui.py
./weather_tui.py
```

## 🎯 How to Use

1. **Launch the application** - Run the script to see the welcome screen
2. **Enter a city name** - Type any city name (e.g., "London", "New York", "Tokyo")
3. **View weather data** - See comprehensive weather information displayed beautifully
4. **Search again** - Choose option 1 to search for another city
5. **Exit** - Choose option 2 or press `Ctrl+C` to exit

## 📦 Dependencies

- **[Rich](https://github.com/Textualize/rich)** - Beautiful terminal formatting
- **[Requests](https://docs.python-requests.org/)** - HTTP library for API calls

## 🌟 Weather Information Displayed

- **Location Info**: City name, region, and timezone
- **Current Conditions**: Temperature (with feels-like), weather description, humidity, UV index, and visibility
- **Wind & Pressure**: Wind speed and direction, atmospheric pressure with trends
- **Temperature Details**: 24-hour temperature range and dew point
- **Sun Times**: Sunrise and sunset times, day/night indicator
- **AI Summary**: Natural language weather summary

## 🔧 Technical Details

- Built with **Python 3**
- Uses **parse.bot** API for weather data
- Rich library for terminal UI components
- Color-coded temperature displays
- Visual progress bars for metrics
- Error handling for network issues
- Keyboard interrupt support

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

Copyright (c) 2025 Mudit Atrey

## 👤 Author

Created with ❤️ by Mudit Atrey

## 🙏 Acknowledgments

- Weather data provided by [parse.bot](https://parse.bot)
- Terminal UI powered by [Rich](https://github.com/Textualize/rich)
- Icons and emojis for visual enhancement

---

**Note**: Remember to keep your API key secure and never commit it to version control. The `weather_tui.py` file (with your actual API key) is ignored by git for security.
