# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 23:38:47 2019

@author: runda
"""

from  my_class import EDGE, CELL
from read_gri import read_gri
from pre_calculation import pre_calculation
import numpy as np
import matplotlib.pyplot as plt
from task_1 import plot_mesh
from task_3 import verification_test, plot_R

def split_edge(mesh):    
    nEdge_old = mesh['nEdge'];
    new_nodes = [None]*nEdge_old;
    new_edges = [None]*nEdge_old;
    for i in range(0,nEdge_old):
        edge = mesh['Edges'][i];
        x0,y0 = mesh['node_pos'][edge.node_0];
        x1,y1 = mesh['node_pos'][edge.node_1];
        midpt_pos = np.array([0.5*(x0+x1),0.5*(y0+y1)]);
        #correct the midpt position for lower boundary
        if edge.e2 == 'Bottom':
            midpt_pos[1] = 0.0625*np.exp(-25*midpt_pos[0]**2);
        #add the midpt to current list
        mesh['node_pos'] = np.append(mesh['node_pos'], [midpt_pos], axis = 0);
        new_node_no = mesh['nNode'];
        mesh['nNode'] = mesh['nNode'] + 1;
        new_nodes[i] = new_node_no;
        #split the edge            
        new_edge_0 = EDGE(edge.node_0, new_node_no, None, None, None, None, None, None, None);
        new_edge_1 = EDGE(new_node_no, edge.node_1, None, None, None, None, None, None, None);
        mesh['Edges'][i] = new_edge_0; # replace the current edge with edge0
        mesh['Edges'].append(new_edge_1); # append the edge1
        new_edge_no = mesh['nEdge'];
        mesh['nEdge'] = mesh['nEdge'] + 1;
        new_edges[i] = {'new_edge_0': i, 'new_edge_1': new_edge_no};
    return new_nodes,new_edges;

def split_elem(mesh,new_nodes):
    nElem_old = mesh['nElem'];
    for i in range(0,nElem_old):
        edge_splitted = [];
        cell = mesh['Elems'][i];
        state = cell.state;
        for j in range(0,3):
            global_edge_no = cell.edge[j];
            edge_splitted.append({'loc_edge': j, 'new_node_no': new_nodes[global_edge_no]});

        loc_v0 = edge_splitted[0]['loc_edge']; #v0 = 0
        loc_v1 = edge_splitted[1]['loc_edge']; #v0 = 0
        loc_v2 = edge_splitted[2]['loc_edge']; #v0 = 0
        global_v0 = cell.vertex[loc_v0];
        global_v1 = cell.vertex[loc_v1];
        global_v2 = cell.vertex[loc_v2];
        new_node_no_0 = edge_splitted[0]['new_node_no'];
        new_node_no_1 = edge_splitted[1]['new_node_no'];
        new_node_no_2 = edge_splitted[2]['new_node_no'];
        new_edge_0 = EDGE(new_node_no_0, new_node_no_1, None, None, None, None, None, None, None);
        new_edge_1 = EDGE(new_node_no_1, new_node_no_2, None, None, None, None, None, None, None);
        new_edge_2 = EDGE(new_node_no_2, new_node_no_0, None, None, None, None, None, None, None);
        new_tri_0 = CELL([global_v0, new_node_no_2, new_node_no_1], None, None, None, state, None, None, None);
        new_tri_1 = CELL([new_node_no_2, global_v1, new_node_no_0], None, None, None, state, None, None, None);
        new_tri_2 = CELL([new_node_no_2, new_node_no_0, new_node_no_1], None, None, None, state, None, None, None);
        new_tri_3 = CELL([new_node_no_1, new_node_no_0, global_v2], None, None, None, state, None, None, None);
        mesh['Edges'].append(new_edge_0);
        mesh['Edges'].append(new_edge_1);
        mesh['Edges'].append(new_edge_2);
        mesh['nEdge'] = mesh['nEdge'] + 3;
        mesh['Elems'][i] = new_tri_0;
        mesh['Elems'].append(new_tri_1);
        mesh['Elems'].append(new_tri_2);
        mesh['Elems'].append(new_tri_3);
        mesh['nElem'] = mesh['nElem'] + 3;
    return 0;
#
def split_boundary(mesh,new_edges):
    for i in range(0,mesh['nBGroup']):
        nBFace_old = mesh['boundary'][i].nBFace;
        for j in range(0,nBFace_old):
            global_edge_no = mesh['boundary'][i].B[j];
            new_edge = new_edges[global_edge_no]['new_edge_1'];
            mesh['boundary'][i].B.append(new_edge);
            mesh['boundary'][i].nBFace = mesh['boundary'][i].nBFace + 1;
    return 0;

def refine(mesh):
    global new_nodes,new_edges;
    [new_nodes,new_edges] = split_edge(mesh);
    split_boundary(mesh,new_edges);
    split_elem(mesh,new_nodes);
    return 0;

def write_gri_file(mesh,folder,title):
    file = open('..\\%s\\%s.gri' %(folder,title), 'w');
    file.write('%d %d %d\n' %(mesh['nNode'],mesh['nElem'],2));
    for i in range(0,mesh['nNode']):
        pos = mesh['node_pos'][i];
        file.write('%f %f\n' %(pos[0], pos[1]));
    file.write('%d\n' %(mesh['nBGroup']));
    for i in range(0,mesh['nBGroup']):
        file.write('%d %d %s\n' %(mesh['boundary'][i].nBFace, mesh['boundary'][i].nf, mesh['boundary'][i].Title));
        for j in range(0,mesh['boundary'][i].nBFace):
            edge = mesh['boundary'][i].B[j];
            node_0 = mesh['Edges'][edge].node_0 + 1; #the index start from 1
            node_1 = mesh['Edges'][edge].node_1 + 1; #the index start from 1
            file.write('%d %d\n' %(node_0, node_1));
    file.write('%d %d %s\n' %(mesh['nElem'],1,'triangles'));
    for i in range(0,mesh['nElem']):
        elem = mesh['Elems'][i];
        v0,v1,v2 = elem.vertex;
        v0 = v0 + 1; v1 = v1 + 1; v2 = v2 + 1;
        file.write('%d %d %d\n' %(v0,v1,v2));
    file.close();
    return 0;

def plot_R_max(R_max_bump):
    x = np.linspace(1, 4, num=4);
    y = R_max_bump[1:5];
    f1, ax = plt.subplots(figsize=([9,15]));
    ax.semilogy(x, y,'-*');
    ax.grid();
    ax.yaxis.set_ticks(np.arange(5e-18,3e-17,2e-18))
    ax.set_xticks([1,2,3,4]);
    ax.set_xticklabels(['bump1','bump2','bump3','bump4']);
    plt.xlabel('Mesh');
    plt.ylabel('Maximum Residual');
    plt.savefig('..\\figure\\R_vs_iter.pdf',dpi=150);
    #plt.close(f1);
    return 0;

def main():
    global mesh,R_max_bump;
    Nrefine = 5;
    R_max_bump = [None]*Nrefine;    
    for i in range(0,Nrefine):
        mesh = read_gri('..\\mesh\\bump%d.gri' %i);
        pre_calculation(mesh);
        R_max_bump[i] = verification_test(mesh);
        plot_R(mesh,'figure','R_bump%d' %i,[15,4]);        
        refine(mesh);
        plot_mesh(mesh,'figure','mesh_bump%d' %(i+1));
        write_gri_file(mesh,'mesh','bump%d'%(i+1));
    plot_R_max(R_max_bump);
    return 0;

if __name__=="__main__":
    main()