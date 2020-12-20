 # -*- coding: utf-8 -*-

import csv
import requests

OFFICES = ['President and Vice President', 'Governor', 'U.S. Representative', 'State Senator', 'State Representative', 'Lieutenant Governor', 'U.S. Senator']

precinct_file = open("precincts.txt", "rt")
csvfile = csv.DictReader(precinct_file, delimiter=',')
precincts = list(csvfile)

def general():
    results = []
    url = "https://elections.hawaii.gov/wp-content/results/media.txt"
    r = requests.get(url)
    decoded_content = r.text
    reader = csv.DictReader(decoded_content.splitlines())
    for row in reader:
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
        party = row['Choice_party']
        votes = int(row['Absentee_votes']) + int(row['Early_votes']) + int(row['Election_Votes'])
        results.append([county, row['Precinct_Name'], office, district, party, row['Candidate_name'], row['Absentee_votes'], row['Early_votes'], row['Election_Votes'], votes])

    with open('2020/20201103__hi__general__precinct.csv','wt') as csvfile:
            csvwriter = csv.writer(csvfile)
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
