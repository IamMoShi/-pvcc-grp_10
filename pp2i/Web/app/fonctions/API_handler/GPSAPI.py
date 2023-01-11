import requests

def get_coordinates(adress):
    res = requests.get(f'https://nominatim.openstreetmap.org/search?q={adress}&format=json')
    data = res.json()

    if not data:
        return "Coordonnées non trouvées"
    else :
        latitude = data[0]['lat']
        longitude = data[0]['lon']
        return (latitude, longitude)

def get_weather(coords):
    res = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={coords[0]}&longitude={coords[0]}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=Europe%2FBerlin')
    data = res.json()
    print(data['daily'])
    return (data['daily']['temperature_2m_min'],data['daily']['temperature_2m_max'],data['daily']['precipitation_sum'])