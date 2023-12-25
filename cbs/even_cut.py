import yaml

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data

def find_shortest_agents(schedule):
    shortest_agents = []
    shortest_length = float('inf')

    for agent, path in schedule.items():
        if len(path) < shortest_length:
            shortest_agents = [agent]
            shortest_length = len(path)
        elif len(path) == shortest_length:
            shortest_agents.append(agent)

    return shortest_agents, shortest_length

def save_yaml(file_path, data):
    with open(file_path, 'w') as file:
        yaml.dump(data, file)

def equalize_agents(schedule):
    shortest_agents, shortest_length = find_shortest_agents(schedule)

    for agent, path in schedule.items():
        if len(path) > shortest_length:
            schedule[agent] = path[:shortest_length]

    return schedule,shortest_agents
def main():
    file_path = "output.yaml"
    data = load_yaml(file_path)
    equalized_schedule,shortest_agents = equalize_agents(data['schedule'])
    save_yaml(file_path, {"cost": data['cost'], "schedule": equalized_schedule})
    return shortest_agents
main()