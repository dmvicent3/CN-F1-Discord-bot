import requests
from tabulate import tabulate

#API: http://ergast.com/mrd/

async def get_constructors_standings(message, args=None):
    if args == None:
        year = "current"
    else:
        if len(args) > 0:
            year = args[0]
    
    url = f"https://ergast.com/api/f1/{year}/constructorStandings.json"
    response = requests.get(url, timeout=5)
    data = response.json()
    try:
        constructors_standings = data['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']
    except KeyError:
        await message.channel.send("Invalid year")
        return
    
    table_data = []
    for constructor in constructors_standings:
        position = constructor['position']
        nationality = constructor['Constructor']['nationality']
        flag = flags.get(nationality, "")
        constructor_name = flag + ' ' + constructor['Constructor']['name']
        points = constructor['points']
        table_data.append([position, constructor_name, points])
    
    headers = ['#', 'Constructor', 'Points']
    table_str = tabulate(table_data, headers=headers, tablefmt='pretty')
    await message.channel.send(f'{table_str}')


async def get_drivers_standings(message, args=None):
    if args == None:
        year = "current"
    else:
        if len(args) > 0:
            year = args[0]
    
    url = f"https://ergast.com/api/f1/{year}/driverStandings.json"
    response = requests.get(url, timeout=5)
    data = response.json()
    try:
        drivers_standings = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
    except KeyError:
        await message.channel.send("Invalid year")
        return
    
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


async def get_driver_profile(message, args=None):
    if len(args) <= 1:
        await message.channel.send("Please specify the driver's first name and last name")
        return
    
    driver_name = args[0] + " " + args[1]
    url = "http://ergast.com/api/f1/drivers.json?limit=1000"
    response = requests.get(url, timeout=5)
    data = response.json()
    drivers = data['MRData']['DriverTable']['Drivers']
    driver_id = -1
    for driver in drivers:
        if driver['givenName'] + ' ' + driver['familyName'] == driver_name:
            driver_id = driver['driverId']
            break
        
    if driver_id == -1:
        await message.channel.send("Invalid Name")
        return 
    
    url = f"http://ergast.com/api/f1/drivers/{driver_id}.json"
    response = requests.get(url, timeout=5)
    data = response.json()
    
    table_data = []
    driver = data['MRData']['DriverTable']['Drivers'][0]
    driver_name = driver['givenName'] + ' ' + driver['familyName']
    nationality = driver['nationality']
    flag = flags.get(nationality, "")
    driver_name = flag + ' ' + driver_name
    birth = driver['dateOfBirth']
    wiki = driver['url']
   
    table_data.append([driver_name, nationality, birth, wiki])
    headers = ["Driver", "Nationality", "Birthday", "Wiki"]
    
    table_str = tabulate(table_data, headers=headers, tablefmt='pretty')
    await message.channel.send(f'{table_str}')
    
    
async def get_schedule(message, args=None):
    if args == None:
        year = "current"
    else:
        if len(args) > 0:
            year = args[0]
            
    url = f"http://ergast.com/api/f1/{year}.json"
    response = requests.get(url, timeout=5)
    data = response.json()
    try:
        schedule = data['MRData']['RaceTable']['Races']
    except KeyError:
        await message.channel.send("Invalid year")
        return
    
    table_data = []
    i = 0
    for race in schedule:
        race_number = i
        i = i + 1
        race_name = race['raceName']
        date = race['date']
        time = race['time']
        time = time[:-3] + 'GMT+0'
        table_data.append([race_number, race_name, date, time])
    
    headers = ['#', 'Race', 'Date', 'Time']
    table_str = tabulate(table_data, headers=headers, tablefmt='pretty')
    await message.channel.send(f'{"```"+table_str+"```"}')
    
    
async def get_next_grandprix(message):
    url = "https://ergast.com/api/f1/current/next.json"
    response = requests.get(url, timeout=5)
    data = response.json()
    next_grandprix = data['MRData']['RaceTable']['Races'][0]
    next_grandprix_name = next_grandprix['raceName']
    next_grandprix_date = next_grandprix['date']
    next_grandprix_time = next_grandprix['time']
    next_grandprix_time = next_grandprix_time[:-3] + 'GMT+0'
    await message.channel.send(f'The next grandprix is {next_grandprix_name} on {next_grandprix_date} at {next_grandprix_time}')
    
    
