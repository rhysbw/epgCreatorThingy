import re
import ast

# Number word to number mapping
number_word_mapping = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
    'ten': '10'
    # Add more mappings if needed
}

def normalize_name(name, is_epg=False):
    # Convert number words to numbers for EPG channels
    if is_epg:
        for word, number in number_word_mapping.items():
            name = re.sub(r'\b' + word + r'\b', number, name, flags=re.IGNORECASE)

    # Check for a pattern of a dot followed by any two characters at the end
    country_code_pattern = re.compile(r'\.\w{2}$')
    country_code_match = country_code_pattern.search(name)
    if country_code_match:
        country_code = country_code_match.group()
        name = name[:-len(country_code)]  # Remove country code for now
    else:
        country_code = ''

    # Remove all non-alphanumeric characters
    normalized = re.sub(r'\W+', '', name)

    # Add the country code back if it was originally at the end
    normalized += country_code.lower()

    return normalized.lower()

# Read and evaluate M3U channel names
with open('channelID.txt', 'r') as file:
    m3u_content = file.read()
    m3u_list = ast.literal_eval(m3u_content)
    m3u_channels = [normalize_name(channel) for channel in m3u_list]

# Read EPG channel names
with open('epg.txt', 'r') as file:
    epg_channels = [line.strip() for line in file.readlines()]

print(epg_channels)
# Create a mapping from EPG to M3U
mapping = {}
for epg_channel in epg_channels:
    normalized_epg = normalize_name(epg_channel, is_epg=True)
    for m3u_channel in m3u_channels:
        if normalized_epg in m3u_channel:
            print(f'Mapping: {m3u_channel} with {epg_channel}')
            mapping[epg_channel] = m3u_channel
            break

# Read the EPG XML file
with open('epg.xml', 'r') as file:
    file_content = file.read()

# Replace all occurrences of EPG channel names with M3U names
for epg_name, m3u_name in mapping.items():
    file_content = re.sub(r'\b' + re.escape(epg_name) + r'\b', m3u_name, file_content)

# Write to a new XML file
print('writing to epg.xml')
with open('updated_epg_file.xml', 'w') as file:
    file.write(file_content)
