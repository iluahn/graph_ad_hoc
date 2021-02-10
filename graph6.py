import itertools
import numpy as np
import random
import networkx as nx
import numpy.random as rnd
import matplotlib.pyplot as plt
import re

width  = 16
height = 7
#width  = 7
#height = 8

def random_graph(n, p):
  graph = nx.Graph()
   
  N_range = range(n)
  graph.add_nodes_from(N_range)
   
  for pair in itertools.permutations(N_range, 2):
    if rnd.random() < p:
      graph.add_edge(*pair)
   
  return graph

def RREQ_str(RREQ):
	return str(RREQ[0]) + ", " + str(RREQ[1])+ ", " + str(RREQ[2])+ ", " + str(RREQ[3])

def nodes_connected(u, v, Graph):
	return u in Graph.neighbors(v)

def req(H, src, init_src, dict_nodes, pos, my_nodelist,dst, broadcasted):
	node_labels = {}
	list_adj = list(H.neighbors(src))
	if(init_src != -1):
		list_adj.remove(init_src)
	if not list_adj:
		print("FINISH!\n")
	else:
		for i in list_adj:
			#если пусто  
			if(not (dict_nodes[i])[1]):
				#если не изначальный источник
				if(i != int((dict_nodes[i])[2])):
					(dict_nodes[i])[1] = (dict_nodes[src])[1] + str(i) + ';'
			#проверяем что наименьшее
			else:
				alt_path = (dict_nodes[src])[1] + str(i) + ';'
				alt_path_semi = re.sub('[^;]', '', alt_path)
				init_path_semi = re.sub('[^;]', '', (dict_nodes[i])[1])
				
				if(len(alt_path_semi) < len(init_path_semi)):
					print("ALTERNATIVE PATH")
					(dict_nodes[i])[1] = alt_path
			#отрисовочка
			figure = plt.gcf()
			figure.set_size_inches(width, height)
			plt.cla()
			node_labels.clear()
			for j in range(node_number):
				if(not (dict_nodes[j])[1]):
					node_labels[j] = str(j)
				else:
					node_labels[j] =  str(dict_nodes[j]) +  "\n" + str(j)
			nx.draw(H, pos, node_color='#FAE701', edge_color='#A4A49C', node_size=420, with_labels=False)
			my_nodelist.append(src)
			nx.draw(H, pos, nodelist = my_nodelist, node_color='#F7370E', edge_color='#A4A49C', node_size=420, with_labels=False)
			nx.draw_networkx_labels(H,pos,node_labels,font_size=9)
			plt.pause(0.6)
			#отрисовочка
		broadcasted.append(src)
		for i in list_adj:
			if(i not in broadcasted and i != dst):
				req(H,i,src,dict_nodes, pos, my_nodelist,dst, broadcasted)
				

node_number = 10
print("Enter the number of nodes: ")
node_number = int(input())

#H = random_graph(node_number,0.12)
while(1):
	H = random_graph(node_number,0.12)
	if(nx.is_connected(H) == True):
		break
fixed_nodes = list(H.nodes)
#random_pos0 = nx.random_layout(H)
random_pos0 = nx.kamada_kawai_layout(H)
pos = nx.spring_layout(H, pos = random_pos0.copy(), fixed = fixed_nodes.copy())

#выведем матрицу смежности
print("\nМАТРИЦА СМЕЖНОСТИ:")
print("\n","   |",end='')
for i in H.nodes():
	print("","%2d" % (i), "|", end='')
print("\n")
for i in H.nodes():
	print("", "%2d" %  i, "|", end='')
	for j in H.nodes():
		if(nodes_connected(i,j,H)):
			print("", "%2d" % 1, "|", end='')
		else:
			print("", "%2d" % 0, "|", end='')
	print("\n")
#выведем матрицу смежности	



node_labels = {}
UID = 2
#src = 'A'
#dst = 'B'
src = 0
dst = 2

dict_nodes = {}
RREQ = []




#изначальная отрисовочка
figure = plt.gcf()
figure.set_size_inches(width, height)
nx.draw(H, pos, node_color='#FAE701', edge_color='#A4A49C', node_size=420, with_labels=True)
plt.pause(1.6)
#изначальная отрисовочка

print("Enter source node: ")
src = int(input())
print("Enter destination node: ")
dst = int(input())

#заполняем RREQ
RREQ.append(UID)
RREQ.append("")
RREQ.append(src)
RREQ.append(dst)

for j in range(node_number):
	dict_nodes[j] = RREQ.copy()

my_nodelist = [src,dst]
#чтобы не бродкастить повторно
broadcasted = []
req(H, src, -1, dict_nodes,pos,my_nodelist,dst, broadcasted)

#отрисовываем сам маршрут
#вытаскиваем nodelist маршрута
route_node_list = list(((dict_nodes[dst])[1]).split(";"))
route_node_list.pop(-1)
route_node_list = list(map(int, route_node_list))
route_node_list.insert(0, src)

#вытаскиваем ребра графа
my_edge_list = []
for i in range(len(route_node_list)-1):
	e = route_node_list[i],route_node_list[i+1]
	my_edge_list.append(e)


nx.draw(H, pos, nodelist = route_node_list, edgelist = my_edge_list, width = 2.4 , node_color='#56F52C', edge_color='black', node_size=420, with_labels=False)
plt.pause(0.6)


plt.show()










