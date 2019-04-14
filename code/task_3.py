# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 12:16:41 2019

@author: rundaji
"""

from read_gri import read_gri
from pre_calculation import pre_calculation
import numpy as np
import matplotlib.pyplot as plt

def verification_test(mesh):
    #empty R for all cells
    for i in range(0,mesh['nElem']):
        mesh['Elems'][i].R = np.array([0.0,0.0]);
    for i in range(0,mesh['nEdge']):
        edge = mesh['Edges'][i];
        n = edge.norm_vec;
        delta_l = edge.length;
        if type(edge.e2) == int:
            #for interior cells, e2 is an integer
            t1 = edge.t1;
            t2 = edge.t2;
            mesh['Elems'][t1].R = mesh['Elems'][t1].R + n*delta_l;
            mesh['Elems'][t2].R = mesh['Elems'][t2].R - n*delta_l;
        else:
            t = edge.t1;
            mesh['Elems'][t].R = mesh['Elems'][t].R + n*delta_l;
    R_max = 0;
    for i in range(0,mesh['nElem']):
        Rx = mesh['Elems'][i].R[0];
        Ry = mesh['Elems'][i].R[1];
        mesh['Elems'][i].R = np.sqrt(Rx**2 + Ry**2);
        if mesh['Elems'][i].R > R_max:
            R_max = mesh['Elems'][i].R;
    return R_max;

def plot_R(mesh,folder,title,fsize):
    x = mesh['node_pos'][:,0];
    y = mesh['node_pos'][:,1];
    tri = [None]*mesh['nElem'];
    R = [None]*mesh['nElem'];
    for i in range(0,mesh['nElem']):
        tri[i] = mesh['Elems'][i].vertex;
        R[i] = mesh['Elems'][i].R;
    tri = np.asarray(tri);
    f1 = plt.figure(figsize=(fsize));
    plt.tripcolor(x, y, tri, R, edgecolors='k', linewidth=0.0, cmap=plt.cm.jet);
    plt.axis('equal');
    plt.colorbar();
    plt.savefig('..\\%s\\%s.pdf' %(folder,title),dpi=150);
    plt.close(f1);
    return 0;

def main():
    global mesh, R_max_bump0, R_max_test;
    mesh = read_gri('..\\mesh\\bump0.gri');
    pre_calculation(mesh);
    R_max_bump0 = verification_test(mesh);
    plot_R(mesh,'figure','R_bump0',[15,4]);
    mesh = read_gri('..\\mesh\\test.gri');
    pre_calculation(mesh);
    R_max_test = verification_test(mesh);
    plot_R(mesh,'figure','R_test',[5,5]);
    
    return 0;

if __name__=="__main__":
    main()