async def get_circuits(message, args=None):
    if args == None:
        year = "current"
    else:
        if len(args) > 0:
            year = args[0]
            
    url = f"https://ergast.com/api/f1/{year}/circuits.json"
    response = requests.get(url, timeout=5)
    data = response.json()
    try:
        circuits = data['MRData']['CircuitTable']['Circuits']
    except KeyError:
        await message.channel.send("Invalid year")
        return
    
    table_data = []
    for circuit in circuits:
        circuit_name = circuit['circuitName']
        country = circuit['Location']['country']
        #country flag before the circuit name
        country_flag = flags.get(country, "")
        table_data.append([country_flag + ' ' + circuit_name, country])
    
    headers = ['Circuit', 'Country']
    table_str = tabulate(table_data, headers=headers, tablefmt='pretty')
    await message.channel.send(f'{"```"+table_str+"```"}')
    
    
async def get_circuit_info(message, args=None ):
    if len(args) < 1:
        await message.channel.send("Please enter a circuit name")
        return
    
    circuit_name = ""
    for name in args:
        circuit_name = name if circuit_name == "" else circuit_name + " " + name
        
    url = "https://ergast.com/api/f1/circuits.json?limit=100"
    response = requests.get(url, timeout=5)
    data = response.json()
    
    circuits = data['MRData']['CircuitTable']['Circuits']
    circuit_id = -1
    for circuit in circuits:
        if circuit['circuitName']  == circuit_name:
            circuit_id = circuit['circuitId']
            break

    if circuit_id == -1:
        await message.channel.send("Invalid Name")
        return 

    url = f"http://ergast.com/api/f1/circuits/{circuit_id}.json"
    
    response = requests.get(url, timeout=5)
    data = response.json()
    circuit = data['MRData']['CircuitTable']['Circuits'][0]
    
    table_data = []
    circuit_name = circuit['circuitName']
    country = circuit['Location']['country']
    loc = circuit['Location']['locality']
    wiki = circuit['url']
   
    table_data.append([circuit_name, country, loc, wiki])
    headers = ["Circuit", "Country", "Locality", "Wiki"]
    
    table_str = tabulate(table_data, headers=headers, tablefmt='pretty')
    await message.channel.send(f'{table_str}') 
    
  
async def get_last_results(message):
    url = "http://ergast.com/api/f1/current/last/results.json"
    response = requests.get(url, timeout=5)
    data = response.json()
    race = data['MRData']['RaceTable']['Races'][0]
    
    race_name = race['raceName']
    table_data = []
    results = race['Results']
    for result in results:
        pos = result['position']
        number = result['Driver']['permanentNumber']
        name = result['Driver']['givenName'] + " " + result['Driver']['familyName']
        constructor = result['Constructor']['name']
        laps = result['laps']
        grid = result['grid']
        try:
            time = result['Time']['time']
        except KeyError:
            time = "N/A"
        
        table_data.append([pos, number, name, constructor, laps, time])
        
    headers = ['#', 'Number', 'Driver', 'Team', 'Laps', 'Time']
    table_str = tabulate(table_data, headers=headers, tablefmt='pretty')
    new_line = '\n'
    await message.channel.send(f'{"```" + race_name + new_line + table_str+"```"}')
  
  
async def get_last_qual(message):
    url = "http://ergast.com/api/f1/current/last/qualifying.json"
    response = requests.get(url, timeout=5)
    data = response.json()
    race = data['MRData']['RaceTable']['Races'][0]
    
    race_name = race['raceName']
    table_data = []
    results = race['QualifyingResults']
    for result in results:
        pos = result['position']
        number = result['Driver']['permanentNumber']
        name = result['Driver']['givenName'] + " " + result['Driver']['familyName']
        constructor = result['Constructor']['name']
        try:
            q1 = result['Q1']
        except KeyError:
            q1 = "N/A"
        try:
            q2 = result['Q2']
        except KeyError:
            q2 = "N/A"
        try:
            q3 = result['Q3']
        except KeyError:
            q3 = "N/A"
        
        table_data.append([pos, number, name, constructor, q1, q2, q3])
        
    headers = ['#', 'Number', 'Driver', 'Team', 'Q1', 'Q2', 'Q3']
    table_str = tabulate(table_data, headers=headers, tablefmt='github')
    new_line = '\n'
    await message.channel.send(f'{"```" + race_name + new_line + table_str+"```"}')


