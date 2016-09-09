__author__ = 'shebashir'
import json
import pandas as pd
import requests
from flask import Flask, request, render_template, url_for, redirect
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import Required
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import googlemaps
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from wtforms.fields.html5 import IntegerRangeField
from wtforms.validators import NumberRange
from modules.occupation_prediction import PredictiveModels
from modules.data_usa_names_and_ids import DataUsaNamesAndIds
from database.models import JobLocations, JobOccupationCategories
#from flask_wtf.csrf import CsrfProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
bootstrap = Bootstrap(app)
#CsrfProtect(app)

# initiate database connection
engine = create_engine('sqlite:///../job_locations.db')
Session = sessionmaker(bind=engine)
session = Session()

### Map information
#initiate map at the VA library - location of hackathon
gmaps = googlemaps.Client(key='AIzaSyBSEvXEo6Tuts7fso0Y8-RPeDkTBX-p0GY')
initial_location = {'lat': 37.5412607, 'lng': -77.4341621}
locality = ''

### import skill survey data
skill_names = pd.read_csv('./static/skills_df.txt')
skill_names_list = skill_names.columns[1:]
occupation_prediction = PredictiveModels()
names_and_ids = DataUsaNamesAndIds()


### FORMS
class Survey(Form):
    """ Survey questions including all skills for a user to provide personal ratings  """
    q0 = IntegerRangeField(label=skill_names_list[0], default=0,
                           validators=[NumberRange(min=0, max=5)])
    q1 = IntegerRangeField(label=skill_names_list[1], default=0,
                           validators=[NumberRange(min=0, max=5)])
    q2 = IntegerRangeField(label=skill_names_list[2], default=0,
                           validators=[NumberRange(min=0, max=5)])
    q3 = IntegerRangeField(label=skill_names_list[3], default=0,
                           validators=[NumberRange(min=0, max=5)])
    q4 = IntegerRangeField(label=skill_names_list[4], default=0,
                           validators=[NumberRange(min=0, max=5)])
    q5 = IntegerRangeField(label=skill_names_list[5], default=0,
                           validators=[NumberRange(min=0, max=5)])
    q6 = IntegerRangeField(label=skill_names_list[6], default=0,
                           validators=[NumberRange(min=0, max=5)])
    q7 = IntegerRangeField(label=skill_names_list[7], default=0,
                           validators=[NumberRange(min=0, max=5)])
    q8 = IntegerRangeField(label=skill_names_list[8], default=0,
                           validators=[NumberRange(min=0, max=5)])
    q9 = IntegerRangeField(label=skill_names_list[9], default=0,
                           validators=[NumberRange(min=0, max=5)])
    q10 = IntegerRangeField(label=skill_names_list[10], default=0,
                           validators=[NumberRange(min=0, max=5)])
    q11 = IntegerRangeField(label=skill_names_list[11], default=0,
                           validators=[NumberRange(min=0, max=5)])
    q12 = IntegerRangeField(label=skill_names_list[12], default=0,
                           validators=[NumberRange(min=0, max=5)])
    q13 = IntegerRangeField(label=skill_names_list[13], default=0,
                           validators=[NumberRange(min=0, max=5)])
    q14 = IntegerRangeField(label=skill_names_list[14], default=0,
                           validators=[NumberRange(min=0, max=5)])
    q15 = IntegerRangeField(label=skill_names_list[15], default=0,
                           validators=[NumberRange(min=0, max=5)])
    q16 = IntegerRangeField(label=skill_names_list[16], default=0,
                           validators=[NumberRange(min=0, max=5)])
    q17 = IntegerRangeField(label=skill_names_list[17], default=0,
                           validators=[NumberRange(min=0, max=5)])
    q18 = IntegerRangeField(label=skill_names_list[18], default=0,
                           validators=[NumberRange(min=0, max=5)])
    q19 = IntegerRangeField(label=skill_names_list[19], default=0,
                           validators=[NumberRange(min=0, max=5)])
    q20 = IntegerRangeField(label=skill_names_list[20], default=0,
                           validators=[NumberRange(min=0, max=5)])
    q21 = IntegerRangeField(label=skill_names_list[21], default=0,
                           validators=[NumberRange(min=0, max=5)])
    q22 = IntegerRangeField(label=skill_names_list[22], default=0,
                           validators=[NumberRange(min=0, max=5)])
    q23 = IntegerRangeField(label=skill_names_list[23], default=0,
                           validators=[NumberRange(min=0, max=5)])
    q24 = IntegerRangeField(label=skill_names_list[24], default=0,
                           validators=[NumberRange(min=0, max=5)])
    q25 = IntegerRangeField(label=skill_names_list[25], default=0,
                           validators=[NumberRange(min=0, max=5)])
    q26 = IntegerRangeField(label=skill_names_list[26], default=0,
                           validators=[NumberRange(min=0, max=5)])
    q27 = IntegerRangeField(label=skill_names_list[27], default=0,
                           validators=[NumberRange(min=0, max=5)])
    q28 = IntegerRangeField(label=skill_names_list[28], default=0,
                           validators=[NumberRange(min=0, max=5)])
    q29 = IntegerRangeField(label=skill_names_list[29], default=0,
                           validators=[NumberRange(min=0, max=5)])
    q30 = IntegerRangeField(label=skill_names_list[30], default=0,
                           validators=[NumberRange(min=0, max=5)])
    q31 = IntegerRangeField(label=skill_names_list[31], default=0,
                           validators=[NumberRange(min=0, max=5)])
    q32 = IntegerRangeField(label=skill_names_list[32], default=0,
                           validators=[NumberRange(min=0, max=5)])
    q33 = IntegerRangeField(label=skill_names_list[33], default=0,
                           validators=[NumberRange(min=0, max=5)])
    q34 = IntegerRangeField(label=skill_names_list[34], default=0,
                           validators=[NumberRange(min=0, max=5)])


