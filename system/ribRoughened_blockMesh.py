# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
# Joseph B. Tipton, Jr.
# 7/19/2019
#
# Python script to create a blockMeshDict file for meshing in OpenFOAM.
# Creates a rib-roughened channel matching experiments of Wang & Sunden.
#
# VERSION HISTORY:
#
# v2 --> Fixed block vertice definitions to start at a consistent origin
#    --> Defined interior interfaces between blocks with duplicate vertices
# v3 --> 10/27/2019
#    --> Split the upperWall and lowerWall into 3 regions
#    --> Added mesh refinement at the top
# v4 --> 12/17/2019
#    --> Split lower wall into 2 named sections for ribs and flat wall
# v5 --> 12/30/2019
#    --> Changed mesh grading to inflate around the ribs
#    --> Broke apart file.write statements to make mesh grading more readable
# v6 --> 12/30/2019
#    --> Created mesh density variables to use for eventual mesh refinement studies
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------

import numpy as np

#
# Set geometry variables
#

Dh = 50         # hydraulic diameter
e = 0.1*Dh      # rib height
P = 12*e        # rib spacing
segments = 12   # number of rib segments
outlet = 5*Dh   # length of outlet segment
inlet = 750     # length of inlet segment

#
# Set mesh density variables
#

P_x = 79	# number of cells in between ribs (x-dir)
e_span = 72     # number of cells spanning a rib (x & y-dir)
D_y = 66        # number of cells spanning channel (y-dir)

#
# Create file header
#

file1 = open("blockMeshDict","w+")

header = ["FoamFile \n", 
          "{\n", 
          "    version    2.0;\n",
          "    format     ascii;\n",
          "    class      dictionary;\n",
          "    object     blockMeshDict;\n"
          "}\n",
          "\n",
          "scale   0.001;\n",
          "\n"]
file1.writelines(header)


# ------------------------------------------------------------------------------------
# WRITE VERTICES ---------------------------------------------------------------------
# ------------------------------------------------------------------------------------

file1.write("vertices\n(\n")

# Rib-roughened segments
for n in range(0,segments):
    file1.write("    (  {}  0  -0.5)\n".format(e+n*P))
    file1.write("    (  {}  0  -0.5)\n".format(P+n*P))
    file1.write("    (  {}  {}  -0.5)\n".format(P+n*P,e))
    file1.write("    (  {}  {}  -0.5)\n".format(P+n*P,Dh))
    file1.write("    (  {}  {}  -0.5)\n".format(e+n*P,Dh))
    file1.write("    (  {}  {}  -0.5)\n".format(0+n*P,Dh))
    file1.write("    (  {}  {}  -0.5)\n".format(0+n*P,e))
    file1.write("    (  {}  {}  -0.5)\n\n".format(e+n*P,e))
    
    file1.write("    (  {}  0   0.5)\n".format(e+n*P))
    file1.write("    (  {}  0   0.5)\n".format(P+n*P))
    file1.write("    (  {}  {}   0.5)\n".format(P+n*P,e))
    file1.write("    (  {}  {}   0.5)\n".format(P+n*P,Dh))
    file1.write("    (  {}  {}   0.5)\n".format(e+n*P,Dh))
    file1.write("    (  {}  {}   0.5)\n".format(0+n*P,Dh))
    file1.write("    (  {}  {}   0.5)\n".format(0+n*P,e))
    file1.write("    (  {}  {}   0.5)\n\n".format(e+n*P,e))

# Outlet segment
file1.write("    (  {}  0  -0.5)\n".format(0+segments*P))
file1.write("    (  {}  0  -0.5)\n".format(outlet+segments*P))
file1.write("    (  {}  {}  -0.5)\n".format(outlet+segments*P,e))
file1.write("    (  {}  {}  -0.5)\n".format(outlet+segments*P,Dh))
file1.write("    (  {}  {}  -0.5)\n".format(0+segments*P,Dh))
file1.write("    (  {}  {}  -0.5)\n\n".format(0+segments*P,e))

file1.write("    (  {}  0   0.5)\n".format(0+segments*P))
file1.write("    (  {}  0   0.5)\n".format(outlet+segments*P))
file1.write("    (  {}  {}   0.5)\n".format(outlet+segments*P,e))
file1.write("    (  {}  {}   0.5)\n".format(outlet+segments*P,Dh))
file1.write("    (  {}  {}   0.5)\n".format(0+segments*P,Dh))
file1.write("    (  {}  {}   0.5)\n\n".format(0+segments*P,e))

