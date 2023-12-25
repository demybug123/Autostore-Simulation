import yaml


List_agent = ['agent0','agent1','agent2','agent3']

with open('output.yaml', 'r') as file1:
    with open('input.yaml', 'r') as file2:
        out = yaml.safe_load(file1)
        init = yaml.load(file2, Loader=yaml.FullLoader)
        for i in range(len(List_agent)):
            x=out['schedule'][List_agent[i]][-1]['x']
            y=out['schedule'][List_agent[i]][-1]['y']
            a = (x,y)
            init['agents'][0]['start'] = a
with open('agent.yaml', 'w') as intput_yaml:
    yaml.safe_dump(init['agents'], intput_yaml)
