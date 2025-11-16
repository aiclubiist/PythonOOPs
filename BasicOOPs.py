#run fetchSate,lliteData.py to generate satelliteData.json file before using this class

import json

class Satellite:
    def __init__(self, sat_id, norad_cat_id, name, status, launched, operator, countries):
        self.sat_id = sat_id
        self.norad_cat_id = norad_cat_id
        self.name = name
        self.status = status
        self.launched = launched
        self.operator = operator
        self.countries = countries

    def get_info(self):
        return f"Satellite({self.norad_cat_id}): {self.name}, ID: {self.sat_id}, Status: {self.status}, Launched: {self.launched}, Operator: {self.operator}, Countries: {self.countries}"

if __name__ == "__main__":
    with open('satelliteData.json', 'r') as file:
        data = json.load(file)

    satellites = []
    for entry in data:
        sat = Satellite(
            sat_id=entry.get('sat_id'),
            norad_cat_id=entry.get('norad_cat_id'),
            name=entry.get('name'),
            status=entry.get('status'),
            launched=entry.get('launched'),
            operator=entry.get('operator'),
            countries=entry.get('countries')
        )
        satellites.append(sat)
    for sat in satellites[:5]:  # Print info of first 5 satellites
        print(sat.get_info())