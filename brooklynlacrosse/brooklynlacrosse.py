#!/usr/bin/env python

import os
import gdata.spreadsheets.client
import oauth2client.client
import flask
import json
import httplib2

class TokenFromOAuth2Creds:
  def __init__(self, creds):
    self.creds = creds
  def modify_request(self, req):
    if self.creds.access_token_expired or not self.creds.access_token:
      self.creds.refresh(httplib2.Http())
    self.creds.apply(req.headers)

app = flask.Flask(__name__)

json_key = json.load(open('/data/web/brooklynlacrosse/google.json'))
scope = ['https://spreadsheets.google.com/feeds']
credentials = oauth2client.client.SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
client = gdata.spreadsheets.client.SpreadsheetsClient()
client.auth_token = TokenFromOAuth2Creds(credentials)

sheets = ['roster', 'schedule', 'roster_m', 'schedule_m']
data = {}

for sheet in sheets:

    query = gdata.spreadsheets.client.SpreadsheetQuery(title=sheet, title_exact=True)
    feed = client.get_spreadsheets(query=query)

    # get the id of the first spreadsheet, should only be one anyway
    spreadsheet_id = feed.entry[0].id.text.rsplit('/',1)[1]
    feed = client.GetWorksheets(spreadsheet_id)

    # entry[0] is the first worksheet in the spreadhsheet
    worksheet_id = feed.entry[0].id.text.rsplit('/',1)[1]
    rows = client.GetListFeed(spreadsheet_id, worksheet_id).entry

    # in order to preserve the order, we build our own headers
    if 'schedule' in sheet:
        headers = ['date', 'time', 'opponent', 'location']
    if 'roster' in sheet:
        headers = ['position', 'name', 'college']

    # loop through each sheets record, adding the key'd value
    items = []
    for row in rows:
        rec = row.to_dict()
        entry = [rec[header] for header in headers]
        items.append(entry)
        
    # we add each sheet's (header, items) tuple, to a dict with the key being the sheet name
    data[sheet] = (headers, items)

@app.route('/')
def index():
    return flask.render_template('home.html')

@app.route('/about')
def about():
    return flask.render_template('about.html')

@app.route('/roster')
def roster():
    return flask.render_template('table.html', header=data['roster'][0], rows=data['roster'][1], title='2016 A.L.L. Roster')

@app.route('/roster_m')
def roster_m():
    return flask.render_template('table.html', header=data['roster_m'][0], rows=data['roster_m'][1], title='2016 Masters Roster')

@app.route('/schedule')
def schedule():
    return flask.render_template('table.html', header=data['schedule'][0], rows=data['schedule'][1], title='2016 A.L.L. Schedule')

@app.route('/schedule_m')
def schedule_m():
    return flask.render_template('table.html', header=data['schedule_m'][0], rows=data['schedule_m'][1], title='2016 Masters Schedule')

if __name__ == '__main__':
   app.run()
