import requests
from bs4 import BeautifulSoup as bs
import os
import csv


# company name, country, e-mail, contact name, position(title), phone and Website


def saveData(dataset):
    with open('data.csv', mode='a+', encoding='utf-8-sig', newline='') as csvFile:
        fieldnames = ["Company Name", "Country", "Address", "Email", "Contact Name", "Position", "Phone", "Website", "Raw Data"]
        writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
        if os.stat('data.csv').st_size == 0:
            writer.writeheader()
        writer.writerow({
            "Company Name": dataset[0],
            "Country": dataset[1],
            "Address": dataset[2],
            "Email": dataset[3],
            "Contact Name": dataset[4],
            "Position": dataset[5],
            "Phone": dataset[6],
            "Website": dataset[7],
            "Raw Data": dataset[8]
        })



def extractCountries():
    link = "https://www.forwarderspages.com/company-directory"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
    }
    try:
        resp = requests.get(link, headers=headers).text
    except:
        print("Failed to open {}".format(link))
        return []
    soup = bs(resp, 'html.parser')
    all_countries = soup.find_all('li', class_="cat-item")
    all_countries = [x.a.get('href') for x in all_countries]
    return all_countries


def extractCompanyList(link):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
    }
    try:
        resp = requests.get(link, headers=headers).text
    except:
        print("Failed to open {}".format(link))
        return []
    soup = bs(resp, 'html.parser')
    all_companies = soup.find_all('h2', class_="entry-title")
    all_companies = [x.a.get('href') for x in all_companies]
    return all_companies


def extractCompanyData(link):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
    }
    try:
        resp = requests.get(link, headers=headers).text
    except:
        print("Failed to open {}".format(link))
        return
    soup = bs(resp, 'html.parser')
    try:
        company_name = soup.find('h1', class_="page-title").text.strip()
    except:
        print("Failed to parse company for url {}".format(link))
        return
    print("Company name: {}".format(company_name))
    try:
        country = soup.find(
            'nav', class_="ct-breadcrumbs").find_all('span')[2].text.strip()
    except:
        country = "N/A"
    print("Country: {}".format(country))
    try:
        other_data = soup.find('article').get_text(separator='\n').strip()
        other_data = other_data.split('\n')
    except:
        print("Could not parse details for {}".format(link))
        return
    raw_data = [x.strip() for x in other_data if x.strip()]
    name = ""
    position = ""
    email = ""
    phone = ""
    website = ""
    address = ""
    other_data = '\n'.join(raw_data)
    for i, person_data in enumerate(raw_data):
        if person_data.lower().startswith("direct line") or person_data.lower().startswith("mobile") or person_data.lower().startswith("emergency call"):
            phone = raw_data[i+1]
        elif person_data.lower().startswith("name"):
            name = raw_data[i+1]
        elif person_data.lower().startswith("title"):
            position = raw_data[i+1]
        elif person_data.lower().startswith("email"):
            email = raw_data[i+1]
        elif person_data.lower().startswith("website"):
            website = raw_data[i+1]
        elif person_data.lower().startswith("address"):
            address = raw_data[i+1]
        if name and position and email:
            saveData([company_name, country, address, email, name, position, phone, website, other_data])
            name = ""
            email = ""
            position = ""
    print(other_data)


if __name__ == '__main__':
    all_countries = extractCountries()
    print("Countries found: {}".format(len(all_countries)))
    for country in all_countries:
        print("Extracting companies from {}".format(country))
        all_companies = extractCompanyList(country)
        for company in all_companies:
            extractCompanyData(company)
