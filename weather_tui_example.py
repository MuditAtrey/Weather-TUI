#!/usr/bin/env python3
"""
Weather TUI - Terminal User Interface for Weather API
A beautiful terminal interface to fetch weather data by city.
"""

import requests
import sys
from typing import Optional, Dict, Any

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.prompt import Prompt
    from rich.text import Text
    from rich.layout import Layout
    from rich import box
    from rich.live import Live
    from rich.align import Align
    from rich.columns import Columns
except ImportError:
    print("Error: 'rich' library is required. Install it with: pip install rich")
    sys.exit(1)


class WeatherTUI:
    """Terminal User Interface for Weather API"""
    
    # TODO: Replace with your own API URL from parse.bot
    API_URL = "YOUR_API_URL_HERE"
    # TODO: Replace with your own API key
    API_KEY = "YOUR_API_KEY_HERE"
    
    def __init__(self):
        self.console = Console()
        self.weather_data: Optional[Dict[str, Any]] = None
    
    def display_header(self):
        """Display the application header"""
        title = Text("🌤️  WEATHER TUI  ☔", style="bold cyan", justify="center")
        subtitle = Text("Get real-time weather data for any city", style="italic", justify="center")
        
        header_panel = Panel(
            Align.center(f"{title}\n{subtitle}"),
            border_style="bright_blue",
            box=box.DOUBLE
        )
        self.console.print(header_panel)
        self.console.print()
    
    def fetch_weather(self, city: str) -> Optional[Dict[str, Any]]:
        """Fetch weather data from the API"""
        payload = {"city": city}
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.API_KEY
        }
        
        try:
            with self.console.status(f"[bold green]Fetching weather for {city}...", spinner="dots"):
                response = requests.post(self.API_URL, json=payload, headers=headers, timeout=10)
                response.raise_for_status()
                return response.json()
        except requests.exceptions.RequestException as e:
            self.console.print(f"[bold red]Error:[/bold red] Failed to fetch weather data: {e}")
            return None
        except Exception as e:
            self.console.print(f"[bold red]Unexpected error:[/bold red] {e}")
            return None
    
    def create_progress_bar(self, value: float, max_value: float, width: int = 20, color: str = "cyan") -> str:
        """Create a visual progress bar"""
        filled = int((value / max_value) * width)
        bar = "█" * filled + "░" * (width - filled)
        return f"[{color}]{bar}[/{color}]"
    
    def get_temp_color(self, temp: float) -> str:
        """Get color based on temperature"""
        if temp < 0:
            return "bright_blue"
        elif temp < 10:
            return "cyan"
        elif temp < 20:
            return "green"
        elif temp < 30:
            return "yellow"
        else:
            return "red"
    
    def display_weather(self, data: Dict[str, Any], city: str):
        """Display weather data in a beautiful format"""
        if not data:
            self.console.print(Panel(
                "[bold red]No weather data available[/bold red]",
                border_style="red"
            ))
            return
        
        # Check if the API returned an error
        if "error" in data or "message" in data:
            error_msg = data.get("error") or data.get("message", "Unknown error")
            self.console.print(Panel(
                f"[bold red]API Error:[/bold red] {error_msg}",
                border_style="red",
                title="❌ Error"
            ))
            return
        
        # Extract nested data
        location = data.get("matched_location", {})
        current = data.get("current_observation", {})
        summary = data.get("weather_summary", "")
        
        # ===== LOCATION PANEL =====
        location_table = Table(show_header=False, box=None, padding=(0, 1))
        location_table.add_column(style="bold cyan", width=15)
        location_table.add_column(style="bright_white")
        
        display_name = location.get("display_name", city)
        display_context = location.get("display_context", "")
        location_table.add_row("📍 Location:", f"[bold yellow]{display_name}[/bold yellow]")
        if display_context:
            location_table.add_row("🌍 Region:", display_context)
        location_table.add_row("🕐 Timezone:", location.get("iana_time_zone", "N/A"))
        
        location_panel = Panel(
            location_table,
            title="[bold bright_blue]📍 Location Info[/bold bright_blue]",
            border_style="bright_blue",
            box=box.ROUNDED
        )
        
        # ===== CURRENT CONDITIONS PANEL =====
        conditions_table = Table(show_header=False, box=None, padding=(0, 1))
        conditions_table.add_column(style="bold yellow", width=18)
        conditions_table.add_column(style="bright_white", no_wrap=False)
        
        # Temperature
        temp = current.get("temperature", 0)
        feels_like = current.get("temperatureFeelsLike", temp)
        temp_color = self.get_temp_color(temp)
        conditions_table.add_row(
            "🌡️  Temperature:", 
            f"[bold {temp_color}]{temp}°C[/bold {temp_color}] (Feels like {feels_like}°C)"
        )
        
        # Weather description
        wx_phrase = current.get("wxPhraseLong", "N/A")
        conditions_table.add_row("☁️  Condition:", f"[bold cyan]{wx_phrase}[/bold cyan]")
        
        # Humidity with progress bar
        humidity = current.get("relativeHumidity", 0)
        humidity_bar = self.create_progress_bar(humidity, 100, 15, "blue")
        conditions_table.add_row("💧 Humidity:", f"{humidity}% {humidity_bar}")
        
        # UV Index with progress bar
        uv_index = current.get("uvIndex", 0)
        uv_desc = current.get("uvDescription", "N/A")
        uv_color = "green" if uv_index < 3 else "yellow" if uv_index < 6 else "orange" if uv_index < 8 else "red"
        uv_bar = self.create_progress_bar(min(uv_index, 11), 11, 15, uv_color)
        conditions_table.add_row("☀️  UV Index:", f"{uv_index} ({uv_desc}) {uv_bar}")
        
        # Visibility
        visibility = current.get("visibility", 0)
        conditions_table.add_row("👁️  Visibility:", f"{visibility} km")
        
        conditions_panel = Panel(
            conditions_table,
            title="[bold green]🌤️  Current Conditions[/bold green]",
            border_style="green",
            box=box.ROUNDED
        )
        
        # ===== WIND & PRESSURE PANEL =====
        wind_table = Table(show_header=False, box=None, padding=(0, 1))
        wind_table.add_column(style="bold yellow", width=18)
        wind_table.add_column(style="bright_white")
        
        wind_speed = current.get("windSpeed", 0)
        wind_dir = current.get("windDirectionCardinal", "N/A")
        wind_bar = self.create_progress_bar(min(wind_speed, 100), 100, 15, "cyan")
        wind_table.add_row("💨 Wind Speed:", f"{wind_speed} km/h {wind_dir}")
        wind_table.add_row("", wind_bar)
        
        pressure = current.get("pressureMeanSeaLevel", 0)
        pressure_trend = current.get("pressureTendencyTrend", "Steady")
        trend_icon = "📈" if "Rising" in pressure_trend else "📉" if "Falling" in pressure_trend else "➡️"
        wind_table.add_row("🎚️  Pressure:", f"{pressure:.1f} mb {trend_icon} {pressure_trend}")
        
        wind_panel = Panel(
            wind_table,
            title="[bold magenta]🌬️  Wind & Pressure[/bold magenta]",
            border_style="magenta",
            box=box.ROUNDED
        )
        
        # ===== TEMPERATURE DETAILS PANEL =====
        temp_table = Table(show_header=False, box=None, padding=(0, 1))
        temp_table.add_column(style="bold yellow", width=18)
        temp_table.add_column(style="bright_white")
        
        temp_max = current.get("temperatureMax24Hour", "N/A")
        temp_min = current.get("temperatureMin24Hour", "N/A")
        dew_point = current.get("temperatureDewPoint", "N/A")
        
        if temp_max != "N/A" and temp_min != "N/A":
            temp_range_bar = self.create_progress_bar(temp - temp_min, temp_max - temp_min, 15, "yellow")
            temp_table.add_row("📊 24h Range:", f"{temp_min}°C → {temp_max}°C")
            temp_table.add_row("", temp_range_bar)
        
        temp_table.add_row("💧 Dew Point:", f"{dew_point}°C")
        
        temp_panel = Panel(
            temp_table,
            title="[bold yellow]🌡️  Temperature Details[/bold yellow]",
            border_style="yellow",
            box=box.ROUNDED
        )
        
        # ===== SUN TIMES PANEL =====
        sun_table = Table(show_header=False, box=None, padding=(0, 1))
        sun_table.add_column(style="bold yellow", width=18)
        sun_table.add_column(style="bright_white")
        
        sunrise = current.get("sunriseTimeLocal", "N/A")
        sunset = current.get("sunsetTimeLocal", "N/A")
        day_or_night = current.get("dayOrNight", "D")
        
        if sunrise != "N/A":
            sunrise = sunrise.split("T")[1][:5] if "T" in sunrise else sunrise
        if sunset != "N/A":
            sunset = sunset.split("T")[1][:5] if "T" in sunset else sunset
        
        sun_table.add_row("🌅 Sunrise:", f"[yellow]{sunrise}[/yellow]")
        sun_table.add_row("🌇 Sunset:", f"[orange1]{sunset}[/orange1]")
        sun_table.add_row("🌓 Period:", f"{'☀️  Daytime' if day_or_night == 'D' else '🌙 Nighttime'}")
        
        sun_panel = Panel(
            sun_table,
            title="[bold orange1]🌅 Sun Times[/bold orange1]",
            border_style="orange1",
            box=box.ROUNDED
        )
        
        # ===== SUMMARY PANEL =====
        if summary:
            summary_panel = Panel(
                f"[bold bright_white]{summary}[/bold bright_white]",
                title="[bold bright_cyan]📝 Summary[/bold bright_cyan]",
                border_style="bright_cyan",
                box=box.ROUNDED
            )
        
        # Display all panels in a nice layout
        self.console.print(location_panel)
        self.console.print(conditions_panel)
        self.console.print(Columns([wind_panel, temp_panel], equal=True, expand=True))
        self.console.print(sun_panel)
        if summary:
            self.console.print(summary_panel)
        self.console.print()
    
    def show_menu(self) -> str:
        """Display menu and get user choice"""
        self.console.print("[bold cyan]Options:[/bold cyan]")
        self.console.print("  [yellow]1.[/yellow] Search for another city")
        self.console.print("  [yellow]2.[/yellow] Exit")
        self.console.print()
        
        choice = Prompt.ask(
            "Choose an option",
            choices=["1", "2"],
            default="1"
        )
        return choice
    
    def run(self):
        """Main application loop"""
        self.console.clear()
        self.display_header()
        
        while True:
            # Get city from user
            city = Prompt.ask("[bold cyan]Enter city name[/bold cyan]", default="London")
            
            if not city.strip():
                self.console.print("[bold red]Please enter a valid city name[/bold red]\n")
                continue
            
            # Fetch and display weather
            self.console.print()
            weather_data = self.fetch_weather(city.strip())
            
            if weather_data:
                self.console.print()
                self.display_weather(weather_data, city)
            
            # Show menu
            self.console.print()
            choice = self.show_menu()
            
            if choice == "2":
                self.console.print("\n[bold green]Thanks for using Weather TUI! 👋[/bold green]\n")
                break
            
            self.console.clear()
            self.display_header()


def main():
    """Entry point for the application"""
    try:
        app = WeatherTUI()
        app.run()
    except KeyboardInterrupt:
        console = Console()
        console.print("\n\n[bold yellow]Application interrupted by user[/bold yellow]")
        console.print("[bold green]Goodbye! 👋[/bold green]\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
