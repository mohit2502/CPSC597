#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 16:30:34 2021
Updated on Sat April 24 17:50:36 2021
@author: mohit_kumar@csu.fullerton.edu
"""

####################################################
from email.parser import HeaderParser
import networkx as nx
import matplotlib.pyplot as plt
import collections
import tarfile
import networkx.algorithms.community.centrality as cen
import itertools

# person of interest
poi = {
    'albert.meyers@enron.com', 'a..martin@enron.com', 'andrea.ring@enron.com', 'andrew.lewis@enron.com',
    'andy.zipper@enron.com', 'a..shankman@enron.com', 'barry.tycholiz@enron.com', 'benjamin.rogers@enron.com',
    'bill.rapp@enron.com', 'bill.williams@enron.com', 'brad.mckay@enron.com', 'brenda.whitehead@enron.com',
    'b..sanders@enron.com', 'cara.semperger@enron.com', 'c..giron@enron.com', 'charles.weldon@enron.com',
    'chris.dorland	@enron.com', 'chris.germany@enron.com', 'clint.dean@enron.com', 'cooper.richey@enron.com',
    'craig.dean@enron.com', 'dana.davis@enron.com', 'dan.hyvl@enron.com', 'danny.mccarty@enron.com',
    'daren.farmer@enron.com', 'darrell.schoolcraft@enron.com', 'darron.giron@enron.com', 'david.delainey@enron.com',
    'debra.bailey@enron.com', 'debra.perlingiere@enron.com', 'diana.scholtes@enron.com', 'd..martin@enron.com',
    'don.baughman@enron.com', 'drew.fossum@enron.com', 'd..steffes@enron.com', 'd..thomas@enron.com',
    'dutch.quigley@enron.com', 'e..haedicke@enron.com', 'elizabeth.sager@enron.com', 'eric.bass@enron.com',
    'eric.saibi@enron.com', 'errol.mclaughlin@enron.com', 'e.taylor@enron.com', 'f..brawner@enron.com',
    'f..campbell@enron.com', 'f..keavey@enron.com', 'fletcher.sturm@enron.com', 'frank.ermis@enron.com',
    'geir.solberg@enron.com', 'geoff.storey@enron.com', 'gerald.nemec@enron.com', 'greg.whalley@enron.com',
    'gretel.smith@enron.com', 'harry.arora@enron.com', 'h..lewis@enron.com', 'holden.salisbury@enron.com',
    'hunter.shively@enron.com', 'james.derrick@enron.com', 'james.steffes@enron.com', 'jane.tholt@enron.com',
    'jason.williams@enron.com', 'jason.wolfe@enron.com', 'jay.reitmeyer@enron.com', 'jeff.dasovich@enron.com',
    'jeff.king@enron.com', 'jeffrey.hodge@enron.com', 'jeffrey.shankman@enron.com', 'jeff.skilling@enron.com',
    'j..farmer@enron.com', 'j.harris@enron.com', 'jim.schwieger@enron.com', 'j..kaminski@enron.com',
    'j.kaminski@enron.com', 'j..kean@enron.com', 'joannie.williamson@enron.com', 'joe.parks@enron.com',
    'joe.quenet@enron.com', 'joe.stepenovitch@enron.com', 'john.arnold@enron.com', 'john.forney@enron.com',
    'john.griffith@enron.com', 'john.hodge@enron.com', 'john.lavorato@enron.com', 'john.zufferli@enron.com',
    'jonathan.mckay@enron.com', 'j..sturm@enron.com', 'juan.hernandez@enron.com', 'judy.hernandez@enron.com',
    'judy.townsend@enron.com', 'k..allen@enron.com', 'kam.keiser@enron.com', 'kate.symes@enron.com',
    'kay.mann@enron.com', 'keith.holst@enron.com', 'kenneth.lay@enron.com', 'kevin.hyatt@enron.com',
    'kevin.presto@enron.com', 'kevin.ruscitti@enron.com', 'kimberly.watson@enron.com', 'kim.ward@enron.com',
    'larry.campbell@enron.com', 'larry.may@enron.com', 'l..gay@enron.com', 'lindy.donoho@enron.com',
    'lisa.gang@enron.com', 'liz.taylor@enron.com', 'l..mims@enron.com', 'louise.kitchen@enron.com',
    'lynn.blair@enron.com', 'margaret.carson@enron.com', 'marie.heard@enron.com', 'mark.e.haedicke@enron.com',
    'mark.haedicke@enron.com', 'mark.mcconnell@enron.com', 'mark.taylor@enron.com', 'mark.whitt@enron.com',
    'martin.cuilla@enron.com', 'mary.fischer@enron.com', 'matthew.lenhart@enron.com', 'matt.motley@enron.com',
    'matt.smith@enron.com', 'm..forney@enron.com', 'michele.lokay@enron.com', 'michelle.cash@enron.com',
    'michelle.lokay@enron.com', 'mike.carson@enron.com', 'mike.grigsby@enron.com', 'mike.maggi@enron.com',
    'mike.mcconnell@enron.com', 'mike.swerzbin@enron.com', 'm..love@enron.com', 'monika.causholli@enron.com',
    'monique.sanchez@enron.com', 'm..presto@enron.com', 'm..scott@enron.com', 'm..smith@enron.com',
    'm..tholt@enron.com', 'patrice.mims@enron.com', 'paul.thomas@enron.com', 'pete.davis@enron.com',
    'peter.keavey@enron.com', 'phillip.allen@enron.com', 'phillip.love@enron.com', 'phillip.platter@enron.com',
    'randall.gay@enron.com', 'richard.ring@enron.com', 'richard.sanders@enron.com', 'richard.shapiro@enron.com',
    'rick.buy@enron.com', 'robert.badeer@enron.com', 'robert.benson@enron.com', 'rob.gay@enron.com',
    'rod.hayslett@enron.com', 'ryan.slinger@enron.com', 'sally.beck@enron.com', 'sandra.brawner@enron.com',
    'sara.shackleton@enron.com', 'scott.hendrickson@enron.com', 'scott.neal@enron.com', 'shelley.corman@enron.com',
    's..shively@enron.com', 'stacy.dickson@enron.com', 'stanley.horton@enron.com', 'stephanie.panus@enron.com',
    'steven.kean@enron.com', 'steven.south@enron.com', 'susan.bailey@enron.com', 'susan.pereira@enron.com',
    'susan.scott@enron.com', 's..ward@enron.com', 'tana.jones@enron.com', 'teb.lokey@enron.com',
    'theresa.staab@enron.com', 't..hodge@enron.com', 'thomas.martin@enron.com', 't..lucci@enron.com',
    'tom.donohoe@enron.com', 'tori.kuykendall@enron.com', 'tracy.geaccone@enron.com', 'vince.kaminski@enron.com',
    'vladi.pimenov@enron.com', 'v.weldon@enron.com', 'w..delainey@enron.com', 'w..pereira@enron.com',
    'w..white@enron.com'
}

# path of the enron dataset
fullpath = "./"
zipfile = "enron_mail_20150507.tar.gz"

save_path = "./"
png_dump = save_path + "path.png"
hist_dump = save_path + "hist.png"
G_dump = save_path + "graph.pickle"
G_dump_poi = save_path + "poi_graph.pickle"

# create a graph variable
# G = nx.DiGraph()

# list for storing external emails
external_email_id = []

# emails of interest count
eoi = 100


def plot_hist(G):
    to_plot = []
    for key, value in G.degree().items():
        to_plot.append(value)

    degreeCount = collections.Counter(to_plot)
    deg, cnt = zip(*degreeCount.items())

    fig, ax = plt.subplots()
    plt.bar(deg, cnt, width=0.35, color='b')

    plt.title("Degree Histogram")
    plt.ylabel("Count")
    plt.xlabel("Degree")

    # draw graph in inset
    plt.axes([0.4, 0.4, 0.5, 0.5])
    plt.axis('off')
    plt.savefig(hist_dump)
    plt.show()


G_poi = nx.DiGraph()


def make_email_graph(G, graph_node):
    for n, item in enumerate(graph_node):
        if 0 == n:
            src = item
            if src in poi:
                # print("SRC in POI : ", src)
                G_poi.add_node(src)

        G.add_node(item)

        dst = item
        if (src == dst):
            continue

        if G.has_edge(src, dst):
            param = G.get_edge_data(src, dst, 'weight')
            wt = param['weight'] + 1
            G.add_edge(src, dst, weight=wt)
        else:
            G.add_edge(src, dst, weight=1)

        if src in poi and dst in poi:
            # print("DST in POI : ", dst)
            if G_poi.has_edge(src, dst):
                param = G_poi.get_edge_data(src, dst, 'weight')
                wt = param['weight'] + 1
                G_poi.add_edge(src, dst, weight=wt)
            else:
                G_poi.add_edge(src, dst, weight=1)


def strip_split(x):
    x = x.replace(',', '')
    x = x.replace('<', '')
    x = x.replace('>', '')
    x = x.split()
    return x


def add_node_ext(t, x_id, gn):
    graph_node = gn.copy()
    if None != x_id:
        x_id = strip_split(x_id)
        for x in x_id:
            if ("From" == t):
                graph_node.insert(0, x)
            else:
                graph_node.append(x)
    return graph_node


def add_node(t, x_id, gn):
    graph_node = gn.copy()
    if None != x_id:
        x_id = strip_split(x_id)
        for x in x_id:
            if 'enron.com' in str(x) or 'enron.net' in str(x):
                if ("From" == t):
                    graph_node.insert(0, x)
                else:
                    graph_node.append(x)
            else:
                print("EXT EMAIL [", t, "] : ", x)
                external_email_id.append(x)
    return graph_node


def open_parse_email(G, tar, tarinfo):
    f = tar.extractfile(tarinfo)
    # few mails are of utf-8 and some are other formats (just workaround)
    # FIXME: Is there a better way to handle all formats ?
    try:
        whole_line = f.read().decode('utf-8')
    except:
        whole_line = f.read().decode('us-ascii')

    p = HeaderParser()
    h = p.parsestr(whole_line)

    # read header information from individual emails
    from_id = h['From']
    to_id = h['To']
    cc_id = h['Cc']
    bcc_id = h['Bcc']

    # list to store the graph nodes which will be created by from, to. cc, bcc
    # member of this list is added to the graph
    graph_node = []

    # enable/disable the inclusion of extermal mails in graph creation
    include_external_mail = False

    # include external email ids in graph creation
    if True == include_external_mail:
        graph_node = add_node_ext("FROM", from_id, graph_node)
        graph_node = add_node_ext("TO", to_id, graph_node)
        graph_node = add_node_ext("CC", cc_id, graph_node)
        graph_node = add_node_ext("BCC", bcc_id, graph_node)
    # DO NOT include external email ids in graph creation
    else:
        graph_node = add_node("FROM", from_id, graph_node)
        graph_node = add_node("TO", to_id, graph_node)
        graph_node = add_node("CC", cc_id, graph_node)
        graph_node = add_node("BCC", bcc_id, graph_node)
    # make the graph from the nodes
    make_email_graph(G, graph_node)


def graph_stats(G):
    print("NODES : ", G.number_of_nodes())
    print("EDGES : ", G.number_of_edges())


# apply the degree centrality and display the top (eoi) members
def apply_degree_centrality(G):
    print(" ================================================================================")
    print("|                             Applying DEGREE CENTRALITY ...                     |")
    print(" ================================================================================")
    counter = 0
    max_counter = eoi
    dcen = nx.degree_centrality(G)
    for dc in sorted(dcen.items(), key=lambda r: -r[1]):
        if counter <= max_counter:
            counter += 1
        else:
            counter = 0
            break
        is_poi = False
        for x in poi:
            if x in str(dc):
                print("POI : ", dc)
                is_poi = True
        if False == is_poi:
            print(dc)


# apply the page rank and display the top (eoi) members
def apply_page_rank(G):
    print(" ================================================================================")
    print("|                               Applying PAGE RANK ...                           |")
    print(" ================================================================================")
    counter = 0
    max_counter = eoi
    prank = nx.pagerank(G)
    for pr in sorted(prank.items(), key=lambda r: -r[1]):
        if counter <= max_counter:
            counter += 1
        else:
            counter = 0
            break

        is_poi = False
        for x in poi:
            if x in str(pr):
                print("POI : ", pr)
                is_poi = True
        if False == is_poi:
            print(pr)


# apply the edge centrality and display the top (eoi) members
def apply_edge_centrality(G):
    print(" ================================================================================")
    print("|                             Applying EDGE CENTRALITY ...                       |")
    print(" ================================================================================")
    counter = 0
    max_counter = eoi
    eb = nx.edge_betweenness_centrality(G)
    # print("edge betweenness centrality = ", eb)

    for e in sorted(eb.items(), key=lambda r: -r[1]):
        if counter <= max_counter:
            counter += 1
        else:
            counter = 0
            break
        is_poi = False
        for x in poi:
            if x in str(e):
                print("POI : ", e)
                is_poi = True
        if False == is_poi:
            print(e)


# apply the hubs and authorities and display the top (eoi) members
def apply_hits(G):
    print(" ================================================================================")
    print("|                               Applying HITS ...                                |")
    print(" ================================================================================")
    counter = 0
    max_counter = eoi

    hub, auth = nx.hits(G)
    print(" ================================================================================")
    print("|                                   HUBS                                         |")
    print(" ================================================================================")
    for hb in sorted(hub.items(), key=lambda r: -r[1]):
        if counter <= max_counter:
            counter += 1
        else:
            counter = 0
            break
        is_poi = False
        for x in poi:
            if x in str(hb):
                print("POI : ", hb)
                is_poi = True
        if False == is_poi:
            print(hb)

    counter = 0
    max_counter = eoi
    print(" ================================================================================")
    print("|                                AUTHORITIES                                     |")
    print(" ================================================================================")
    for au in sorted(auth.items(), key=lambda r: -r[1]):
        if counter <= max_counter:
            counter += 1
        else:
            counter = 0
            break
        is_poi = False
        for x in poi:
            if x in str(au):
                print("POI : ", au)
                is_poi = True
        if False == is_poi:
            print(au)


# apply the degree centrality and display the top (eoi) members
def apply_girvan_newman(G):
    print(" ================================================================================")
    print("|                             Applying GIRVAN NEWMAN ...                         |")
    print(" ================================================================================")

    comp = cen.girvan_newman(G)
    #    print(tuple(sorted(c) for c in next(comp)))
    #    tup = (tuple(sorted(c) for c in next(comp)))
    #    for t in tup:
    #        print(t)

    cmt = itertools.takewhile(lambda c: len(c) <= 100, comp)
    for communities in cmt:
        x = tuple(sorted(c) for c in communities)

    id_dict = {}
    for i in range(len(x)):
        print("Printining community : ", i)
        print(x[i])
        if len(x[i]) >= 2:
            for xx in x[i]:
                id_dict[xx] = i

    values = [id_dict.get(node, 0.25) for node in G.nodes()]
    nx.draw(G, cmap=plt.get_cmap('jet'), node_color=values, with_labels=True)
    plt.show()

    return G_poi


def process_graph(G, pd):
    apply_degree_centrality(G)
    apply_page_rank(G)
    apply_edge_centrality(G)
    apply_hits(G)

    apply_girvan_newman(G)

    print("\nPreparing Graph statistics ...\n")
    graph_stats(G)

    # print("External Email Ids :")
    # print(str(external_email_id))

    # print("Creating networkx graph ...")
    # nx.draw_networkx(G, with_labels=True)
    # plt.show()

    # when the graph is created freshly from mails
    if False == pd:
        print("\ndumping pickle graph ...")
        nx.write_gpickle(G, G_dump)
        print("dumping pickle graph done !!!")

    # nx.draw_networkx(nx.read_gpickle(G_dump), with_labels=False)
    # plt.show()


#        print("\ndumping poi pickle graph ...")
#        nx.write_gpickle(G_poi, G_dump_poi)
#        print("dumping poi pickle graph done !!!")

# print("Graph Degree : ", G.degree())
# print("Creating degree vs Count Histogram ...")
# plot_hist()

# this function reads the tar file as a whole avoids individual
# file read from the disk makes it pretty faster
def read_tar(G):
    counter = 0
    tar = tarfile.open(zipfile)
    for tarinfo in tar:
        if tarinfo.isreg():
            print(counter, tarinfo.name)
            counter += 1
            open_parse_email(G, tar, tarinfo)
    tar.close()


# this is used for showing more debug information
def read_tar_debug(G):
    counter = 0
    tar = tarfile.open(zipfile)
    for tarinfo in tar:
        # print( tarinfo.name, "is", tarinfo.size, "bytes in size and is")
        if tarinfo.isreg():
            print(counter, tarinfo.name)  # , " : a regular file.")
            counter += 1
            # open_parse_new(tar, tarinfo)
            open_parse_email(G, tar, tarinfo)
            # print("graph_node = ", str(graph_node))
            nop = 0  # nop = no operation
        elif tarinfo.isdir():
            nop = 1
            # print( "a directory.")
        else:
            if nop == 0:
                nop = 1
            # print( "something else.")
        if counter >= 10:
            break
    tar.close()


def modify_graph(G_enron):
    for edge in G_enron.edges():
        param = G_enron.get_edge_data(edge[0], edge[1], 'weight')
        if (param['weight'] < 50):
            G_enron.remove_edge(edge[0], edge[1])
    nds = G_enron.degree()
    for key, items in nds.items():
        if (items == 0):
            G_enron.remove_node(key)
    return G_enron


def make_poi_graph(G):
    # create a new poi graph
    G_poi = nx.DiGraph()

    for src, dst in G.edges():
        if src in poi and dst in poi:
            # print("[ ", src, ", ", dst, "]")
            G_poi.add_edge(src, dst)

    #    print("\ndumping poi pickle graph ...")
    #    nx.write_gpickle(G_poi, G_dump_poi)
    #    print("dumping poi pickle graph done !!!")

    #    nx.draw_networkx(G_poi, with_labels=True)
    #    plt.show()
    return G_poi


def start_new():
    # enable this to dump logs in file
    # import sys
    # sys.stdout = open("logs.txt", "w")

    # check if the pickle dump file is read or all emails are read
    G = nx.DiGraph()
    try:
        G = nx.read_gpickle(G_dump)

        # pickle dump read flag : true when the pickle graph is read from disk
        pd_read = True
    except:
        print("\nNo valid pickle dump found, reading all mails")
        pd_read = False

    # print(G)
    if (0 == G.number_of_nodes()):
        read_tar(G)
        # read_tar_debug(G)
    else:
        print("\n**************************** Warning !!! *******************************")
        print("Found previous pickle dump file [graph.pickle]")
        print("delete 'graph.pickle' manually if you want to parse all mails again\n")

    #    G_mod = modify_graph(G)
    #    process_graph(G_mod, pickle_dump_read)

    # process_graph(G, pd_read)
    G_poi = make_poi_graph(G)
    process_graph(G_poi, pd_read)

    # nx.draw_networkx(nx.read_gpickle(G_dump_poi), with_labels=True)
    # plt.show()


start_new()