# Inlet segment
file1.write("    (  {}  0  -0.5)\n".format(-1*inlet))
file1.write("    (  {}  0  -0.5)\n".format(0))
file1.write("    (  {}  {}  -0.5)\n".format(0,e))
file1.write("    (  {}  {}  -0.5)\n".format(0,Dh))
file1.write("    (  {}  {}  -0.5)\n".format(-1*inlet,Dh))
file1.write("    (  {}  {}  -0.5)\n\n".format(-1*inlet,e))

file1.write("    (  {}  0   0.5)\n".format(-1*inlet))
file1.write("    (  {}  0   0.5)\n".format(0))
file1.write("    (  {}  {}   0.5)\n".format(0,e))
file1.write("    (  {}  {}   0.5)\n".format(0,Dh))
file1.write("    (  {}  {}   0.5)\n".format(-1*inlet,Dh))
file1.write("    (  {}  {}   0.5)\n\n".format(-1*inlet,e))

file1.write(");\n\n")

# ------------------------------------------------------------------------------------
# WRITE BLOCKS -----------------------------------------------------------------------
# ------------------------------------------------------------------------------------

file1.write("blocks\n(\n")

# Rib-roughened segments
file1.write("    // Block 0 then 1 then 2 for each segment\n")

block0  = np.array([0,1,2,7,8,9,10,15])
blockI  = np.array([7,2,3,4,15,10,11,12])
blockII = np.array([6,7,4,5,14,15,12,13])

for n in range(0,segments-1):
    file1.write("    hex ({i[0]} {i[1]} {i[2]} {i[3]} {i[4]} {i[5]} {i[6]} {i[7]})\n".format(i=block0+16*n))
    file1.write("    ({i} {j} 1)\n".format(i=P_x,j=e_span))
    file1.write("    simpleGrading (\n")
    file1.write("         ((0.125 0.25 8)(0.75 0.5 1)(0.125 0.25 0.125))\n")
    file1.write("         1\n")
    file1.write("         1\n")
    file1.write("    )\n\n")

    file1.write("    hex ({i[0]} {i[1]} {i[2]} {i[3]} {i[4]} {i[5]} {i[6]} {i[7]})\n".format(i=blockI+16*n))
    file1.write("    ({i} {j} 1)\n".format(i=P_x,j=D_y))
    file1.write("    simpleGrading (\n")
    file1.write("         ((0.125 0.25 8)(0.75 0.5 1)(0.125 0.25 0.125))\n")
    file1.write("         ((0.125 0.25 8)(0.75 0.50 1)(0.125 0.25 0.125))\n")
    file1.write("         1\n")
    file1.write("    )\n\n")

    file1.write("    hex ({i[0]} {i[1]} {i[2]} {i[3]} {i[4]} {i[5]} {i[6]} {i[7]})\n".format(i=blockII+16*n))
    file1.write("    ({i} {j} 1)\n".format(i=e_span,j=D_y))
    file1.write("    simpleGrading (\n")
    file1.write("         1\n")
    file1.write("         ((0.125 0.25 8)(0.75 0.50 1)(0.125 0.25 0.125))\n")
    file1.write("         1\n")
    file1.write("    )\n\n")

n = segments-1
file1.write("    hex ({i[0]} {i[1]} {i[2]} {i[3]} {i[4]} {i[5]} {i[6]} {i[7]})\n".format(i=block0+16*n))
file1.write("    ({i} {j} 1)\n".format(i=P_x,j=e_span))
file1.write("    simpleGrading (\n")
file1.write("         ((0.125 0.25 8)(0.875 0.75 1))\n")
file1.write("         1\n")
file1.write("         1\n")
file1.write("    )\n\n")

file1.write("    hex ({i[0]} {i[1]} {i[2]} {i[3]} {i[4]} {i[5]} {i[6]} {i[7]})\n".format(i=blockI+16*n))
file1.write("    ({i} {j} 1)\n".format(i=P_x,j=D_y))
file1.write("    simpleGrading (\n")
file1.write("         ((0.125 0.25 8)(0.875 0.75 1))\n")
file1.write("         ((0.125 0.25 8)(0.75 0.50 1)(0.125 0.25 0.125))\n")
file1.write("         1\n")
file1.write("    )\n\n")