### ROUTES
@app.route('/')
@app.route('/datathon/')
def index():
    # initiate the map at the VA library - location of hackathon
    return render_template('index.html')

@app.route('/job/')
def tableau_job():
    return render_template('job.html')

@app.route('/education/')
def tableau_education():
    return render_template('education.html')

@app.route('/initial_map/')
def initial_map():
    # initiate the map at the VA library - location of hackathon
    return render_template('initial_map.html', users_address=json.dumps(initial_location))

@app.route('/initial_map/', methods=['POST'])
def user_map():
    user_address = request.form.get("zoom-to-area-text", "")

    global initial_location
    if user_address == "":
        return render_template('initial_map.html', users_address=json.dumps(initial_location))

    # get locality with google maps
    geocode_result = gmaps.geocode(user_address)
    #parse geocode result to get lat and longitude
    user_latitude = geocode_result[0]['geometry']['location']['lat']
    user_longitude = geocode_result[0]['geometry']['location']['lng']
    initial_location = {'lat': user_latitude, 'lng': user_longitude}

    # get locality of user selected location
    for address_component in geocode_result[0]['address_components']:
        if 'locality' in address_component['types']:
            global locality
            locality = address_component['short_name']
            break

    # query for listings in locality
    job_loc = session.query(JobLocations).filter_by(locality=locality).all()
    locations = create_locations_list(job_loc)

    return render_template('users_map.html', users_address=json.dumps(initial_location), locations=json.dumps(locations))

@app.route('/filter_jobs', methods=['POST'])
def filter_jobs():
    # get lists of categories used to filter job listings
    occupation_categories = []
    for i in range(1,23):
        category = "job_category_" + str(i)
        occupation_category = request.form.get(category, "")
        if occupation_category != "":
            occupation_categories.append(occupation_category)

    job_loc = session.query(JobLocations).join(JobOccupationCategories).filter(JobLocations.locality==locality).filter(JobOccupationCategories.occupation_category.in_(occupation_categories)).all()
    locations = create_locations_list(job_loc)

    return render_template('users_map.html', users_address=json.dumps(initial_location), locations=json.dumps(locations))

@app.route('/nearby_places', methods=['GET', 'POST'])
def nearby_places():
    keyword = request.form.get("search_criteria", "")
    destination = request.form.get("job_title", "")

    # get geolocation details about selected job
    selected_job = session.query(JobLocations).filter_by(destination=destination).first()
    latitude = selected_job.latitude
    longitude = selected_job.longitude

    # update central point for the map
    job_location = {'lat': float(latitude.replace("('","").replace("',)","")), 'lng': float(longitude.replace("('","").replace("',)",""))}
    locations = [{'location': job_location, 'title':destination.replace("'","")}]


    # search for nearby places of interest
    place_of_interest = gmaps.places_nearby(
        location={'lat':latitude,'lng':longitude},
        radius=400,
        keyword=keyword,
        language=None, min_price=None, max_price=None, name=None, open_now=False,
        rank_by=None, type=None, page_token=None
    )

    for result in place_of_interest['results']:
        lat = result['geometry']['location']['lat']
        lng = result['geometry']['location']['lng']
        title = result['name']

        locations.append({'location':{'lat':float(lat),
                                      'lng':float(lng)},
                          'title':title.replace("'","")})

    distance = gmaps.distance_matrix(origins=initial_location, destinations=job_location,
                    mode='walking', language=None, avoid=None, units='imperial',
                    departure_time=None, arrival_time=None, transit_mode=None,
                    transit_routing_preference=None, traffic_model=None)
    minutes_away = distance['rows'][0]['elements'][0]['duration']['text']
    distance = distance['rows'][0]['elements'][0]['distance']['text']

    return render_template('users_map.html',
                           users_address=json.dumps(initial_location),
                           locations=json.dumps(locations),
                           distance=distance,
                           minutes_away=minutes_away)

