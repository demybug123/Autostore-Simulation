import yaml
List_even = ['free','come_goods','take_goods','has_goods','receive']
i = {'agent0':0,'agent1':1,'agent2':2,'agent3':3}
def change_even(even):
    if even == 'free':
        return 'come_goods'
    elif even == 'come_goods':
        return 'take_goods'
    elif even == 'take_goods':
        return 'has_goods'
    elif even == 'has_goods':
        return 'receive'
    else:
        print('even problem')
        return 'come_goods'
def main(shortest_agents):
    with open('agent.yaml', 'r') as file2:
        init = yaml.load(file2, Loader=yaml.FullLoader)
        for agent in shortest_agents:
            print(init[0])
            init[i[agent]]['even'] = change_even(init[i[agent]]['even'])
    with open('agent.yaml', 'w') as intput_yaml:
        yaml.safe_dump(init, intput_yaml)