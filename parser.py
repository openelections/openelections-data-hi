 # -*- coding: utf-8 -*-

import unicodecsv as csv
import requests

OFFICES = ['President', 'Governor', 'Representative', 'Senator', 'SELECT A PARTY']

precinct_file = open("precincts.txt", "r")
csvfile = csv.DictReader(precinct_file, delimiter=',')
precincts = list(csvfile)

def general():
    results = []
    url = "http://files.hawaii.gov/elections/files/results/2010/general/media.txt"
    r = requests.get(url)
    decoded_content = r.content
    reader = csv.DictReader(decoded_content.splitlines(), delimiter=',', encoding='utf-8')
    for row in reader:
        if any(x in row['Contest_title'] for x in OFFICES):
            county = next((p['COUNTY'] for p in precincts if row['Precinct_Name'] == p['PRECINCT']), None)
            office = row['Contest_title']
            if 'Dist' in office:
                office, district = office.split(', Dist ')
                if district == 'I':
                    district = "1"
                elif district == 'I Vacancy':
                    district = "1 Unexpired"
                elif district == 'II':
                    district = "2"
            else:
                district = None
            party, candidate = row['Candidate_name'].split(') ')
            party = party.replace('(','')
            votes = int(row['Absentee_votes']) + int(row['Early_votes']) + int(row['Election_Votes'])
            results.append([county, row['Precinct_Name'], office, district, party, candidate, row['Absentee_votes'], row['Early_votes'], row['Election_Votes'], votes])


    with open('2010/20101102__hi__general__precinct.csv','wb') as csvfile:
            csvwriter = csv.writer(csvfile, encoding='utf-8')
            csvwriter.writerow(['county','precinct', 'office', 'district', 'party', 'candidate', 'absentee', 'early_votes', 'election_day', 'votes'])
            csvwriter.writerows(results)

def primary():
    results = []
    url = "http://files.hawaii.gov/elections/files/results/2010/primary/media.txt"
    r = requests.get(url)
    decoded_content = r.content
    reader = csv.DictReader(decoded_content.splitlines(), delimiter=',', encoding='utf-8')
    for row in reader:
        if any(x in row['Contest_title'] for x in OFFICES):
            county = next((p['COUNTY'] for p in precincts if row['Precinct_Name'] == p['PRECINCT']), None)
            if row['Contest_title'] == 'SELECT A PARTY':
                office = 'Straight Party'
                party = None
            else:
                office, party = row['Contest_title'].split(' - ')
            if 'Dist' in office:
                office, district = office.split(', Dist ')
                if district == 'I':
                    district = "1"
                elif district == 'I Vacancy':
                    district = "1 Unexpired"
                elif district == 'II':
                    district = "2"
            else:
                district = None
            votes = int(row['Absentee_votes']) + int(row['Early_votes']) + int(row['Election_Votes'])
            results.append([county, row['Precinct_Name'], office, district, party, row['Candidate_name'], row['Absentee_votes'], row['Early_votes'], row['Election_Votes'], votes])


    with open('2010/20100918__hi__primary__precinct.csv','wb') as csvfile:
            csvwriter = csv.writer(csvfile, encoding='utf-8')
            csvwriter.writerow(['county','precinct', 'office', 'district', 'party', 'candidate', 'absentee', 'early_votes', 'election_day', 'votes'])
            csvwriter.writerows(results)

if __name__ == "__main__":
    general()
    primary()
