from flask import Blueprint, json, request,render_template,jsonify
import requests
import urllib.request
from app.extensions import mongo
from flask_cors import CORS,cross_origin
from datetime import datetime

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')
CORS(webhook)
# collection = mongo.db.webhookdb 

def get_pull_request_data(url):
    get_data = requests.get(url)
    data = get_data.json()
    return data

def format_datetime(datetime_str):
    # Parse the datetime string into a datetime object
    date_obj = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S%z')

    # Convert the datetime object to UTC
    date_obj_utc = date_obj - date_obj.utcoffset()

    # Format the datetime object into the desired format
    formatted_date = date_obj_utc.strftime('%d %B %Y - %I:%M %p UTC')

    # Add ordinal suffix to the day
    day = date_obj.day
    suffix = 'th' if 11 <= day <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    formatted_date = formatted_date.replace(str(day), str(day) + suffix)

    return formatted_date

@webhook.route('/receiver', methods=["POST"])
def receiver():
    if request.headers['Content-Type'] == 'application/json':
        get_res = json.dumps(request.json, indent=4)
        res_dict = json.loads(get_res)
        # print(json.dumps(res_dict, indent=4))
        # if res_dict["pusher"]:
        #     print("PUSH")
        # if rec_res["pull_request"]:
        #     print("PULL REQUEST")
        # print(res_dict.keys())
        # print(json.dumps(res_dict, indent=4))

        ##############################################
        key_REQUEST_ID  = None
        key_AUTHOR      = None
        key_ACTION      = None
        key_FROM_BRANCH = None
        key_TO_BRANCH   = None
        key_TIMESTAMP   = None
        ###############################################

        
        if 'pull_request' in res_dict:
            if res_dict['action'] == 'opened':
                url = res_dict['pull_request']['_links']['self']['href']
                url_data = get_pull_request_data(url)
                # print(url_data)
                key_REQUEST_ID  = url_data['id']
                key_AUTHOR      = url_data['user']['login']
                key_ACTION      = 'PULL REQUEST'
                key_FROM_BRANCH = url_data['head']['ref']
                key_TO_BRANCH   = url_data['base']['ref']
                key_TIMESTAMP   = url_data['created_at']
            # print("PR")

            # print(json.dumps(res_dict['commits'],indent=4),)
            # print("HEAD COMMIT ID: ")
            # check = res_dict['pull_request']['_links']['self']['href']
            # r = requests.get(check)
            # dt = r.json()
            # print()

                # print(res_dict['action'])
                # print('REQUEST_ID', key_REQUEST_ID )
                # print('AUTHOR',key_AUTHOR     )
                # print('ACTION',key_ACTION     )
                # print('FROM_BRANCH',key_FROM_BRANCH)
                # print('TO_BRANCH',key_TO_BRANCH  )
                # print('TIMESTAMP',key_TIMESTAMP  )
            # print("REQUEST ID: ",dt['id'])
            # print("AUTHOR: ", json.dumps(dt['user']['login'],indent=4))
            # print("ACTION: PULL REQUEST")
            # print("FROM BRANCH: ", json.dumps(dt['head']['ref'],indent=4))
            # print("TO BRANCH: ", json.dumps(dt['base']['ref'],indent=4))
            # print("TIMESTAMP: ", json.dumps(dt['created_at'],indent=4))
            # print(json.dumps(res_dict['pull_request'], indent=4))
        else:
            get_head_commit_user = res_dict['head_commit']['committer']
            if (get_head_commit_user['username']    != 'web-flow'
            and get_head_commit_user['name']        != 'GitHub'
            and get_head_commit_user['email']       != 'email'):
                key_REQUEST_ID  = res_dict['commits'][0]["id"]
                key_AUTHOR      = res_dict['pusher']['name']
                key_ACTION      = 'PUSH'
                key_FROM_BRANCH = ''
                key_TO_BRANCH   = res_dict['ref'].split('/')[-1]
                key_TIMESTAMP   = res_dict['head_commit']['timestamp']
                # print("PUSH/MERGE")
                # print(json.dumps(res_dict['head_commit']['committer'],indent=4))
                # print(json.dumps(res_dict['head_commit']['committer']['email'],indent=4))
                # print(json.dumps(res_dict['head_commit']['committer']['name'],indent=4))
                # print(json.dumps(res_dict['head_commit']['committer']['username'],indent=4))
                # print('REQUEST_ID', key_REQUEST_ID )
                # print('AUTHOR',key_AUTHOR     )
                # print('ACTION',key_ACTION     )
                # print('FROM_BRANCH',key_FROM_BRANCH)
                # print('TO_BRANCH',key_TO_BRANCH  )
                # print('TIMESTAMP',key_TIMESTAMP  )
                # print("REF: ",json.dumps(res_dict['ref'],indent=4),)
                # print("BASE_REF: ",json.dumps(res_dict['base_ref'],indent=4),)
                # print("COMPARE: ",json.dumps(res_dict['compare'],indent=4),)
                # print("AFTER: ",json.dumps(res_dict['after'],indent=4),)
                # print("BEFORE: ",json.dumps(res_dict['before'],indent=4),)
                # print("HEAD_COMMIT: ",json.dumps(res_dict['head_commit'],indent=4),)
            # print(json.dumps(res_dict['commits'],indent=4),)
            # print("HEAD COMMIT ID: ",json.dumps(res_dict['head_commit']["id"],indent=4))
            # print("REQUEST ID: ",json.dumps(res_dict['commits'][0]["id"],indent=4))
            # print("AUTHOR: ",json.dumps(res_dict['pusher']['name'], indent=4))
            # print("ACTION: PUSH")
            # print("FROM BRANCH: ")
            # print("TO BRANCH: ",json.dumps(res_dict['ref'], indent=4))
            # print("TIMESTAMP: ", json.dumps(res_dict['head_commit']['timestamp']))
        # create-pull-req: dict_keys(['action', 'number', 'pull_request', 'repository', 'sender'])
        
        # psuh: dict_keys(['after', 'base_ref', 'before', 'commits', 'compare', 'created', 'deleted', 'forced', 'head_commit', 'pusher', 'ref', 'repository', 'sender'])

        # merge: dict_keys(['after', 'base_ref', 'before', 'commits', 'compare', 'created', 'deleted', 'forced', 'head_commit', 'pusher', 'ref', 'repository', 'sender'])
        if key_REQUEST_ID is not None:
            webhook_data = {
                'request_id' : key_REQUEST_ID,
                'author' : key_AUTHOR,
                'action': key_ACTION,
                'from_branch': key_FROM_BRANCH,
                'to_branch': key_TO_BRANCH,
                'timestamp': format_datetime(key_TIMESTAMP)
            }
            print(webhook_data)
            collection = mongo.db.webhookdb 
            inserted_data = collection.insert_one(webhook_data).inserted_id
            # inserted_data = mongo.db.webhookdb.insertOne(webhook_data)
            print(inserted_data)
            # print('REQUEST_ID', key_REQUEST_ID )
            # print('AUTHOR',key_AUTHOR     )
            # print('ACTION',key_ACTION     )
            # print('FROM_BRANCH',key_FROM_BRANCH)
            # print('TO_BRANCH',key_TO_BRANCH  )
            # print('TIMESTAMP',key_TIMESTAMP  )
        
        
        return res_dict
    return {}, 200

@webhook.route('/webhook-data', methods=["GET"])
@cross_origin()
def get_webhook_data():
    # data.headers.add("Access-Control-Allow-Origin", "http://localhost:3000/")
    try:
        # data = {"name": "John", "age": 30}
        collection = mongo.db.webhookdb 
        data1 = collection.find().sort("_id", -1)
        # .limit(5)
        data_list = []
        for document in data1:
            document['_id'] = str(document['_id'])
            # print(document)
            data_list.append(document)
        return data_list
        
        # top_5_documents_json = [doc for doc in data1]  # Convert cursor to list of dictionaries
        # print(top_5_documents_json)
        # return jsonify(data)
    except Exception as e:
        print('error')
        return jsonify({"error": str(e)}), 500