async def get_race_results(message, args=None):
    if args == 0:
        await message.channel.send("Please specify a year(optinal) and the race number, you can check the race number on !schedule, for example !race 2 or !race 2019 6")
        return
    else:
        if len(args) == 1:
            race_number = args[0]
            url = f"http://ergast.com/api/f1/current/{race_number}/results/.json"
        else:
            race_number = args[1]
            year = args[0]
            url = f"http://ergast.com/api/f1/{year}/{race_number}/results/.json"
            
    response = requests.get(url, timeout=5)
    data = response.json()
    try:
        race = data['MRData']['RaceTable']['Races'][0]
    except KeyError:
        await message.channel.send("Invalid race")
        return
    
    
    race_name = race['raceName']
    table_data = []
    results = race['Results']
    for result in results:
        pos = result['position']
        try:
            number = result['Driver']['permanentNumber']
        except KeyError:
            number = ' '
        name = result['Driver']['givenName'] + " " + result['Driver']['familyName']
        constructor = result['Constructor']['name']
        laps = result['laps']
        grid = result['grid']
        try:
            time = result['Time']['time']
        except KeyError:
            time = "N/A"
        
        table_data.append([pos, number, name, constructor, laps, time])
        
    headers = ['#', 'Number', 'Driver', 'Team', 'Laps', 'Time']
    table_str = tabulate(table_data, headers=headers, tablefmt='pretty')
    new_line = '\n'
    await message.channel.send(f'{"```" + race_name + new_line + table_str+"```"}')
    
    
async def get_qual_results(message, args=None):
    if args == None:
        await message.channel.send("Please specify a year(optinal) and the race number, you can check the race number on !schedule, for example !race 2 or !race 2019 6")
        return
    else:
        if len(args) == 1:
            race_number = args[0]
            url = f"http://ergast.com/api/f1/current/{race_number}/qualifying.json"
        else:
            race_number = args[1]
            year = args[0]
            url = f"http://ergast.com/api/f1/{year}/{race_number}/qualifying.json"
            
    response = requests.get(url, timeout=5)
    data = response.json()
    try:
        race = data['MRData']['RaceTable']['Races'][0]
    except KeyError:
        await message.channel.send("Invalid race")
        return
    
    
    race_name = race['raceName']
    table_data = []
    results = race['QualifyingResults']
    for result in results:
        pos = result['position']
        number = result['Driver']['permanentNumber']
        name = result['Driver']['givenName'] + " " + result['Driver']['familyName']
        constructor = result['Constructor']['name']
        try:
            q1 = result['Q1']
        except KeyError:
            q1 = "N/A"
        try:
            q2 = result['Q2']
        except KeyError:
            q2 = "N/A"
        try:
            q3 = result['Q3']
        except KeyError:
            q3 = "N/A"
        
        table_data.append([pos, number, name, constructor, q1, q2, q3])
        
    headers = ['#', 'Number', 'Driver', 'Team', 'Q1', 'Q2', 'Q3']
    table_str = tabulate(table_data, headers=headers, tablefmt='github')
    new_line = '\n'
    await message.channel.send(f'{"```" + race_name + new_line + table_str+"```"}')
    
    
async def show_help(message, args=None):
    #Sends a message with a table of the available commands and their description
    if args == None:
        table_data = []
        for command in commands:
            table_data.append([command, commands[command]['description']])
        headers = ['Command', 'Description']
        table_str = tabulate(table_data, headers=headers, tablefmt='github')
        await message.channel.send(f'{"```"+table_str+"```"}')
    else:
        #Sends message with the description of the commmand sent as argument
        command = args[0]
        if command in commands:
            await message.channel.send(commands[command]['description'])
        else:
            await message.channel.send(f'Command {command} not found.')



# Define the commands dictionary
commands = {
    'help': {
        'function': show_help,
        'description': 'Displays the current available bot commands or specific command with "!help <command>.'
    },
    'drivers': {
        'function': get_drivers_standings,
        'description': 'Displays the current driver standings in the Championship.'
    },
    'constructors': {
        'function': get_constructors_standings,
        'description': 'Displays the current constructor standings in the Championship.'
    },
    'driver': {
        'function': get_driver_profile,
        'description': 'Displays information of a specific driver.'
    },
    'schedule': {
        'function': get_schedule,
        'description': 'Displays the race schedule for the current or specified year.'
    },
    'nextgp': {
        'function': get_next_grandprix,
        'description': 'Displays whens the next grandprix.'
    },
    'circuits': {
        'function': get_circuits,
        'description': 'Displays the championship circuits.'
    },
    'circuit': {
        'function': get_circuit_info,
        'description': 'Displays circuit information.'
    },
    'last': {
        'function': get_last_results,
        'description': 'Shows results from the last race.'
    },
    'race': {
        'function': get_race_results,
        'description': 'Shows race results for a specific race and year if specified. Example: !race 2003 5, !race 3'
    },
    'lastqual': {
        'function': get_last_qual,
        'description': 'Shows results from the last qualifying.'
    },
    'qual': {
        'function': get_qual_results,
        'description': 'Shows qualifying results for a specific race and year if specified. Example: !qual 2003 5, !qual 3'
    }
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