file1.write("    hex ({i[0]} {i[1]} {i[2]} {i[3]} {i[4]} {i[5]} {i[6]} {i[7]})\n".format(i=blockII+16*n))
file1.write("    ({i} {j} 1)\n".format(i=e_span,j=D_y))
file1.write("    simpleGrading (\n")
file1.write("         1\n")
file1.write("         ((0.125 0.25 8)(0.75 0.50 1)(0.125 0.25 0.125))\n")
file1.write("         1\n")
file1.write("    )\n\n")



# Outlet segment
block0  = np.array([0,1,2,5,6,7,8,11])
blockI  = np.array([5,2,3,4,11,8,9,10])

file1.write("    hex ({i[0]} {i[1]} {i[2]} {i[3]} {i[4]} {i[5]} {i[6]} {i[7]})\n".format(i=block0+16*segments))
file1.write("    (40 {i} 1)\n".format(i=e_span))
file1.write("    simpleGrading (\n")
file1.write("         8\n")
file1.write("         1\n")
file1.write("         1\n")
file1.write("    )\n\n")

file1.write("    hex ({i[0]} {i[1]} {i[2]} {i[3]} {i[4]} {i[5]} {i[6]} {i[7]})\n".format(i=blockI+16*segments))
file1.write("    (40 {i} 1)\n".format(i=D_y))
file1.write("    simpleGrading (\n")
file1.write("         8\n")
file1.write("         ((0.125 0.25 8)(0.75 0.50 1)(0.125 0.25 0.125))\n")
file1.write("         1\n")
file1.write("    )\n\n")



# Inlet segment
block0  = np.array([0,1,2,5,6,7,8,11])
blockI  = np.array([5,2,3,4,11,8,9,10])

file1.write("    hex ({i[0]} {i[1]} {i[2]} {i[3]} {i[4]} {i[5]} {i[6]} {i[7]})\n".format(i=block0+16*segments+12))
file1.write("    (160 {i} 1)\n".format(i=e_span))
file1.write("    simpleGrading (\n")
file1.write("         0.125\n")
file1.write("         1\n")
file1.write("         1\n")
file1.write("    )\n\n")

file1.write("    hex ({i[0]} {i[1]} {i[2]} {i[3]} {i[4]} {i[5]} {i[6]} {i[7]})\n".format(i=blockI+16*segments+12))
file1.write("    (160 {i} 1)\n".format(i=D_y))
file1.write("    simpleGrading (\n")
file1.write("         0.125\n")
file1.write("         ((0.125 0.25 8)(0.75 0.50 1)(0.125 0.25 0.125))\n")
file1.write("         1\n")
file1.write("    )\n\n")



file1.write(");\n\n")

# ------------------------------------------------------------------------------------
# WRITE EDGES ------------------------------------------------------------------------
# ------------------------------------------------------------------------------------

file1.write("edges\n(\n);\n\n")

# ------------------------------------------------------------------------------------
# WRITE BOUNDARIES -------------------------------------------------------------------
# ------------------------------------------------------------------------------------

file1.write("boundary\n(\n")

# Inlet
face1 = np.array([4,5,11,10])
face2 = np.array([5,0,6,11])

file1.write("    inlet\n    {\n        type patch;\n        faces\n        (\n")
file1.write("            ({i[0]} {i[1]} {i[2]} {i[3]})\n".format(i=face1+16*segments+12))
file1.write("            ({i[0]} {i[1]} {i[2]} {i[3]})\n".format(i=face2+16*segments+12))
file1.write("        );\n    }\n\n")


# Outlet
face1 = np.array([1,2,8,7])
face2 = np.array([2,3,9,8])

file1.write("    outlet\n    {\n        type patch;\n        faces\n        (\n")
file1.write("            ({i[0]} {i[1]} {i[2]} {i[3]})\n".format(i=face1+16*segments))
file1.write("            ({i[0]} {i[1]} {i[2]} {i[3]})\n".format(i=face2+16*segments))
file1.write("        );\n    }\n\n")


# Upper Wall Inlet
file1.write("    upperWallInlet\n    {\n        type wall;\n        faces\n        (\n")

face3 = np.array([3,4,10,9])
file1.write("            ({i[0]} {i[1]} {i[2]} {i[3]})\n".format(i=face3+16*segments+12))

