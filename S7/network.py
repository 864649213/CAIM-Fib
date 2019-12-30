from igraph import Graph
from igraph import plot
from IPython import display
from numpy import histogram, max
import matplotlib.pyplot as plt


def task1():
    n = 14      # In the plot of the pdf we have 12 points more or less
    d = n/4     # To have the range [10^-4, 1.0]
    probs = [10**(-i/d) for i in range(n, -1, -1)]

    ccoef0 = -1
    asp0 = -1
    ccoef_list = []
    asp_list = []

    # To calculate the normalized list of clustering coefficient and avarage shortest paths
    # corresponding WS model graphs
    for i in range(0,len(probs)):
        ws = Graph.Watts_Strogatz(1, 5000, 100, probs[i])
        ccoef = ws.transitivity_undirected()
        asp = ws.average_path_length()
        if (ccoef0 == -1):
            ccoef0 = ccoef
        if (asp0 == -1):
            asp0 = asp
        ccoef_list.append(ccoef/ccoef0)
        asp_list.append(asp/asp0)

    plt.plot(probs, ccoef_list, 's', probs, asp_list, 'o')
    plt.xlabel('Prob')
    plt.xscale('log')
    plt.show()


def task2_1():
    g = Graph(directed=False)
    g = g.Load('./edges.txt', format='edgelist', directed=False)
    print("num. edges:", len(g.es()))
    print("num. vertices: ", len(g.vs()))
    print("diameter: ", g.diameter())
    print("transitivity :", g.transitivity_undirected())
    print("degree distr. :", g.degree_distribution())
    print("degree : ", g.degree())
    plot(g, layout = g.layout_kamada_kawai())
    prs = g.pagerank();
    prs = [prs[i]*500 for i in range(0,len(prs))]
    plot(g, vertex_size = prs)

def task2_2():
    g = Graph(directed=False)
    g = g.Load('./edges.txt', format='edgelist', directed=False)
    com = g.community_edge_betweenness()
    comC = com.as_clustering()
    comSizes = comC.sizes()
    print("Size of largest community:", max(comSizes))

    plt.hist(comSizes, rwidth = 0.5)
    plt.ylabel('Number of communities')
    plt.xlabel('Community size')
    plt.show()

    plot(comC, layout = g.layout_kamada_kawai(), orientation='bottom-top')
    print ('Clusters:', com.optimal_count)

if __name__ == "__main__":
    #task1()
    #task2_1()
    task2_2()
