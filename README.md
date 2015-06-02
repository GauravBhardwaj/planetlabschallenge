This is a REST service implemented in Flask and python with end points mentioned in api-doc.txt
not a full fledged solution but coded in around 8 hours or so.

To install dependencies
    ```
    $ pip install -r requirements.txt
    ```
To run this app execute following command
    ```
    $ python app.py
    ```
This app will run on port 5000 at 0.0.0.0 , make your user has persmissions to do this
open link: http://0.0.0.0/5000/


Following curl commands can be used to test all endpoints:
1.
```
curl -X GET -H "Content-Type: application/json" -H "Cache-Control: no-cache" http://0.0.0.0:5000/
```

2.
```
curl -X POST -H "Content-Type: application/json" -H "Cache-Control: no-cache" -d '{
"first_name": "Gaurav",
"last_name": "Bhardwaj",
"userid": "gbhardwaj",
"groups": ["interns", "fulltimers"]
}' http://0.0.0.0:5000/userrecord/api/v1.0/users
```

3.
```
curl -X GET -H "Content-Type: application/json" -H "Cache-Control: no-cache"  http://0.0.0.0:5000/userrecord/api/v1.0/users/gbhardwaj
```

4.
```
curl -X PUT -H "Content-Type: application/json" -H "Cache-Control: no-cache" -d '{
    "first_name": "Joe",
    "last_name": "Smith",
    "userid": "gbhardwaj",
    "groups": ["admins1", "users1","grp1"]
}' http://0.0.0.0:5000/userrecord/api/v1.0/users/gbhardwaj
```

5.
```
 curl -X DELETE -H "Content-Type: application/json" -H "Cache-Control: no-cache" -d '' http://0.0.0.0:5000/userrecord/api/v1.0/users/gbhardwaj
```

6.
```
 curl -X GET -H "Content-Type: application/json" -H "Cache-Control: no-cache"  http://0.0.0.0:5000/userrecord/api/v1.0/groups/admins
```

7.
```
curl -X PUT -H "Content-Type: application/json" -H "Cache-Control: no-cache" -d '{
"userlist":["user1","user2","user3"]
}' http://0.0.0.0:5000/userrecord/api/v1.0/groups/group1
```

8.
```
curl -X DELETE -H "Content-Type: application/json" -H "Cache-Control: no-cache" -d '' http://0.0.0.0:5000/userrecord/api/v1.0/groups/pythonists
```

9.
```
curl -X POST -H "Content-Type: application/json" -H "Cache-Control: no-cache" -d '{
"groupname":"newgroup"
}' http://0.0.0.0:5000/userrecord/api/v1.0/groups
```
