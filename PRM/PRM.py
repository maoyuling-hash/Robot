import math
from PIL import Image
import numpy as np
import networkx as nx
import copy

class RoadMap():
    def __init__(self,img_file):
        test_map = []
        img = Image.open(img_file)
        img_gray = img.convert('L')
        img_arr = np.array(img_gray)
        img_binary = np.where(img_arr<127,0,255)
        for x in range(img_binary.shape[0]):
            temp_row = []
            for y in range(img_binary.shape[1]):
                if img_binary[x,y] == 0:
                    status = '#'
                else:
                    status = '.'
                temp_row.append(status)
            test_map.append(temp_row)
            
        self.map = test_map
        self.cols = len(self.map[0])
        self.rows = len(self.map)
        
    def is_valid_xy(self, x,y):
        if x < 0 or x >= self.rows or y < 0 or y >= self.cols:
            return False
        return True
    
    def EuclidenDistance(self, xy1, xy2):
        dis = 0
        for (x1, x2) in zip(xy1, xy2):
            dis += (x1 - x2)**2
        return dis**0.5

    def check_path(self, xy1, xy2):
        steps = max(abs(xy1[0]-xy2[0]), abs(xy1[1]-xy2[1]))
        xs = np.linspace(xy1[0],xy2[0],steps+1)
        ys = np.linspace(xy1[1],xy2[1],steps+1)
        for i in range(1, steps - 1):
            if not self.map[math.ceil(xs[i])][math.ceil(ys[i])] != '#':
                return False
            if not self.map[math.ceil(xs[i] - 1)][math.ceil(ys[i])] != '#':
                return False
            if not self.map[math.ceil(xs[i])][math.ceil(ys[i] - 1)] != '#':
                return False
            
        return True

    def plot(self,path):
        out = []
        for x in range(self.rows):
            temp = []
            for y in range(self.cols):
                if self.map[x][y]=='#':
                    temp.append(0)
                elif self.map[x][y]=='.':
                    temp.append(255)
                elif self.map[x][y]=='*':
                    temp.append(255)
                else:
                    temp.append(255)
            out.append(temp)
        for x,y in path:
            out[x][y] = 0
            out[x][y - 1] = 0
            out[x - 1][y] = 0
            if x + 1 < self.rows - 1:
                out[x + 1][y] = 0
            if y + 1 < self.cols - 1:
                out[x][y + 1] = 0
        out = np.array(out)
        img = Image.fromarray(np.uint8(out))
        img.show()



class PRM(RoadMap):
    def __init__(self, img_file, **param):
        RoadMap.__init__(self,img_file)
        if 'num_sample' in param:
            self.num_sample = param['num_sample']
        else:
            self.num_sample = 100
        if 'distance_neighbor' in param:
            self.distance_neighbor = param['distance_neighbor']
        else:
            self.distance_neighbor = 100
        self.G = nx.Graph()
        
    def learn(self):
        while len(self.G.nodes)<self.num_sample:
            XY = (np.random.randint(0, self.rows),np.random.randint(0, self.cols))
            if self.is_valid_xy(XY[0],XY[1]) and self.map[XY[0]][XY[1]] != '#':
                self.G.add_node(XY)
        for node1 in self.G.nodes:
            for node2 in self.G.nodes:
                if node1==node2:
                    continue
                dis = self.EuclidenDistance(node1,node2)
                if dis<self.distance_neighbor and self.check_path(node1,node2):
                    self.G.add_edge(node1,node2,weight=dis)
    
    def find_path(self,startXY=None,endXY=None):
        temp_G = copy.deepcopy(self.G)
        startXY = tuple(startXY) if startXY else (self.rows-65,30)
        endXY = tuple(endXY) if endXY else (60, self.cols-65)
        temp_G.add_node(startXY)
        temp_G.add_node(endXY)
        for node1 in [startXY, endXY]:
            for node2 in temp_G.nodes:
                dis = self.EuclidenDistance(node1,node2)
                if dis < self.distance_neighbor and self.check_path(node1,node2):
                    temp_G.add_edge(node1,node2,weight=dis)
        path = nx.shortest_path(temp_G, source=startXY, target=endXY)
        
        return self.construct_path(path)

    def construct_path(self, path):
        out = []
        for i in range(len(path)-1):
            xy1,xy2=path[i],path[i+1]
            steps = max(abs(xy1[0]-xy2[0]), abs(xy1[1]-xy2[1]))
            xs = np.linspace(xy1[0],xy2[0],steps+1)
            ys = np.linspace(xy1[1],xy2[1],steps+1)
            for j in range(0, steps+1):
                out.append((math.ceil(xs[j]), math.ceil(ys[j])))
        return out
        
        
if __name__ == '__main__':

    prm = PRM('maz.png',num_sample=500,distance_neighbor=200)
    prm.learn()
    path = prm.find_path()
    prm.plot(path)

