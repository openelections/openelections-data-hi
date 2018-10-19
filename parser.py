 # -*- coding: utf-8 -*-

import csv
import requests

OFFICES = ['President', 'Governor', 'Representative', 'State Senator', 'SELECT A PARTY', 'Lieutenant Governor', 'U.S. Senator']

precinct_file = open("precincts.txt", "r")
csvfile = csv.DictReader(precinct_file, delimiter=',')
precincts = list(csvfile)

def general():
    results = []
    url = "http://files.hawaii.gov/elections/files/results/2008/general/media.txt"
    r = requests.get(url)
    decoded_content = r.content
    reader = csv.DictReader(decoded_content.splitlines(), delimiter=',', encoding='utf-8')
    for row in reader:
        county = next((p['COUNTY'] for p in precincts if row['Precinct Name'] == p['PRECINCT']), None)
        office = row['Contest Title']
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
        party, candidate = row['Candidate Name'].split(') ')
        party = row['Candidate Party']
        votes = row['Total Votes']
        results.append([county, row['Precinct Name'], office, district, party, candidate, None, None, None, row['Total Votes']])
        for col in ['Total Blank Votes', 'Total Over Votes', 'Total Ballots']:
            results.append([county, row['Precinct Name'], office, district, None, col, None, None, None, row[col]])

    with open('2008/20081104__hi__general__precinct.csv','wb') as csvfile:
            csvwriter = csv.writer(csvfile, encoding='utf-8')
            csvwriter.writerow(['county','precinct', 'office', 'district', 'party', 'candidate', 'absentee', 'early_votes', 'election_day', 'votes'])
            csvwriter.writerows(results)

def primary():
    results = []
    url = "https://elections.hawaii.gov/wp-content/results/media.txt"
    r = requests.get(url)
    decoded_content = r.text
    reader = csv.DictReader(decoded_content.splitlines(), delimiter=',', quotechar='"')
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


    with open('2018/20180811__hi__primary__precinct.csv','w') as csvfile:
            csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
            csvwriter.writerow(['county','precinct', 'office', 'district', 'party', 'candidate', 'absentee', 'early_votes', 'election_day', 'votes'])
            csvwriter.writerows(results)

if __name__ == "__main__":
#    general()
    primary()
