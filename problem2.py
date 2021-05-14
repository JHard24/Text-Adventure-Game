import urllib.request

BASE_URL = 'https://www.ics.uci.edu/~thornton/ics32/Exercises/Set4/Ants/'
FOOTER = '.dat'

def url_to_text(base_url: str, location: str) -> str:
    '''Return the text at the desired URL (given the base_url and location).
    '''
    url = base_url + location + FOOTER
    response = urllib.request.urlopen(url)
    data = response.read()
    response.close()
    return data.decode(encoding = 'utf-8')

def text_to_dict(text: str) -> dict:
    '''Return a dict containing all of the information in text (the text from
    a URL describing a location).
    '''
    location_dict = {}
    lines = text.splitlines()
    index = 0
    location_dict['title'] = lines[index][len('TITLE '):]
    index += 2
    location_dict['description'] = ''
    while lines[index] != 'END DESCRIPTION':
        if lines[index] == '':
            location_dict['description'] += '\n'
        else:
            location_dict['description'] += lines[index] + '\n'
        index += 1
    location_dict['description'] = location_dict['description'][:-1]
    index += 2
    location_dict['commands'] = ''
    while lines[index] != 'END COMMANDS':
        location_dict['commands'] += lines[index] + '\n'
        index += 1
    location_dict['commands'] = location_dict['commands'][:-1]
    index += 1
    location_dict['game over'] = False
    if len(lines) > index and lines[index] == 'GAME OVER':
        location_dict['game over'] = True
    return location_dict

def print_location_info(location_dict: dict) -> None:
    '''Print the information contained in the location_dict.
    '''
    print('\n' + location_dict['title'], end = '\n\n')
    print(location_dict['description'], end = '\n\n')

def valid_command(location_dict: dict, the_command: str) -> bool:
    '''Check if command is among the valid commands found in the location_dict.
    '''
    valid_commands = []
    for line in location_dict['commands'].splitlines():
        commands = line[:line.find(':')]
        commands = commands.split(',')
        for command in commands:
            valid_commands.append(command)
    #print(valid_commands)
    return the_command in valid_commands

def get_new_location(location_dict: dict, the_command: str) -> str:
    '''Return the new location given the location_dict and the command,
    '''
    command_map = {}
    for line in location_dict['commands'].splitlines():
        commands = line[:line.find(':')]
        commands = commands.split(',')
        for command in commands:
            command_map[command] = line[line.find(':') + 1:]
    #print(command_map)
    return command_map[the_command]

if __name__ == '__main__':
    base_url = input('Enter base URL for a text adventure game (leave blank for default): ')
    if base_url == '':
        base_url = BASE_URL

    location_text = url_to_text(base_url, 'start')
    location_dict = text_to_dict(location_text)
    print_location_info(location_dict)

    while True:
        command = input('Enter a command (example commands: NORTH, SOUTH, UP, DOWN, OPEN DOOR): ').upper()
        if not valid_command(location_dict, command):
            print('Invalid command. Try again.')
        else:
            new_location = get_new_location(location_dict, command)
            location_text = url_to_text(base_url, new_location)
            location_dict = text_to_dict(location_text)
            print_location_info(location_dict)
            if location_dict['game over']:
                break

    print('Game over')
