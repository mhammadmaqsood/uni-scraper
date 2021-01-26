import csv, requests
from bs4 import BeautifulSoup


def Leads(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    profiles = soup.find_all('a', class_='btn btn-green')
    links = [profile.get('href') for profile in profiles]
    count = 1
    with open('leads.csv', 'a', encoding="utf-8", newline='') as leads_sheet:
        header = csv.DictWriter(leads_sheet, delimiter=',',
                                fieldnames=['Name', 'Designation', 'Department', 'Location', 'Contact', 'Biography'])
        header.writeheader()
        csv_writer = csv.writer(leads_sheet)
        for link in links:
            response = requests.get(link)
            soup = BeautifulSoup(response.text, 'html.parser')
            print(count)
            row = soup.find_all('div', class_='row')[4]
            name = row.find('h2').text.strip()
            designation = row.find('h4').text.strip()
            department = row.find('p').text.strip().split(',')[0]
            location = row.find('p').text.split(',')[1].split('Curriculum')[0].strip().replace('\n', ' ')
            contact = row.find_all('p')[1].find('span').text.replace(' & ', ',').strip()
            biography = row.find_all('p')[2].text.strip()
            if biography == '':
                biography = row.find_all('p')[3].text.strip()
            if '44000' in biography:
                biography = 'N/A'
            csv_writer.writerow([name, designation, department, location, contact, biography])
            count = count + 1
        leads_sheet.close()
    return 'Done'


print(Leads('http://ww3.comsats.edu.pk/cs/Faculty.aspx'))
