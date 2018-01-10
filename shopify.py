import urllib.request
import json
import copy
from pprint import pprint

valid = True

class Node:
    def __init__(self, id, data, parent_id, child_ids):
        self.id = id
        self.data = data
        self.parent_id = parent_id
        self.child_ids = child_ids

def search(currentNode, nodes, visited):
    if currentNode in visited:
        global valid
        valid = False
        return visited
    children = [node for node in nodes if node.id in currentNode.child_ids]
    visited.add(currentNode)
    all_visited = copy.copy(visited)
    for child in children:
        all_visited.update(search(child, nodes, copy.copy(visited)))
    return all_visited

def convertJsonToArray(data):
    arr = []
    for node in data:
        arr.append(Node(node['id'], node['data'], node['parent_id'] if 'parent_id' in node else None, set(node['child_ids'])))
    return arr

def processData(data):
    roots = [node for node in data if node.parent_id is None]
    response = {'valid_menus': [], 'invalid_menus': []}
    for node in roots:
        visited = set([])
        global valid
        valid = True
        visistedNodes = list(map(lambda node: node.id, search(node, data, copy.copy(visited))))
        if valid == False:
            response['invalid_menus'].append({'root_id' : node.id, 'children' : visistedNodes})
        else:
            visistedNodes.remove(node.id)
            response['valid_menus'].append({'root_id': node.id, 'children': visistedNodes})
    return json.dumps(response)

def main():
    for id in range(1, 3):
        currentNumberOfNodes = 0
        totalNodes = 0
        page = 1
        allData = []
        while currentNumberOfNodes <= totalNodes:
            data = urllib.request.urlopen("https://backend-challenge-summer-2018.herokuapp.com/challenges.json?id=" + str(id) + "&page=" + str(page)).read()
            currentNumberOfNodes += json.loads(data)["pagination"]["per_page"]
            totalNodes = json.loads(data)["pagination"]["total"]
            page += 1
            jsonData = json.loads(data)["menus"]
            allData.extend(convertJsonToArray(jsonData))
        pprint(processData(allData))

if __name__ == "__main__":
    main()




