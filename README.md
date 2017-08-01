# FuzzApiApi
Fuzzapi's easy to use Python API. This API is written using Flask. All output is given in JSONs

# Features
* Searching for scans - Use of SQL Wildcards (%) may be necessary
* Start scan
* Get results
* User log in

# Prerequisites
This API requires Fuzzapi to be present on the system (so we can read it's database), and the service to be live if you want to run scans. 
This API also requires python

# Testing Environment
The code was written in a Windows 10 machine using Intellij (the best IDE!) and tested on Kali Linux x64 v2017.1 (Debian 64bit). The code was written using Python2.7.13

# Installation
To install this package, simple run `pip install -r requirements.txt`

# Places to do Quick Edits
This tool does not have a config tool (might add one in if it really helps, but not sure yet). The `driver.py` file holds all the configurations that need to be changed to work with your machine. 

`app.config["DBPATH"]` is the path to the Fuzzapi database. This path should be something like /path/to/fuzzapi/db/development.sqlite3

`app.config["FUZZAPI_IP"]` is the server's IP Address

`app.config["FUZZAPI_PORT"]` is the port Fuzzapi is currently running on. 

If you want FuzzApiApi to run on another port (despite 80), then please change the port number to whichever you wish (provided it is not already in use), in the line of code below:

```python
app.run("0.0.0.0", port="80")
```

# Usage
For the usage, we assume the IP address of the server is w.x.y.z and the port is 80
After installing the required dependencies, please run the following command:
`python driver.py`

# API Documentation

| Method 	|    Path   	| Parameters 	|                 Description                	|
|:------:	|:---------:	|:----------:	|:------------------------------------------:	|
|   [GET](#get-all-scans)  	| [/scan/all](#get-all-scans) 	|    [None](#get-all-scans)    	| [Gets all the scans in the Fuzzapi database](#get-all-scans) 	|
|   [GET](#search-all-scans)  	|  [/scan/search](#search-all-scans) 	| [id, url, sid, parameters, method, cookies, created_at, updated_at, json, user_id, status](#search-all-scans) 	| [Searches for relevant records in the scan table. (Wildcards enabled!)](#search-all-scans) 	|
|  [POST](#start-scan)  	|  [/scan/start](#start-scan)  	|                             [user, pass, headers, url, params](#start-scan)                             	|             [Starts the Fuzzapi vulnerability scan process](#start-scan)             	|
|   GET  	| /scan/results 	|                                            id                                            	|          Gets all the vulnerabilities for a specified scan id         	|



## Get All Scans
### Request Example
```
GET /scan/all HTTP/1.1
Host: w.x.y.z


```
### Response Example
```json
[[1, "https://rest.nexmo.com", "9706a8bd209f86201627a306a89eb046", "", "[\"GET\"]", "", "2017-07-26 02:50:18.344585", "2017-07-26 02:50:45.136466", null, 1, "completed"]]
```
Each field in the above array is listed below (basically to help you identify what the data means):
```json
["id", "url", "sid", "parameters", "method", "cookies", "created_at", "updated_at", "json", "user_id", "status"]
```


## Search All Scans
### Request Example
```
GET /scan/search?id=1 HTTP/1.1
Host: w.x.y.z


```
### Response Example
```json
[[1, "https://rest.nexmo.com", "9706a8bd209f86201627a306a89eb046", "", "[\"GET\"]", "", "2017-07-26 02:50:18.344585", "2017-07-26 02:50:45.136466", null, 1, "completed"]]
```
Each field in the above array is listed below (basically to help you identify what the data means):
```json
["id", "url", "sid", "parameters", "method", "cookies", "created_at", "updated_at", "json", "user_id", "status"]
```

These fields can also be used for searching within the database. 


## Start Scan
### Request Example
```
POST /scan/start HTTP/1.1
Host: w.x.y.z

user=username&pass=password&headers=headers&url=https://google.com&params=parameters


```
### Response Example
```
Started the scan! The scan ID is: <number>
```



# Note
Scans (database table and Ruby object) are the actual scan containing the timestamp, target, etc. Vulnerabilities (database table and Ruby object) actually hold the bugs found within the target.