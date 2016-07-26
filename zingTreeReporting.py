import requests
import csv


# Insert your API Key Here
ztHeaders = {
    'authorization': "Basic INSERT_API_KEY_HERE"
    }


# Defines List Variables
# These are for High Level Session View
sessionIdList = []
treeNameList = []
agentList = []
resultList = []
sessionLengthList = []
SessionRowPrinter = []


# This is for Detailed Session View
pathSessionID = []
pathTree = []
pathFromNode = []
pathToNode = []
pathNodeTime = []
pathStepTitle = []
pathQuestion = []
PathRowPrinter = []


# Runs API Call to get list of all sessions from a high level
# Replace below
zingTreeURL = 'http://zingtree.com/api/sessions/YOUR_ORG_KEY_HERE/*/YYYY-06-01/YYYY-07-20'
response = requests.get(url=zingTreeURL, headers=ztHeaders)
Sessions = response.json()


x = 0
z = 0
for session in Sessions['sessions']:  # For each session in list
    sessionId = session['session_id']


    # Pulls each session to get fine details
    zingTreeURL = 'http://zingtree.com/api/session/' + str(sessionId) + '/get_session_data'
    print zingTreeURL
    response = requests.get(url=zingTreeURL, headers=ztHeaders)
    SessionDetail = response.json()


    # Appends fine details to a list
    sessionIdList.append(sessionId)
    treeNameList.append(SessionDetail['tree_name'])
    agentList.append(session['agent'])
    resultList.append(session['resolution_state'])
    sessionLengthList.append(SessionDetail['time_spent'])


    # Appends to an object that will print out the High Level Overview
    SessionRowPrinter.append([sessionIdList[x], treeNameList[x], agentList[x], resultList[x], sessionLengthList[x]])


    # Appends each step to a seperate set of variables for a more granular view
    for step in SessionDetail['path']:
        pathSessionID.append(sessionId)
        pathTree.append(SessionDetail['tree_name'])
        pathStepTitle.append(step['page_title'])
        pathFromNode.append(step['button_text'])
        pathQuestion.append(step['question'])
        pathNodeTime.append(step['time'])


        PathRowPrinter.append([pathSessionID[z], pathTree[z], pathStepTitle[z], pathFromNode[z], pathQuestion[z],
                               pathNodeTime[z]])
        z += 1
    x += 1


# Prints data out to csv files for further analysis
x = 0
with open("dataOutput/ZingTree/Session Report.csv", 'wb') as outcsv:
    # configure writer to write standard csv file
    writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    writer.writerow([
        'sessionIdList, treeNameList, agentList, resultList, sessionLengthList'])
    while x < len(SessionRowPrinter):
        writer.writerow(SessionRowPrinter[x])
        x += 1


x = 0
with open("dataOutput/ZingTree/Step Report.csv", 'wb') as outcsv:
    # configure writer to write standard csv file
    writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    writer.writerow([
        'Path Session ID, Path Tree, Path Step Title, Path From Node, Path Question, Path Node Time'
    ])
    while x < len(PathRowPrinter):
        writer.writerow([sub.encode("utf-8") if isinstance(sub, basestring) else sub for sub in PathRowPrinter[x]])
        x += 1
