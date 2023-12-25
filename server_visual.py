import socket
import threading
import math
import path4server
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

HOST = "192.168.1.5"
PORT = 2113
ADR = (HOST,PORT)

HEADER = 64
DISCONNECT_MESSAGE = "!DISCONNECT"

class Agent:
    def __init__(self,id,x,y,status):
        self.id = id
        self.curr_x = x
        self.curr_y = y
        self.status = status
    def updatePosition(self,x,y):
        self.curr_x = x
        self.curr_y = y
    def updateStatus(self,status):
        self.status = status
    def showInfo(self):
        print(f"ID: {self.id}|| Status: {self.status}|| X: {self.curr_x}|| Y: {self.curr_y}")

agent_list = []
wait = True
goal_list = [(2,1),(3,4),(3,2),(6,7),(5,5),(9,9)]
cmap = mpl.colors.ListedColormap(['green','white','red'])
Grid = np.zeros((10,10))
# goal_list = []
job_dict = {}
to_make_path = []
path_dict = {}
vis_grid = np.zeros((10,10))

def calculateDistance(goal_pos,agent_pos):
    gx,gy = goal_pos
    ax,ay = agent_pos
    # distance = math.sqrt((gx-ax)**2+(gy-ay)**2)
    distance = abs(gx-ax) + abs(gy-ay)
    return distance

def assignJob():
    free_agent_list = []
    global job_dict
    job_dict = {}
    if(len(goal_list)):
        for agent in agent_list:
            if(agent.status==0):
                free_agent_list.append(agent)
        # print(free_agent_list)                
    # if(len(free_agent_list)):    
        for goal in goal_list:
            min_dist = 99999
            min_agent = None
            for agent in free_agent_list:
                temp = calculateDistance(goal,(agent.curr_x,agent.curr_y))
                if(temp <= min_dist):
                    min_dist = temp
                    min_agent = agent
            if(min_agent!=None):
                job_dict[goal] = min_agent
                free_agent_list.remove(min_agent)
                # goal_list.remove(goal)
                # print(goal_list)
            else:
                # print(f"No availble agent for {goal} goal")
                pass
        for goal in job_dict.keys():
            goal_list.remove(goal)

def _forward(x):
    return x


def _inverse(x):
    return x

def plot_grid(grid):
    ax = plt.gca()
    norm = mpl.colors.FuncNorm((_forward, _inverse), vmin=-1, vmax=2)
    ax.set_xticks(np.arange(0, 10, 1))
    ax.set_yticks(np.arange(0, 10, 1))
    ax.set_xticklabels(np.arange(0, 10, 1))
    ax.set_yticklabels(np.arange(0, 10, 1))

    ax.set_xticks(np.arange(-.5, 10, 1), minor=True)
    ax.set_yticks(np.arange(-.5, 10, 1), minor=True)
    ax.imshow(grid,cmap=cmap,norm=norm,origin='lower')
    # Gridlines based on minor ticks
    ax.grid(which='minor', color='k', linestyle='-', linewidth=2)
    return ax

def updateGrid(grid):
    with np.nditer(grid,op_flags=['readwrite']) as it:
        for x in it:
            if x!=-1:
                x[...] = 0
    if(len(agent_list)):
        for agent in agent_list:
            x = agent.curr_x
            y = agent.curr_y
            grid[y,x] = 2
    if(len(goal_list)):
        for goal in goal_list:
            x,y = goal
            grid[y,x] = -1
    return grid

def manageOrder():
    global Grid
    global wait

    while True:
        to_make_path = []
        if(wait):
            temp = input("Enter Y to begin: ")
            if(temp == "Y"):
                wait = False
        else:
            enter = input("next")
            # else:
            #     if(len(temp)):
            #         x,y = temp.split(',')
            #         x = int(x)
            #         y = int(y)
            #         temp_goal = (x,y)
            #         goal_list.append(temp_goal)
            # print(goal_list)
            if(len(goal_list)>0 and len(agent_list)>0):
                assignJob()
            if(len(job_dict)>0):
                for goal,agent in job_dict.items():
                    job = {}
                    job['name'] = agent.id
                    job['start'] = [agent.curr_x,agent.curr_y]
                    job['goal'] = list(goal)
                    job['even'] = None
                    if(job not in to_make_path):
                        to_make_path.append(job)
                print(to_make_path)
                global path_dict 
                path_dict = path4server.main(to_make_path)
                # print(path_dict)  
    

def acceptThread():
    while True:
        conn, adr = server.accept()
        thread = threading.Thread(target=handleClient,args=(conn,adr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-3}")

def handleClient(conn,adr):
    print(f"[NEW CONNECTION] {adr} connected")
    connected = True
    listening = True
    robot_id = None
    while connected:
        if(listening):
            msg_length = conn.recv(HEADER).decode('utf-8')
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode('utf-8')
                # conn.send("Msg received".encode('utf-8'))
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                else:
                    id,status,x,y = msg.split('|')
                    x = int(x)
                    y = int(y)
                    status = int(status)
                    # print(id,status,x,y)
                    new_agent = Agent(id,x,y,status)
                    for agent in agent_list:
                        if(id==agent.id):
                            agent.updatePosition(x,y)
                            agent.updateStatus(status)
                            # agent.showInfo()
                            break
                    else:
                        agent_list.append(new_agent)
                        robot_id = id
                    if(status==0):
                        listening = False
                    else:
                        listening = True
                print(f"[{adr}] {msg}")
        else:
            global path_dict
            if(len(path_dict)):
                # print(robot_id)
                try:
                    # print(path_dict[robot_id])
                    for agent in agent_list:
                        if(id==agent.id):
                            agent.updateStatus(1)
                            # agent.showInfo()
                            break
                    path = path_dict[robot_id]
                    path_dict.pop(robot_id)
                    path_str = ""
                    for item in path:
                        path_str += str(item[0])+item[1]
                        path_str += ','
                    path_str = path_str[:-1]
                    # print(path_str)
                    conn.send(path_str.encode('utf-8'))
                    listening = True
                except:
                    print("no")

    conn.close()

def start():
    global Grid
    server.listen(5)
    print(f"[LISTENING] Server is listening on {socket.gethostbyname(socket.gethostname())}")
    order_thread = threading.Thread(target=manageOrder)
    order_thread.start()
    listen_thread = threading.Thread(target=acceptThread)
    listen_thread.start()
    plt.ion()
    fig = plot_grid(Grid)
    plt.pause(2)
    while True:
        fig.remove()
        Grid = updateGrid(Grid)
        fig = plot_grid(Grid)   
        plt.pause(0.1)
    

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADR)

print("Server is starting!")
start()