file1.write("        );\n    }\n\n")


# Upper Wall Ribs
file1.write("    upperWallRibs\n    {\n        type wall;\n        faces\n        (\n")

face1 = np.array([3,4,12,11])
face2 = np.array([4,5,13,12])
file1.write("            ({i[0]} {i[1]} {i[2]} {i[3]})\n".format(i=face1))
file1.write("            ({i[0]} {i[1]} {i[2]} {i[3]})\n".format(i=face2))

face1 = np.array([3,4,12,11])
face2 = np.array([4,5,13,12])
for n in range(1,segments):
    file1.write("            ({i[0]} {i[1]} {i[2]} {i[3]})\n".format(i=face1+16*n))
    file1.write("            ({i[0]} {i[1]} {i[2]} {i[3]})\n".format(i=face2+16*n))

file1.write("        );\n    }\n\n")


# Upper Wall Outlet
file1.write("    upperWallOutlet\n    {\n        type wall;\n        faces\n        (\n")

face3 = np.array([3,4,10,9])
file1.write("            ({i[0]} {i[1]} {i[2]} {i[3]})\n".format(i=face3+16*segments))

file1.write("        );\n    }\n\n")


# Lower Wall Inlet
file1.write("    lowerWallInlet\n    {\n        type wall;\n        faces\n        (\n")

face5 = np.array([0,1,7,6])
file1.write("            ({i[0]} {i[1]} {i[2]} {i[3]})\n".format(i=face5+16*segments+12))

file1.write("        );\n    }\n\n")


# Lower Wall Ribbed Section - Ribs
file1.write("    lowerWallRibs1\n    {\n        type wall;\n        faces\n        (\n")

face6 = np.array([2,1,7,8])
file1.write("            ({i[0]} {i[1]} {i[2]} {i[3]})\n".format(i=face6+16*segments+12))

face1 = np.array([6,7,15,14])
face2 = np.array([7,0,8,15])
face4 = np.array([1,2,10,9])
for n in range(0,segments):
    file1.write("            ({i[0]} {i[1]} {i[2]} {i[3]})\n".format(i=face1+16*n))
    file1.write("            ({i[0]} {i[1]} {i[2]} {i[3]})\n".format(i=face2+16*n))
    if n != segments-1:
         file1.write("            ({i[0]} {i[1]} {i[2]} {i[3]})\n".format(i=face4+16*n))

file1.write("        );\n    }\n\n")


# Lower Wall Ribbed Section - Flat Wall
file1.write("    lowerWallRibs2\n    {\n        type wall;\n        faces\n        (\n")

face3 = np.array([0,1,9,8])

for n in range(0,segments):
    file1.write("            ({i[0]} {i[1]} {i[2]} {i[3]})\n".format(i=face3+16*n))

file1.write("        );\n    }\n\n")


# Lower Wall Outlet
file1.write("    lowerWallOutlet\n    {\n        type wall;\n        faces\n        (\n")

face5 = np.array([0,1,7,6])
file1.write("            ({i[0]} {i[1]} {i[2]} {i[3]})\n".format(i=face5+16*segments))
file1.write("        );\n    }\n\n")


# Front
file1.write("    front\n    {\n        type empty;\n        faces\n        (\n")

face1 = np.array([10,11,12,15])
face2 = np.array([12,13,14,15])
face3 = np.array([8,9,10,15])
for n in range(0,segments):
    file1.write("            ({i[0]} {i[1]} {i[2]} {i[3]})\n".format(i=face1+16*n))
    file1.write("            ({i[0]} {i[1]} {i[2]} {i[3]})\n".format(i=face2+16*n))
    file1.write("            ({i[0]} {i[1]} {i[2]} {i[3]})\n".format(i=face3+16*n))

face4 = np.array([8,9,10,11])
face5 = np.array([7,8,11,6])
file1.write("            ({i[0]} {i[1]} {i[2]} {i[3]})\n".format(i=face4+16*segments))
file1.write("            ({i[0]} {i[1]} {i[2]} {i[3]})\n".format(i=face5+16*segments))
file1.write("            ({i[0]} {i[1]} {i[2]} {i[3]})\n".format(i=face4+16*segments+12))
file1.write("            ({i[0]} {i[1]} {i[2]} {i[3]})\n".format(i=face5+16*segments+12))

file1.write("        );\n    }\n\n")


