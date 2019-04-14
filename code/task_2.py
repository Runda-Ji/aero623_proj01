# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 09:02:16 2019

@author: runda
"""

from read_gri import read_gri
from pre_calculation import pre_calculation

def write_edge_info(mesh,folder,fname):
    I2E = [];
    B2E_Bottom = [];
    B2E_Right = [];
    B2E_Top = [];
    B2E_Left = [];
    In = [];
    Bn_Bottom = [];
    Bn_Right = [];
    Bn_Top = [];
    Bn_Left = [];
    for i in range(0,mesh['nEdge']):
        elemL = mesh['Edges'][i].t1;
        faceL = mesh['Edges'][i].e1;
        elemR = mesh['Edges'][i].t2;
        faceR = mesh['Edges'][i].e2;
        norm_vec = mesh['Edges'][i].norm_vec;
        norm_vec = norm_vec.tolist();
        if type(faceR) == int:
            I2E.append([elemL+1,faceL+1,elemR+1,faceR+1]);
            In.append(norm_vec);
        else:
            if faceR == 'Bottom':
                B2E_Bottom.append([elemL+1,faceL+1,faceR]);
                Bn_Bottom.append(norm_vec);
            if faceR == 'Right':
                B2E_Right.append([elemL+1,faceL+1,faceR]);
                Bn_Right.append(norm_vec);
            if faceR == 'Top':
                B2E_Top.append([elemL+1,faceL+1,faceR]);
                Bn_Top.append(norm_vec);
            if faceR == 'Left':
                B2E_Left.append([elemL+1,faceL+1,faceR]);
                Bn_Left.append(norm_vec);
    B2E = B2E_Bottom + B2E_Right + B2E_Top + B2E_Left;
    Bn = Bn_Bottom + Bn_Right + Bn_Top + Bn_Left;
    #--------------------------------------------------------------------------
    file = open('..\\%s\\%s_I2E.txt' %(folder,fname), 'w');
    for i in range(0,len(I2E)):
        file.write('%d %d %d %d\n' %(I2E[i][0],I2E[i][1],I2E[i][2],I2E[i][3]));
    file.close();
    
    file = open('..\\%s\\%s_B2E.txt' %(folder,fname), 'w');
    for i in range(0,len(B2E)):
        file.write('%d %d %s\n' %(B2E[i][0],B2E[i][1],B2E[i][2]));
    file.close();
    
    file = open('..\\%s\\%s_In.txt' %(folder,fname), 'w');
    for i in range(0,len(In)):
        file.write('%f %f\n' %(In[i][0],In[i][1]));
    file.close();
    
    file = open('..\\%s\\%s_Bn.txt' %(folder,fname), 'w');
    for i in range(0,len(Bn)):
        file.write('%f %f\n' %(Bn[i][0],Bn[i][1]));
    file.close();
    return 0;

def write_cell_info(mesh,folder,fname):
    file = open('..\\%s\\%s_Area.txt' %(folder,fname), 'w');
    for i in range(0,mesh['nElem']):
        file.write('%f\n' %(mesh['Elems'][i].A));
    file.close(); 
    return 0;

def main():
    global mesh;
    mesh = read_gri('..\\mesh\\bump0.gri');
    pre_calculation(mesh);
    write_edge_info(mesh,'data','bump0');
    write_cell_info(mesh,'data','bump0');
    mesh = read_gri('..\\mesh\\test.gri');
    pre_calculation(mesh);
    write_edge_info(mesh,'data','test');
    write_cell_info(mesh,'data','test');
    return 0;

if __name__=="__main__":
    main()