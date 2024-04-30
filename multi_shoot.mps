NAME multi_shoot
ROWS
 N  OBJ
 E  R0      
 E  R1      
 E  dynamics[0][0,0]
 E  dynamics[0][1,0]
 E  dynamics[1][0,0]
 E  dynamics[1][1,0]
 E  dynamics[2][0,0]
 E  dynamics[2][1,0]
 E  dynamics[3][0,0]
 E  dynamics[3][1,0]
 E  dynamics[4][0,0]
 E  dynamics[4][1,0]
 E  dynamics[5][0,0]
 E  dynamics[5][1,0]
 E  dynamics[6][0,0]
 E  dynamics[6][1,0]
 E  dynamics[7][0,0]
 E  dynamics[7][1,0]
 E  dynamics[8][0,0]
 E  dynamics[8][1,0]
 E  dynamics[9][0,0]
 E  dynamics[9][1,0]
COLUMNS
    x[0,0]    R0        1
    x[0,0]    dynamics[0][0,0]  -1
    x[0,1]    dynamics[0][0,0]  1
    x[0,1]    dynamics[1][0,0]  -1
    x[0,2]    dynamics[1][0,0]  1
    x[0,2]    dynamics[2][0,0]  -1
    x[0,3]    dynamics[2][0,0]  1
    x[0,3]    dynamics[3][0,0]  -1
    x[0,4]    dynamics[3][0,0]  1
    x[0,4]    dynamics[4][0,0]  -1
    x[0,5]    dynamics[4][0,0]  1
    x[0,5]    dynamics[5][0,0]  -1
    x[0,6]    dynamics[5][0,0]  1
    x[0,6]    dynamics[6][0,0]  -1
    x[0,7]    dynamics[6][0,0]  1
    x[0,7]    dynamics[7][0,0]  -1
    x[0,8]    dynamics[7][0,0]  1
    x[0,8]    dynamics[8][0,0]  -1
    x[0,9]    dynamics[8][0,0]  1
    x[0,9]    dynamics[9][0,0]  -1
    x[0,10]   dynamics[9][0,0]  1
    x[1,0]    R1        1
    x[1,0]    dynamics[0][1,0]  -0.5
    x[1,1]    dynamics[0][1,0]  1
    x[1,1]    dynamics[1][1,0]  -0.5
    x[1,2]    dynamics[1][1,0]  1
    x[1,2]    dynamics[2][1,0]  -0.5
    x[1,3]    dynamics[2][1,0]  1
    x[1,3]    dynamics[3][1,0]  -0.5
    x[1,4]    dynamics[3][1,0]  1
    x[1,4]    dynamics[4][1,0]  -0.5
    x[1,5]    dynamics[4][1,0]  1
    x[1,5]    dynamics[5][1,0]  -0.5
    x[1,6]    dynamics[5][1,0]  1
    x[1,6]    dynamics[6][1,0]  -0.5
    x[1,7]    dynamics[6][1,0]  1
    x[1,7]    dynamics[7][1,0]  -0.5
    x[1,8]    dynamics[7][1,0]  1
    x[1,8]    dynamics[8][1,0]  -0.5
    x[1,9]    dynamics[8][1,0]  1
    x[1,9]    dynamics[9][1,0]  -0.5
    x[1,10]   dynamics[9][1,0]  1
    u[0,0]    dynamics[0][1,0]  -1
    u[0,1]    dynamics[1][1,0]  -1
    u[0,2]    dynamics[2][1,0]  -1
    u[0,3]    dynamics[3][1,0]  -1
    u[0,4]    dynamics[4][1,0]  -1
    u[0,5]    dynamics[5][1,0]  -1
    u[0,6]    dynamics[6][1,0]  -1
    u[0,7]    dynamics[7][1,0]  -1
    u[0,8]    dynamics[8][1,0]  -1
    u[0,9]    dynamics[9][1,0]  -1
RHS
BOUNDS
QUADOBJ
    x[0,0]    x[0,0]    2
    x[0,1]    x[0,1]    2
    x[0,2]    x[0,2]    2
    x[0,3]    x[0,3]    2
    x[0,4]    x[0,4]    2
    x[0,5]    x[0,5]    2
    x[0,6]    x[0,6]    2
    x[0,7]    x[0,7]    2
    x[0,8]    x[0,8]    2
    x[0,9]    x[0,9]    2
    x[0,10]   x[0,10]   2
    x[1,0]    x[1,0]    2
    x[1,1]    x[1,1]    2
    x[1,2]    x[1,2]    2
    x[1,3]    x[1,3]    2
    x[1,4]    x[1,4]    2
    x[1,5]    x[1,5]    2
    x[1,6]    x[1,6]    2
    x[1,7]    x[1,7]    2
    x[1,8]    x[1,8]    2
    x[1,9]    x[1,9]    2
    x[1,10]   x[1,10]   2
    u[0,0]    u[0,0]    2
    u[0,1]    u[0,1]    2
    u[0,2]    u[0,2]    2
    u[0,3]    u[0,3]    2
    u[0,4]    u[0,4]    2
    u[0,5]    u[0,5]    2
    u[0,6]    u[0,6]    2
    u[0,7]    u[0,7]    2
    u[0,8]    u[0,8]    2
    u[0,9]    u[0,9]    2
ENDATA