@app.route('/skills_survey/', methods=['GET', 'POST'])
def skills_survey():
    form = Survey()

    if request.method == 'POST':
        if form.validate():
            print "valid"         
        print(form.errors)
        if 2>1:#form.validate_on_submit():
            q0 = form.q0.data
            q1 = form.q1.data
            q2 = form.q2.data
            q3 = form.q3.data
            q4 = form.q4.data
            q5 = form.q5.data
            q6 = form.q6.data
            q7 = form.q7.data
            q8 = form.q8.data
            q9 = form.q9.data
            q10 = form.q10.data
            q11 = form.q11.data
            q12 = form.q12.data
            q13 = form.q13.data
            q14 = form.q14.data
            q15 = form.q15.data
            q16 = form.q16.data
            q17 = form.q17.data
            q18 = form.q18.data
            q19 = form.q19.data
            q20 = form.q20.data
            q21 = form.q21.data
            q22 = form.q22.data
            q23 = form.q23.data
            q24 = form.q24.data
            q25 = form.q25.data
            q26 = form.q26.data
            q27 = form.q27.data
            q28 = form.q28.data
            q29 = form.q29.data
            q30 = form.q30.data
            q31 = form.q31.data
            q32 = form.q32.data
            q33 = form.q33.data
            q34 = form.q34.data

            prediction_data = [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10,
                               q11, q12, q13, q14, q15, q16, q17, q18, q19, q20,
                               q21, q22, q23, q24, q25, q26, q27, q28, q29, q30,
                               q31, q32, q33, q34]

            _result = occupation_prediction.predict(prediction=prediction_data)
            result = _result.values

            predictions = []
            for ind, row in _result.iterrows():
                val = {'job': row['job'], 'prob': row['prob'], 'soc':row['soc']}
                predictions.append(val)

            # Request skills data on the top matching job
            skills_data = []
            r = requests.get(r'http://api.datausa.io/api/?show=skill&sumlevel=all&soc={}'.format(predictions[0]['soc']))
            data_usa = r.json()
            headers = data_usa['headers']
            data = data_usa['data']
            df = pd.DataFrame(data, columns=headers)
            df = pd.merge(df, names_and_ids.skill_names_and_ids, left_on='skill', right_on='id')

            for ind, row in df.iterrows():
                skill = {'name': 'Skills for Top Matching Job',
                         'skill': row['name'],
                         'soc': row['soc'],
                         'score': row['value']}
                skills_data.append(skill)
            print 'we made it '

            # User's skills
            for ind, skill_pred in enumerate(prediction_data):
                skill = {'name': 'Your Skills',
                         'skill': names_and_ids.skill_names_and_ids['name'][ind],
                         'soc': names_and_ids.skill_names_and_ids['id'][ind],
                         'score': skill_pred}
                skills_data.append(skill)

            return render_template('results.html',
                                   result=result, predictions=json.dumps(predictions),
                                   skills_data=json.dumps(skills_data))

    return render_template('skills_survey.html', form=form, skill_names=skill_names_list)


def create_locations_list(job_loc):
    locations = [{'location':initial_location,'title':'Selected Location'}]

    if not isinstance(job_loc, list):
        job_loc = [job_loc]

    for job in job_loc:
        #todo: some lats and lngs were loaded as tuples with parenthesis, which broke the float casting
        locations.append({'location':{'lat':float(job.latitude.replace("('","").replace("',)","").replace("(u'","")),
                                      'lng':float(job.longitude.replace("('","").replace("',)","").replace("(u'",""))},
                                      'title':job.destination.replace("'","")})
    return locations


if __name__ == "__main__":
    app.debug = True
    app.run('0.0.0.0')
