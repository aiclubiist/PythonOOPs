import requests
data = requests.get('https://db.satnogs.org/api/satellites/')

# print(data.json())

satFile = open('satelliteData.json', 'w', encoding='utf-8')
satFile.write(data.text)
satFile.close()

