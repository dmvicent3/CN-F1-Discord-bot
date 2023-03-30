import fastf1
import requests
from tabulate import tabulate

#API: http://ergast.com/mrd/
#FAST-F1 DOCS: https://theoehrly.github.io/Fast-F1/examples/index.html

async def get_drivers_standings(message):
    url = "https://ergast.com/api/f1/current/driverStandings.json"
    response = requests.get(url)
    data = response.json()
    drivers_standings = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
    
    table_data = []
    for driver in drivers_standings:
        position = driver['position']
        nationality = driver['Driver']['nationality']
        flag = flags.get(nationality, "")
        driver_name = flag + ' ' + driver['Driver']['givenName'] + ' ' + driver['Driver']['familyName']
        team = driver['Constructors'][0]['name']
        points = driver['points']
        table_data.append([position, driver_name, team, points])
    
    headers = ['#', 'Driver', 'Team', 'Points']
    table_str = tabulate(table_data, headers=headers, tablefmt='pretty')
    await message.channel.send(f'{table_str}')

# Define the commands dictionary
commands = {
    'drivers': get_drivers_standings,
    # Add more commands here as needed
}

# Map each nationality to its corresponding flag emoji
flags = {
    "British": "🇬🇧",
    "German": "🇩🇪",
    "Finnish": "🇫🇮",
    "Australian": "🇦🇺",
    "Mexican": "🇲🇽",
    "Spanish": "🇪🇸",
    "Canadian": "🇨🇦",
    "Monegasque": "🇲🇨",
    "French": "🇫🇷",
    "Danish": "🇩🇰",
    "Thai": "🇹🇭",
    "Japanese": "🇯🇵",
    "American": "🇺🇸",
    "Chinese": "🇨🇳",
    "Dutch": "🇳🇱",
    "Russian": "🇷🇺",
    "Brazilian": "🇧🇷",
    "Italian": "🇮🇹",
    "Swiss": "🇨🇭",
    "Belgian": "🇧🇪",
    "Polish": "🇵🇱",
    "Argentine": "🇦🇷",
    "Swedish": "🇸🇪",
    "New Zealander": "🇳🇿",
    "Austrian": "🇦🇹",
    "Colombian": "🇨🇴",
    "Venezuelan": "🇻🇪",
    "Indonesian": "🇮🇩",
    "Liechtensteiner": "🇱🇮",
    "Mauritian": "🇲🇺",
    "Portuguese": "🇵🇹",
    "Monégasque": "🇲🇨",
    "South African": "🇿🇦",
    "Irish": "🇮🇪",
    "Jordanian": "🇯🇴",
    "Malaysian": "🇲🇾",
    "Indian": "🇮🇳",
    "San Marino": "🇸🇲",
    "Uruguayan": "🇺🇾",
    "Hungarian": "🇭🇺",
    "Czech": "🇨🇿",
    "Estonian": "🇪🇪",
    "Romanian": "🇷🇴",
    "Israeli": "🇮🇱",
    "Bahraini": "🇧🇭",
    "Chinese-Taipei": "🇹🇼",
    "Slovak": "🇸🇰",
    "Norwegian": "🇳🇴",
    "Icelandic": "🇮🇸",
    "Latvian": "🇱🇻",
    "Costa Rican": "🇨🇷",
    "Lebanese": "🇱🇧",
    "Turkish": "🇹🇷",
    "Zimbabwean": "🇿🇼",
    "Zambian": "🇿🇲"
}