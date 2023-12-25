import yaml

free=0
come_goods=0
take_goods=0
have_goods = 0
receive =0
with open('agent.yaml', 'r') as agents:
    agents = yaml.safe_load(agents)

with open('list_goal.yaml', 'r') as list_goal:
    list_goal = yaml.safe_load(list_goal)

def free():
    List_free=[]
    for agent in agents:
        if agent['even']==free:
            List_free.append(agent)
    new_goal = list_goal[0:len(List_free)]
    list_goal = list_goal

for goal in goals_list:
    # Kiểm tra xem goal có bé hơn dimensions của map không
    if all(0 <= goal[i] <= data['map']['dimensions'][i] for i in range(2)):
        # Kiểm tra xem goal có trùng với obstacles không
        if goal not in data['map']['obstacles']:
            closest_agent = find_closest_agent(data['agents'], goal)

            if closest_agent is not None:
                update_goal(closest_agent, goal)
                print(f"New goal for {closest_agent['name']}: {closest_agent['goal']}")
            else:
                print("All agents already have goals. Choose another goal.")
        else:
            print("Goal coordinates cannot be an obstacle. Please choose another goal.")
    else:
        print("Invalid goal coordinates. Please enter valid coordinates.")


def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def update_goal(agent, new_goal):
    agent['goal'] = new_goal

def find_closest_agent(agents, goal):
    closest_agent = None
    min_distance = float('inf')

    for agent in agents:
        if agent['goal'] is None:
            start = agent['start']
            distance = calculate_distance(start, goal)

            if distance < min_distance:
                min_distance = distance
                closest_agent = agent

    return closest_agent

num_agents = len(data['agents'])