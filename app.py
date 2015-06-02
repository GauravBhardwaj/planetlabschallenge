from flask import Flask, jsonify, request, abort

app = Flask(__name__)

#in memory key value store for doing CRUD operations, key will be userid assuming its unique
user_records = {}

#to support user group operations we are making a group and userlist dictionary
user_groups = {}

#writing a helper function to update group information
def update_group_membership_list(grouplist, userid, operation):
    '''
    It helps in keeping our user_groups data structure up to date with latest group assignments
    This function will not work when user put endpoint has passed less number of groups as earlier
    '''
    global user_groups
    if operation == "add":
        for groupname in grouplist:
            #existing_users = user_groups[groupname]
            if groupname in user_groups:
                #existing_users = []
                existing_users = user_groups[groupname]
                existing_users.append(userid)
                user_groups[groupname] = existing_users
                #print user_groups
            else:
                #existing_users = user_groups[groupname]
                user_groups[groupname] = [userid]
    print user_groups

@app.route("/")
def index():
    return ("Thanks PlanetLabs for giving me this opportunity")

@app.route("/userrecord/api/v1.0/users", methods = ['POST'])
def create_new_record():
    '''
    Creates a new user record. The body of the request should be a valid user
    record. POSTs to an existing user should be treated as errors and flagged
    with the appropriate HTTP status code.
    '''
    #if the request is valid, lets assume the request is bad if any of the field is missing or data is not in json
    if not request.json or not 'first_name' in request.json or not 'last_name' in request.json or not 'userid' in request.json or not 'groups' in request.json:
        print "bad request"
        return abort(400)

    #if its not an existing user, (assume userid are unique across the database and generally they are, later we can have a unique code also each data record)
    userid = request.json['userid']
    if userid in user_records:
        return jsonify({'status':"id already exists"}),403

    else:
        userinfo = {
        'first_name':request.json['first_name'],
        'last_name':request.json['last_name'],
        'groups':request.json['groups']
        }
        user_records[userid] = userinfo
        grouplist = userinfo.get('groups')
        #call a helper function to update group membership
        update_group_membership_list(grouplist, userid,"add")
        return jsonify({'record created for user':userid}),201


@app.route('/userrecord/api/v1.0/users/<string:userid>', methods = ['GET'])
def get_one_record(userid):
    '''
    Returns the matching user record or 404 if none exist.
    '''
    #arecord = [user for user in user_records if user['userid']==userid]
    #userid = request.json['userid']
    print userid
    if not userid in user_records:
        print "bad request"
        return abort(404)
    else:
        return jsonify({"record":user_records[userid]})


@app.route('/userrecord/api/v1.0/users/<string:userid>', methods = ['PUT'])
def update_existing_record(userid):
    '''
    Updates an existing user record. The body of the request should be a valid
    user record. PUTs to a non-existant user should return a 404.
    '''
    #arecord = [user for user in user_records if user['userid']==userid]
    #if len(arecord) == 0:
    #    print "Fail: update to non existing record"
    #    return abort(404)
    if not request.json:
        abort(404)

    if not request.json or not 'first_name' in request.json or not 'last_name' in request.json or not 'groups' in request.json:
        abort(404)

    if not userid in user_records:
        # this user record does not exist in our db
        return jsonify({'status':"No such record exist"}),404
    else:
        userinfo = {
        'first_name':request.json['first_name'],
        'last_name':request.json['last_name'],
        'groups':request.json['groups']
        }
        user_records[userid] = userinfo
        #call a helper function to update group membership
        grouplist = userinfo.get('groups')
        update_group_membership_list(grouplist, userid,"update")
        return jsonify({'record updated':user_records[userid]})


@app.route('/userrecord/api/v1.0/users/<string:userid>', methods=['DELETE'])
def delete_record(userid):
    '''
    Deletes a user record. Returns 404 if the user doesn't exist
    '''
    #if not userid in request.json['userid']:
    #    abort(404)
    if not userid in user_records:
        # this user record does not exist in our db
        return jsonify({'status':"No such record exist"}),404
        abort(404)
    else:
        del user_records[userid]
        return jsonify({'record deleted for':userid})


@app.route('/userrecord/api/v1.0/groups/<string:group_name>', methods = ['GET'])
def get_group_members(group_name):
    '''
    Returns a JSON list of userids containing the members of that group. Should
    return a 404 if the group doesn't exist.
    '''
    if not group_name in user_groups:
        return jsonify({'status':"group doesnt exist"}),404

    else:
        return jsonify({'list of users':user_groups[group_name]})


@app.route('/userrecord/api/v1.0/groups',methods = ['POST'])
def create_new_group():
    '''
    Creates a empty group. POSTs to an existing group should be treated as
    errors and flagged with the appropriate HTTP status code. The body should contain
    a name parameter
    '''
    group_name = request.json['groupname']
    if group_name in user_groups:
        return jsonify({'status':"group already exist"}),404

    else:
        user_groups[group_name] = []
        return jsonify({'created group':group_name})


@app.route('/userrecord/api/v1.0/groups/<string:group_name>',methods = ['PUT'])
def update_group_membership(group_name):
    '''
    Updates the membership list for the group. The body of the request should
    be a JSON list describing the group's members.
    '''
    if not 'userlist' in request.json:
        abort(404)
    if not group_name in user_groups:
        return jsonify({'status':"group name doesnt exist"}),404
    else:
        users_list = request.json['userlist']
        existing_users_list = user_groups[group_name]
        users_list = users_list + existing_users_list
        user_groups[group_name] = users_list
        return jsonify({'users added':user_groups[group_name]})


@app.route('/userrecord/api/v1.0/groups/<string:group_name>',methods = ['DELETE'])
def delete_group(group_name):
    '''
    Deletes a group
    '''
    if not group_name in user_groups:
        return jsonify({'status':"group name doesnt exist"}),404
    else:
        del user_groups[group_name]
        return jsonify({'status':"group deleted"})



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
