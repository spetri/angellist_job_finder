#============================================================================
# Lob Challenge
# By: Sabba Petri
# Date: 31 October 2014
# NOTE: I wrote this using Python v2.7.6. Not tested using Python v3.
#============================================================================

import sys
import urllib2
import json

user_id_url = 'https://api.angel.co/1/search?query={final_query}&type=User'
user_url = 'https://api.angel.co/1/users/{user_id}'
tag_url = 'https://api.angel.co/1/tags/{tag_id}/jobs'

def main(query):
  # Exception: If entered name is blank or numerical
  if query is '' or query.isdigit():
    print('Please enter a name.')
    return False
  name = person.replace(' ', '%20')
  user_id = getUserId(name)
  getUserInformation(user_id)

# getUserInformation: Using id of user, gets full user information, including role and location ids
def getUserInformation(user_id):
  user_data = connectionInformation(connectUser(user_id))
  location_id = getLocationId(user_data)
  role_id = getRoleId(user_data)
  getJobs(location_id, role_id)

# getJobs: Find all jobs consistent with the location and role indicated by the candidate and job postings
def getJobs(location_id, role_id):
  startup = {}
  location_data = connectionInformation(connectTag(location_id))
  
  # If location and role match, return startup information
  for jobs_item in location_data['jobs']:
    for tags_item in jobs_item['tags']:
      if tags_item['id'] == role_id:
        startup_data = jobs_item['startup']
        name = startup_data['name']
        startup[name] = startup_data['product_desc']

  # Exception: If no results are found
  if startup.keys() == []:
    print('Available jobs could not be found for the person entered, given their location and role.')
    raise SystemExit

  # Sorted items up to 10
  for startupName in sorted(startup.keys())[:10]:
    print "---- " + startupName + " ----"
    print startup[startupName], "\n"

# getUserId: Queries API and gets user id of the input
def getUserId(name):
  query_information = connectionInformation(connectUserId(name))
  user_id = []
  for user in query_information:
    user_id.append(user['id'])

  # Exception: If no user id exists
  if user_id == []:
    print("The user does not exist on AngelList.")
    raise SystemExit

  # Exception: If AngelList pulls up more than one name
  if len(query_information) > 1:
    print('More than one person found. Please verify.')

  return user_id[0]

# getLocationId: Gets location id from API
def getLocationId(user_data):
  # If no location was entered into the system
  if user_data['locations'] == []:
    print('Error: No location entered into system. Please enter a location into AngelList account.')
    raise SystemExit
  return user_data['locations'][0]['id']

# getRoleId: Gets role id from API
def getRoleId(user_data):
  # If no role was entered into the system
  if user_data['roles'] == []:
    print('Error: No job role entered into system. Please enter a job role into AngelList account.')
    raise SystemExit
  return user_data['roles'][0]['id']

# Below are connections to the AngelList API
def connectUserId(name):
  return urllib2.urlopen(user_id_url.format(final_query=name))  

def connectUser(user_id):
  return urllib2.urlopen(user_url.format(user_id=user_id))

def connectTag(tag_id):
  return urllib2.urlopen(tag_url.format(tag_id=tag_id))

# Returns the JSON data and closes connection
def connectionInformation(connection):
  data = json.load(connection)
  connection.close()
  return data

# Start Here!
if __name__ == '__main__':
    person = raw_input('Enter AngelList account name: ')
    main(person)