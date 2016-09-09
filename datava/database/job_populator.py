__author__ = 'shebashir'

import sys
import googlemaps
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import JobLocations, JobOccupationCategories

# initiate database connection
#engine = create_engine('sqlite:///C:\\Users\\shebashir\\Desktop\\Datathon\\Data\\job_locations.db')
engine = create_engine('sqlite:////home/ubuntu/vadatathon/DataVA-datathon/job_locations.db')
Session = sessionmaker(bind=engine)
session = Session()

# initiate google maps api connection
gmaps = googlemaps.Client(key='AIzaSyBSEvXEo6Tuts7fso0Y8-RPeDkTBX-p0GY')

# read in jobs data
#data = pd.read_table(r'C:\Users\shebashir\Desktop\Datathon\Data\hackathon\joblistings.merged.parsed.unique.grpbyyear.2016.tsv', sep='\t')
#onet = pd.read_table(r'C:\Users\shebashir\Desktop\Datathon\Data\hackathon\onet_hierarchy.txt')
#onet_minor = pd.read_table(r'C:\Users\shebashir\Desktop\Datathon\Data\hackathon\onet_hierarchy_minor.txt')
#onet_broad = pd.read_table(r'C:\Users\shebashir\Desktop\Datathon\Data\hackathon\onet_hierarchy_broad.txt')
#onet_detailed = pd.read_table(r'C:\Users\shebashir\Desktop\Datathon\Data\hackathon\onet_hierarchy_detailed.txt')
data = pd.read_table(r'/home/ubuntu/vadatathon/hackathon/joblistings.merged.parsed.unique.grpbyyear.2016.tsv', sep='\t')
onet = pd.read_table(r'/home/ubuntu/vadatathon/hackathon/onet_hierarchy.txt')
onet_minor = pd.read_table(r'/home/ubuntu/vadatathon/hackathon/onet_hierarchy_minor.txt')
onet_broad = pd.read_table(r'/home/ubuntu/vadatathon/hackathon/onet_hierarchy_broad.txt')
onet_detailed = pd.read_table(r'/home/ubuntu/vadatathon/hackathon/onet_hierarchy_detailed.txt')

def main():
    onet_dict = create_onet_dict(df=onet, group_term='Major_Group', start=0, finish=2)
    onet_minor_dict = create_onet_dict(df=onet_minor, group_term='Minor_Group', start=0, finish=4)
    onet_broad_dict = create_onet_dict(df=onet_broad, group_term='Broad_Group', start=0, finish=6)
    onet_detailed_dict = create_onet_dict(df=onet_detailed, group_term='Detailed_Occupation')

    for ind, row in data.iterrows():
        if ind < 20000:
            continue
        if ind == 40000:
            sys.exit()

        # extract job data
        job_id = row['id']
        listed_latitude = row['jobLocation_geo_latitude']
        listed_longitude = row['jobLocation_geo_longitude']
        hiringOrganization = row['hiringOrganization_organizationName']
        jobLocation = row['jobLocation_address_locality']
        occupational_categories = row['occupationalCategory']

        # geocode job locations using Google Places API
        destination = '{} | {}, VA'.format(hiringOrganization, jobLocation)

        #query if destination already exists (then don't waste api call)
        job_exists = session.query(JobLocations).filter_by(destination=destination).first()
        if job_exists:
            latitude = job_exists.latitude,
            longitude = job_exists.longitude,
            locality = job_exists.locality
        else:
            geocode_result = gmaps.places(query=destination,
                                          location=(listed_latitude, listed_longitude))

            # get Google Place results (e.g. Latitude, Longitude)
            try:
                results = geocode_result['results'][1]
            except IndexError:
                continue

            latitude = results['geometry']['location']['lat']
            longitude = results['geometry']['location']['lng']
            types = results['types']
            address = results['formatted_address']

            # Look up an address with reverse geocoding to get the locality
            # Do not use locality from open jobs data set as this needs to match the google API localities
            # from user input locations
            reverse_geocode_result = gmaps.reverse_geocode((latitude, longitude ))

            # skip entries that could not be geocoded
            if len(reverse_geocode_result) == 0:
                continue

            for address in reverse_geocode_result[0]['address_components']:
                if 'locality' in address['types']:
                    locality = address['short_name']
                    break

        # Use Onet data to convert job occupation categories from ids to text values
        job_occupation_category_list = []
        for ind, occupation_code in enumerate(occupational_categories.split('///')):
            # use only the first two digits of the id to reduce the categories to ~20
            occupation_category = onet_dict.get(occupation_code.replace(';','')[0:2], '')
            occupation_minor_category = onet_minor_dict.get(occupation_code.replace(';','')[0:4], '')
            occupation_broad_category = onet_broad_dict.get(occupation_code.replace(';','')[0:6], '')
            occupation_detailed_category = onet_detailed_dict.get(occupation_code.replace(';','')[0:7], '')

            if occupation_category == '':
                continue

            job_occupation_category = JobOccupationCategories(
                id=str(job_id+str(ind)),
                occupation_category=occupation_category,
                occupation_broad_category=occupation_broad_category,
                occupation_minor_category=occupation_minor_category,
                occupation_detailed_category=occupation_detailed_category,
                job_id=str(job_id))

            job_occupation_category_list.append(job_occupation_category)

        job = JobLocations(
            id=str(job_id),
            latitude=str(latitude),
            longitude=str(longitude),
            destination=destination,
            locality=locality,
            job_occupation_categories=job_occupation_category_list
        )

        session.add(job)
        session.commit()


def create_onet_dict(df, group_term, start=None, finish=None):
    """ get dict of onet code to job category names """

    onet_dict = {}
    for ind, row in df.iterrows():
        if start == 0:
            group = row[group_term][start:finish]
        else:
            group = row[group_term]
        job_title = row['Job_Title']
        onet_dict[group] = job_title

    return onet_dict


if __name__ == '__main__': main()