# Back
file1.write("    back\n    {\n        type empty;\n        faces\n        (\n")

face1 = np.array([4,3,2,7])
face2 = np.array([7,2,1,0])
face3 = np.array([5,4,7,6])
for n in range(0,segments):
    file1.write("            ({i[0]} {i[1]} {i[2]} {i[3]})\n".format(i=face1+16*n))
    file1.write("            ({i[0]} {i[1]} {i[2]} {i[3]})\n".format(i=face2+16*n))
    file1.write("            ({i[0]} {i[1]} {i[2]} {i[3]})\n".format(i=face3+16*n))

face4 = np.array([5,4,3,2])
face5 = np.array([0,5,2,1])
file1.write("            ({i[0]} {i[1]} {i[2]} {i[3]})\n".format(i=face4+16*segments))
file1.write("            ({i[0]} {i[1]} {i[2]} {i[3]})\n".format(i=face5+16*segments))
file1.write("            ({i[0]} {i[1]} {i[2]} {i[3]})\n".format(i=face4+16*segments+12))
file1.write("            ({i[0]} {i[1]} {i[2]} {i[3]})\n".format(i=face5+16*segments+12))

file1.write("        );\n    }\n\n")


# Rib-roughened segment interfaces

face1 = np.array([2,3,11,10])
face2 = np.array([21,22,30,29])
for n in range(0,segments-1):
    file1.write("    Interface{}Left\n".format(n))
    file1.write("    {\n        type wall;\n        faces\n        (\n")
    file1.write("            ({i[0]} {i[1]} {i[2]} {i[3]})\n".format(i=face1+16*n))
    file1.write("        );\n    }\n\n")

    file1.write("    Interface{}Right\n".format(n))
    file1.write("    {\n        type wall;\n        faces\n        (\n")
    file1.write("            ({i[0]} {i[1]} {i[2]} {i[3]})\n".format(i=face2+16*n))
    file1.write("        );\n    }\n\n")


# Inlet segment interface

face1  = np.array([2,3,9,8])+16*segments+12
file1.write("    InterfaceInletLeft\n    {\n        type patch;\n        faces\n        (\n")
file1.write("            ({i[0]} {i[1]} {i[2]} {i[3]})\n".format(i=face1))
file1.write("        );\n    }\n\n")

face2  = np.array([5,6,14,13])
file1.write("    InterfaceInletRight\n    {\n        type patch;\n        faces\n        (\n")
file1.write("            ({i[0]} {i[1]} {i[2]} {i[3]})\n".format(i=face2))
file1.write("        );\n    }\n\n")


# Outlet segment interface

face1  = np.array([4,5,11,10])+16*segments
face2  = np.array([5,0,6,11])+16*segments
file1.write("    InterfaceOutletLeft\n    {\n        type patch;\n        faces\n        (\n")
file1.write("            ({i[0]} {i[1]} {i[2]} {i[3]})\n".format(i=face1))
file1.write("            ({i[0]} {i[1]} {i[2]} {i[3]})\n".format(i=face2))
file1.write("        );\n    }\n\n")

face1  = np.array([2,3,11,10])+16*(segments-1)
face2  = np.array([1,2,10,9])+16*(segments-1)
file1.write("    InterfaceOutletRight\n    {\n        type patch;\n        faces\n        (\n")
file1.write("            ({i[0]} {i[1]} {i[2]} {i[3]})\n".format(i=face1))
file1.write("            ({i[0]} {i[1]} {i[2]} {i[3]})\n".format(i=face2))
file1.write("        );\n    }\n\n")


# Close boundary section
file1.write(");\n\n")




# ------------------------------------------------------------------------------------
# WRITE MERGE PATCH PAIRS ------------------------------------------------------------
# ------------------------------------------------------------------------------------

file1.write("mergePatchPairs\n(\n\n")

# Rib-roughened segment interfaces
for n in range(0,segments-1):
    file1.write("    ( Interface{}Left Interface{}Right )\n".format(n,n))

# Inlet segment interface
file1.write("    ( InterfaceInletLeft InterfaceInletRight )\n")

# Outlet segment interface
file1.write("    ( InterfaceOutletLeft InterfaceOutletRight )\n")

file1.write(");\n\n")

# ------------------------------------------------------------------------------------
# CLOSE FILE -------------------------------------------------------------------------
# ------------------------------------------------------------------------------------

file1.close()

