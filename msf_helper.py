import pymsf as msf
import config


def connect():
    return msf.MsfClient(user=config.msfUser, password=config.msfPass, port=config.msfPort, ssl=False)

def updateSessionsList():
    global sessions
    sessions = getSessionsList()


# Get info about session in human-readable format for bot
def getInfo(session_id, session):
    return 'Session ID: ' + str(session_id) + ', IP (external): ' + str(session[b'tunnel_peer'], 'utf-8').split(':')[0] \
           + ', IP (internal): ' + session[b'session_host'] \
           + ', Server Port: ' + str(session[b'tunnel_local'], 'utf-8').split(':')[1] + ', Type: ' \
           + str(session[b'type'], 'utf-8') + ', Info: ' + str(session[b'info'], 'utf-8')


def getSessionsList():
    # Without this, pymetasploit try to use connection many times and get an error CannotSendRequest
    client = connect()
    return client.sessions.list


# Get list of sessions for bot
def getHumanSessionList():
    global sessions
    sessions_h = dict()
    updateSessionsList()
    for key, value in sessions.items():
        sessions_h[key] = getInfo(key, value)
    return sessions_h


def getHumanJobsList():
    client = connect()
    job_list = client.jobs.list
    jobs_h = list()

    for job_id in job_list:
        jobs_h.append(
            'ID: ' + str(job_id) + ', Payload: ' + str(client.jobs.info(job_id)['datastore']['PAYLOAD']) + ', LPORT: ' +
            str(client.jobs.info(job_id)['datastore']['LPORT']))

    return jobs_h


# Check for new sessions. Return blank list or list with info
def getNewSessions():
    global sessions
    sessions_human = dict()
    fresh_sessions = getSessionsList()

    temp = (set(fresh_sessions) ^ set(sessions))
    print(temp)
    if temp:
        sessions = fresh_sessions
        for session in temp:
            if session in fresh_sessions:
                sessions_human[session] = 'New session opened: ' + getInfo(session, fresh_sessions[session])
            else:
                sessions_human[session] = 'Session died: ' + str(session)

    return sessions_human


# Connect to msfrpcd
client = connect()

# Get list of sessions for first time
sessions = getSessionsList()
a = 1