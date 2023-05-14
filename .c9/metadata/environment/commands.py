{"changed":false,"filter":false,"title":"commands.py","tooltip":"/commands.py","value":"#import fastf1\nimport requests\nfrom tabulate import tabulate\n\n#API: http://ergast.com/mrd/\n#FAST-F1 DOCS: https://theoehrly.github.io/Fast-F1/examples/index.html\n\nasync def get_drivers_standings(message):\n    url = \"https://ergast.com/api/f1/current/driverStandings.json\"\n    response = requests.get(url, timeout=5)\n    data = response.json()\n    drivers_standings = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']\n    \n    table_data = []\n    for driver in drivers_standings:\n        position = driver['position']\n        nationality = driver['Driver']['nationality']\n        flag = flags.get(nationality, \"\")\n        driver_name = flag + ' ' + driver['Driver']['givenName'] + ' ' + driver['Driver']['familyName']\n        team = driver['Constructors'][0]['name']\n        points = driver['points']\n        table_data.append([position, driver_name, team, points])\n    \n    headers = ['#', 'Driver', 'Team', 'Points']\n    table_str = tabulate(table_data, headers=headers, tablefmt='pretty')\n    await message.channel.send(f'{table_str}')\n\n# Define the commands dictionary\ncommands = {\n    'drivers': get_drivers_standings,\n    # Add more commands here as needed\n}\n\n# Map each nationality to its corresponding flag emoji\nflags = {\n    \"British\": \"🇬🇧\",\n    \"German\": \"🇩🇪\",\n    \"Finnish\": \"🇫🇮\",\n    \"Australian\": \"🇦🇺\",\n    \"Mexican\": \"🇲🇽\",\n    \"Spanish\": \"🇪🇸\",\n    \"Canadian\": \"🇨🇦\",\n    \"Monegasque\": \"🇲🇨\",\n    \"French\": \"🇫🇷\",\n    \"Danish\": \"🇩🇰\",\n    \"Thai\": \"🇹🇭\",\n    \"Japanese\": \"🇯🇵\",\n    \"American\": \"🇺🇸\",\n    \"Chinese\": \"🇨🇳\",\n    \"Dutch\": \"🇳🇱\",\n    \"Russian\": \"🇷🇺\",\n    \"Brazilian\": \"🇧🇷\",\n    \"Italian\": \"🇮🇹\",\n    \"Swiss\": \"🇨🇭\",\n    \"Belgian\": \"🇧🇪\",\n    \"Polish\": \"🇵🇱\",\n    \"Argentine\": \"🇦🇷\",\n    \"Swedish\": \"🇸🇪\",\n    \"New Zealander\": \"🇳🇿\",\n    \"Austrian\": \"🇦🇹\",\n    \"Colombian\": \"🇨🇴\",\n    \"Venezuelan\": \"🇻🇪\",\n    \"Indonesian\": \"🇮🇩\",\n    \"Liechtensteiner\": \"🇱🇮\",\n    \"Mauritian\": \"🇲🇺\",\n    \"Portuguese\": \"🇵🇹\",\n    \"Monégasque\": \"🇲🇨\",\n    \"South African\": \"🇿🇦\",\n    \"Irish\": \"🇮🇪\",\n    \"Jordanian\": \"🇯🇴\",\n    \"Malaysian\": \"🇲🇾\",\n    \"Indian\": \"🇮🇳\",\n    \"San Marino\": \"🇸🇲\",\n    \"Uruguayan\": \"🇺🇾\",\n    \"Hungarian\": \"🇭🇺\",\n    \"Czech\": \"🇨🇿\",\n    \"Estonian\": \"🇪🇪\",\n    \"Romanian\": \"🇷🇴\",\n    \"Israeli\": \"🇮🇱\",\n    \"Bahraini\": \"🇧🇭\",\n    \"Chinese-Taipei\": \"🇹🇼\",\n    \"Slovak\": \"🇸🇰\",\n    \"Norwegian\": \"🇳🇴\",\n    \"Icelandic\": \"🇮🇸\",\n    \"Latvian\": \"🇱🇻\",\n    \"Costa Rican\": \"🇨🇷\",\n    \"Lebanese\": \"🇱🇧\",\n    \"Turkish\": \"🇹🇷\",\n    \"Zimbabwean\": \"🇿🇼\",\n    \"Zambian\": \"🇿🇲\"\n}","undoManager":{"mark":-1,"position":-1,"stack":[]},"ace":{"folds":[],"scrolltop":1251,"scrollleft":0,"selection":{"start":{"row":4,"column":5},"end":{"row":4,"column":28},"isBackwards":true},"options":{"guessTabSize":true,"useWrapMode":false,"wrapToView":true},"firstLineState":{"row":68,"state":"start","mode":"ace/mode/python"}},"timestamp":1681462898944}