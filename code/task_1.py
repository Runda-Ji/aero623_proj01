# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 10:34:03 2019

@author: rundaji
"""

# mesh = {'nNode':nNode, 'nElem':nElem, 'node_pos':node_pos, 'nBGroup':nBGroup, 'boundary':boundary, 'Elems':E, 'nEdge': 0, 'Edges':[]};

from my_class import BOUNDARY,CELL
import numpy as np
import matplotlib.pyplot as plt

def set_boundaries(nBGroup,nNode,node_pos):
    Nx = 20;
    Ny = 2;
    boundary = [None]*nBGroup;
    # Bottom
    B = [None]*Nx;
    j = 0;
    for i in range(0,Nx+1):
        x = -1.5 + i/Nx*3;
        if x > 0:
            x = x**1.5/1.5**0.5;
        else:
            x = -(-x)**1.5/1.5**0.5;
        y = 0.0625*np.exp(-25*x**2);
        node_pos.append([x,y]);
        if j + 1 <= Nx:
            B[j] = {'n0': nNode, 'n1': nNode + 1};
            j = j + 1;
        nNode = nNode + 1;
    boundary[0] = BOUNDARY(Nx, 2, 'Bottom', B);

    # Right
    B = [None]*Ny;
    j = 0;
    for i in range(0,Ny):
        x = 1.5;
        y = 0.8*(i+1)/Ny;
        node_pos.append([x,y]);
        if j + 1 <= Ny:
            B[j] = {'n0': nNode-1, 'n1': nNode};
            j = j + 1;
        nNode = nNode + 1;
    boundary[1] = BOUNDARY(Ny, 2, 'Right', B);
    
    # Top
    Nx_top = int(Nx*0.3);
    B = [None]*Nx_top;
    j = 0;
    for i in range(0,Nx_top):
        x = 1.5 - (i+1)/Nx_top*3;
        y = 0.8;
        node_pos.append([x,y]);
        if j + 1 <= Nx_top:
            B[j] = {'n0': nNode-1, 'n1': nNode};
            j = j + 1;
        nNode = nNode + 1;
    boundary[2] = BOUNDARY(Nx_top, 2, 'Top', B);
    
    #Left
    B = [None]*Ny;
    j = 0;
    for i in range(0,Ny-1):
        x = -1.5;
        y = 0.8 - 0.8*(i+1)/Ny;
        node_pos.append([x,y]);
        if j + 1 <= Ny-1:
            B[j] = {'n0': nNode-1, 'n1': nNode};
            j = j + 1;
        nNode = nNode + 1;
    B[j] = {'n0': nNode-1, 'n1': 0};
    boundary[3] = BOUNDARY(Ny, 2, 'Left', B);
    return nNode, boundary;

def write_geo_file(nBGroup,boundary,node_pos):
    f = open("..\\mesh\\task_1.geo", "w");
    f.write('//GEO FILE FOR GMSH \n');
    f.close;
    f = open("..\\mesh\\task_1.geo", "a");
    for i in range (0,nBGroup):
        for j in range(0,boundary[i].nBFace):
            n0 = boundary[i].B[j]['n0'];
            n1 = boundary[i].B[j]['n1'];
            x0 = node_pos[n0,0];
            y0 = node_pos[n0,1];
            f.write('Point(%d) = {%f, %f, 0, %f};\n' %(n0+1,x0,y0,3));
    line_no = 1;
    for i in range (0,nBGroup):
        for j in range(0,boundary[i].nBFace):
            n0 = boundary[i].B[j]['n0'];
            n1 = boundary[i].B[j]['n1'];
            f.write('Line(%d) = {%d, %d};\n' %(line_no,n0+1,n1+1));
            line_no = line_no + 1;
    f.write('Curve Loop(1) = {');
    for i in range(0,line_no - 2):
        f.write('%d,'%(i+1));
    f.write('%d};\n'%(line_no-1));
    f.write('Plane Surface(1) = {1};\n');
    f.close;
    return 0;

def read_msh_file(fname,nNode_boundary,node_pos):
    f = open("..\\mesh\\task_1.msh", "r");
    line = f.readline();
    #--------------------------------------------------------------------------
    while (line != '$Nodes\n'):
        line = f.readline();
    line = f.readline();
    [numEntityBlocks,numNodes_total] = [int(item) for item in line.split()];
    for i in range(0,numEntityBlocks):
        line = f.readline();
        [tagEntity, dimEntity, parametric, numNodes] = [int(item) for item in line.split()];
        for j in range(0,numNodes):
            line = f.readline();
            item = line.split();
            tag = int(item[0])-1;
            if tag >= nNode_boundary:
                x = float(item[1]);
                y = float(item[2]);
                node_pos = np.append(node_pos,[[x,y]],axis=0);
    #--------------------------------------------------------------------------
    while (line != '$Elements\n'):
        line = f.readline();
    line = f.readline();
    [numEntityBlocks, numElements] = [int(item) for item in line.split()];
    for i in range(0,numEntityBlocks):
        line = f.readline();
        [tagEntity, dimEntity, typeEle, numElements] = [int(item) for item in line.split()];
        for j in range(0,numElements):
            line = f.readline();
            item = line.split();
            tag =  int(item[0]);
            if tag == 2*nNode_boundary:
                break;
        if tag == 2*nNode_boundary:
            break;
    line = f.readline();            
    [tagEntity, dimEntity, typeEle, numElements] = [int(item) for item in line.split()];
    E = [None]*numElements;
    for i in range(0,numElements):
            line = f.readline();
            [tag,n0,n1,n2] = [int(item) for item in line.split()];
            tri = tag - 2*nNode_boundary - 1;
            E[tri] = CELL([n0-1,n1-1,n2-1], None, tri, None, None, None, None, None);
    f.close;
    return numNodes_total,numElements,node_pos,E;

def plot_boundary(node_pos,folder,title):
    x = node_pos[:,0];
    x = np.append(x,x[0]);
    y = node_pos[:,1];
    y = np.append(y,y[0]);
    f1 = plt.figure(figsize=([15,4]));
    plt.plot(x,y,'k.-');
    plt.axis('equal');
    plt.grid();
    plt.savefig('..\\%s\\%s.pdf' %(folder,title),dpi=150);
    plt.close(f1);
    return 0;

def plot_mesh(mesh,folder,title):
    x = mesh['node_pos'][:,0];
    y = mesh['node_pos'][:,1];
    tri = [None]*mesh['nElem'];
    for i in range(0,mesh['nElem']):
        tri[i] = mesh['Elems'][i].vertex;
    tri = np.asarray(tri);
    f1 = plt.figure(figsize=([15,4]));
    plt.triplot(x, y, tri, 'k-', lw=0.5);
    plt.axis('equal');
    plt.savefig('..\\%s\\%s.pdf' %(folder,title),dpi=150);
    plt.close(f1);
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
            node_0 = edge['n0'] + 1; #the index start from 1
            node_1 = edge['n1'] + 1; #the index start from 1
            file.write('%d %d\n' %(node_0, node_1));
    file.write('%d %d %s\n' %(mesh['nElem'],1,'triangles'));
    for i in range(0,mesh['nElem']):
        elem = mesh['Elems'][i];
        v0,v1,v2 = elem.vertex;
        v0 = v0 + 1; v1 = v1 + 1; v2 = v2 + 1;
        file.write('%d %d %d\n' %(v0,v1,v2));
    file.close();
    return 0;

def main():
    global mesh;
    nBGroup = 4;
    nNode = 0;
    node_pos = [];
    #--------------------------------------------------------------------------
    [nNode,boundary] = set_boundaries(nBGroup,nNode,node_pos);
    node_pos = np.asarray(node_pos);
    plot_boundary(node_pos,'figure','boundary_bump0');
    write_geo_file(nBGroup,boundary,node_pos);
    [nNode,nElem,node_pos,E] = read_msh_file('task_1.msh',nNode,node_pos); 
    mesh = {'nNode':nNode, 'nElem':nElem, 'node_pos':node_pos, 'nBGroup':nBGroup, 'boundary':boundary, 'Elems':E, 'nEdge': 0, 'Edges':[]};
    plot_mesh(mesh,'figure','mesh_bump0');
    write_gri_file(mesh,'mesh','bump0');
    return 0;

if __name__=="__main__":
    main()