from z3 import *
import sys
from itertools import combinations

info = []
with open(sys.argv[1]) as f:
#with open("inp3.txt") as f:
	for line in f:
		info.append([int(v) for v in line.strip().split(',')])

n,k = info[0]
k -= 1
red = info[1]
vertical = []
horizontal = []
mines = []
ver = [[0 for i in range(n)] for j in range(n)]
hor = [[0 for i in range(n)] for j in range(n)]
mn = [[0 for i in range(n)] for j in range(n)]
re = [[0 for i in range(n)] for j in range(n)]

def eo(a,b,c):
	return Or(And(a,Not(b),Not(c)), And(b,Not(c),Not(a)), And(c,Not(a),Not(b)))

for i in range(2,len(info)):
	if info[i][0] == 0:
		vertical.append(info[i][1:])
	elif info[i][0] == 1:
		horizontal.append(info[i][1:])
	else :
		mines.append(info[i][1:])

for ind in vertical:
	ver[ind[0]][ind[1]]=1
for ind in horizontal:
	hor[ind[0]][ind[1]]=1
for ind in mines:
	mn[ind[0]][ind[1]]=1
re[red[0]][red[1]]=1

# declaring prop variables
v = [[[ Bool("v_%s_%s_%s" % (m,i,j)) for j in range(n)] for i in range(n)] for m in range(k+1)]
h = [[[ Bool("h_%s_%s_%s" % (m,i,j)) for j in range(n)] for i in range(n)] for m in range(k+1)]
r = [[[ Bool("r_%s_%s_%s" % (m,i,j)) for j in range(n)] for i in range(n)] for m in range(k+1)]
mns = [[ Bool("mns_%s_%s" % (i,j)) for j in range(n)] for i in range(n)]

for i in range(n):
	for j in range(n):
		v[0][i][j]==True

# movement-0 initialise
move_0v = [ If(ver[i][j]==1, v[0][i][j]==True, v[0][i][j]==False) for i in range(n) for j in range(n)]
move_0h = [ If(hor[i][j]==1, h[0][i][j]==True, h[0][i][j]==False) for i in range(n) for j in range(n)]
move_0r = [ If(re[i][j]==1, r[0][i][j]==True, r[0][i][j]==False) for i in range(n) for j in range(n)]
move_0mn = [ If(mn[i][j]==1, mns[i][j]==True, mns[i][j]==False) for i in range(n) for j in range(n)]
move_0 = move_0v + move_0h + move_0r + move_0mn

# boundary conditions
boundary_v = [Not(v[m][n-1][j]) for m in range(1,k+1) for j in range(n)]
boundary_h = [Not(h[m][i][n-1])	for m in range(1,k+1) for i in range(n)]
boundary_r = [Not(r[m][red[0]][n-1]) for m in range(1,k+1)]
list_fg = []
for m in range(k+1):
	list_fg.append(r[m][red[0]][n-2])
final_goal = [Or(list_fg)]
bc = boundary_v + boundary_h + boundary_r + final_goal

#print(boundary_v)
# non-empty columns and rows
#a = [Or(v[0][:][j]) for j in range(n)]  # vertical cars in which columns
#b = [Or(h[0][i][:]) for i in range(n)]	# horizontal cars in which rows
#c = [Or(r[0][i][:]) for i in range(n)]  # red car in which row

# empty columns and rows
#process_v = [ If(Not(a[j]), Not(Or(v[m][:][j])), True) for j in range(n) for m in range(1,k+1)]
#process_h = [ If(Not(b[i]), Not(Or(h[m][i][:])), True) for i in range(n) for m in range(1,k+1)]
process_r = [ If(Not(i == red[0]), r[m][i][j]==False, True) for m in range(1,k+1) for i in range(n) for j in range(n)]

# mine restrictions
#process_minev1 = [ If(mns[i][j], Not(Or(v[1:][i][j])), True) for i in range(n) for j in range(n)]
#process_mineh1 = [ If(mns[i][j], Not(Or(h[1:][i][j])), True) for i in range(n) for j in range(n)]
#process_miner1 = [ If(mns[i][j], Not(Or(r[1:][i][j])), True) for i in range(n) for j in range(n)]

#process_minev2 = [ If(mns[i][j], Not(Or(v[1:][i-1][j])), True) for i in range(1,n) for j in range(n)]
#process_mineh2 = [ If(mns[i][j], Not(Or(h[1:][i][j-1])), True) for i in range(n) for j in range(1,n)]
#process_miner2 = [ If(mns[i][j], Not(Or(r[1:][i][j-1])), True) for i in range(n) for j in range(1,n)]
#process_mine = process_minev1 + process_mineh1 + process_miner1 + process_minev2 + process_mineh2 + process_miner2

# movement restriction(vertical)

move_v = [ If(v[m][i][j], eo( 
			v[m+1][i][j],
			And(v[m+1][i+1][j],Not(mns[i+2][j]),Not(v[m][i+2][j]),Not(h[m][i+2][j-1]),Not(h[m][i+2][j]),Not(r[m][i+2][j-1]),Not(r[m][i+2][j]) ),
			And(v[m+1][i-1][j],Not(mns[i-1][j]),Not(v[m][i-2][j]),Not(h[m][i-1][j-1]),Not(h[m][i-1][j]),Not(r[m][i-1][j-1]),Not(r[m][i-1][j]) )	
			), True)
		   for m in range(k) for i in range(2,n-2) for j in range(1, n)]

move_v1 = [ If(v[m+1][i][j], eo( 
			v[m][i][j],
			And(v[m][i+1][j],Not(mns[i][j]),Not(v[m][i-1][j]),Not(h[m][i][j-1]),Not(h[m][i][j]),Not(r[m][i][j-1]),Not(r[m][i][j]) ),
			And(v[m][i-1][j],Not(mns[i+1][j]),Not(v[m][i+1][j]),Not(h[m][i+1][j-1]),Not(h[m][i+1][j]),Not(r[m][i+1][j-1]),Not(r[m][i+1][j]) )	
			), True)
		   for m in range(k) for i in range(1,n-1) for j in range(1, n)]

# corner cases for movements(vertical)
move_v_0j = [ If(v[m][0][j], Xor( 
				v[m+1][0][j],
				And(v[m+1][1][j],Not(mns[2][j]),Not(v[m][2][j]),Not(h[m][2][j-1]),Not(h[m][2][j]),Not(r[m][2][j-1]),Not(r[m][2][j]) ),	
				), True)
		   		for m in range(k) for j in range(1, n)]

move_v1_0j = [ If(v[m+1][0][j], Xor( 
				v[m][0][j],
				And(v[m][1][j],Not(mns[0][j]),Not(h[m][0][j-1]),Not(h[m][0][j]),Not(r[m][0][j-1]),Not(r[m][0][j]) ),	
				), True)
		   		for m in range(k) for j in range(1, n)]

move_v_1j = [  If(v[m][1][j], eo( 
				v[m+1][1][j],
				And(v[m+1][2][j],Not(mns[3][j]),Not(v[m][3][j]),Not(h[m][3][j-1]),Not(h[m][3][j]),Not(r[m][3][j-1]),Not(r[m][3][j]) ),
				And(v[m+1][0][j],Not(mns[0][j]),Not(h[m][0][j-1]),Not(h[m][0][j]),Not(r[m][0][j-1]),Not(r[m][0][j]) )	
				), True)
		   		for m in range(k) for j in range(1, n)]

move_v_n2_j = [If(v[m][n-2][j], Xor(  
				v[m+1][n-2][j],
				And(v[m+1][n-3][j],Not(mns[n-3][j]),Not(v[m][n-4][j]),Not(h[m][n-3][j-1]),Not(h[m][n-3][j]),Not(r[m][n-3][j-1]),Not(r[m][n-3][j]) ),	
				), True)
		   		for m in range(k) for j in range(1, n)]

move_v_00 = [ If(v[m][0][0], Xor( 
				v[m+1][0][0],
				And(v[m+1][1][0],Not(mns[2][0]),Not(v[m][2][0]),Not(h[m][2][0]),Not(r[m][2][0]) ),	
				), True)
		   		for m in range(k)]

move_v1_00 = [ If(v[m+1][0][0], Xor( 
				v[m][0][0],
				And(v[m][1][0],Not(mns[0][0]),Not(h[m][0][0]),Not(r[m][0][0]) ),	
				), True)
		   		for m in range(k)]

move_v_10 = [  If(v[m][1][0], eo( 
				v[m+1][1][0],
				And(v[m+1][2][0],Not(mns[3][0]),Not(v[m][3][0]),Not(h[m][3][0]),Not(r[m][3][0]) ),
				And(v[m+1][0][0],Not(mns[0][0]),Not(h[m][0][0]),Not(r[m][0][0]) )	
				), True)
		   		for m in range(k)]

move_v_2n3_0 = [ If(v[m][i][0], eo( 
					v[m+1][i][0],
					And(v[m+1][i+1][0],Not(mns[i+2][0]),Not(v[m][i+2][0]),Not(h[m][i+2][0]),Not(r[m][i+2][0]) ),
					And(v[m+1][i-1][0],Not(mns[i-1][0]),Not(v[m][i-2][0]),Not(h[m][i-1][0]),Not(r[m][i-1][0]) )	
					), True)
		   		for m in range(k) for i in range(2,n-2)]

move_v1_i_0 = [ If(v[m+1][i][0], eo( 
					v[m][i][0],
					And(v[m][i+1][0],Not(mns[i][0]),Not(v[m][i-1][0]),Not(h[m][i][0]),Not(r[m][i][0]) ),
					And(v[m][i-1][0],Not(mns[i+1][0]),Not(v[m][i+1][0]),Not(h[m][i+1][0]),Not(r[m][i+1][0]) )	
					), True)
		   		for m in range(k) for i in range(1,n-1)]


move_v_n2_0 = [If(v[m][n-2][0], Xor( 
				v[m+1][n-2][0],
				And(v[m+1][n-3][0],Not(mns[n-3][0]),Not(v[m][n-4][0]),Not(h[m][n-3][0]),Not(r[m][n-3][0]) ),	
				), True)
		   		for m in range(k)]
# movement restriction(HORIZONTAL)

move_h = [ If(h[m][i][j], eo( 
			h[m+1][i][j],
			And(h[m+1][i][j+1],Not(mns[i][j+2]),Not(h[m][i][j+2]),Not(r[m][i][j+2]),Not(v[m][i-1][j+2]),Not(v[m][i][j+2]) ),
			And(h[m+1][i][j-1],Not(mns[i][j-1]),Not(h[m][i][j-2]),Not(r[m][i][j-2]),Not(v[m][i-1][j-1]),Not(v[m][i][j-1]) )	
			), True)
		   for m in range(k) for i in range(1,n) for j in range(2,n-2)]

move_h1 = [ If(h[m+1][i][j], eo( 
			h[m][i][j],
			And(h[m][i][j+1],Not(mns[i][j]),Not(h[m][i][j-1]),Not(r[m][i][j-1]),Not(v[m][i-1][j]),Not(v[m][i][j]) ),
			And(h[m][i][j-1],Not(mns[i][j+1]),Not(h[m][i][j+1]),Not(r[m][i][j+1]),Not(v[m][i-1][j+1]),Not(v[m][i][j+1]) )	
			), True)
		   for m in range(k) for i in range(1,n) for j in range(1,n-1)]


# corner cases for movements(HORIZONTAL)
move_h_i_0 = [ If(h[m][i][0], Xor( 
				h[m+1][i][0],
				And(h[m+1][i][1],Not(mns[i][2]),Not(h[m][i][2]),Not(r[m][i][2]),Not(v[m][i-1][2]),Not(v[m][i][2]) ),	
				), True)
		   	 for m in range(k) for i in range(1, n)]

move_h1_i_0 = [ If(h[m+1][i][0], Xor( 
				h[m][i][0],
				And(h[m][i][1],Not(mns[i][0]),Not(v[m][i-1][0]),Not(v[m][i][0]) ),	
				), True)
		   	 for m in range(k) for i in range(1, n)]

move_h_i_1 = [  If(h[m][i][1], eo( 
					h[m+1][i][1],
					And(h[m+1][i][2],Not(mns[i][3]),Not(h[m][i][3]),Not(r[m][i][3]),Not(v[m][i-1][3]),Not(v[m][i][3]) ),
					And(h[m+1][i][0],Not(mns[i][0]),Not(v[m][i-1][0]),Not(v[m][i][0]) )	
					), True)
		   		for m in range(k) for i in range(1,n)]

move_h_i_n2 = [ If(h[m][i][n-2], Xor( 
					h[m+1][i][n-2],
					And(h[m+1][i][n-3],Not(mns[i][n-3]),Not(h[m][i][n-4]),Not(r[m][i][n-4]),Not(v[m][i-1][n-3]),Not(v[m][i][n-3]) )	
					), True)
		   		for m in range(k) for i in range(1,n)]

move_h_0_0 = [ If(h[m][0][0], Xor( 
				h[m+1][0][0],
				And(h[m+1][0][1],Not(mns[0][2]),Not(h[m][0][2]),Not(r[m][0][2]),Not(v[m][0][2]) ),	
				), True)
		   	 	for m in range(k)]

move_h1_0_0 = [ If(h[m+1][0][0], Xor( 
				h[m][0][0],
				And(h[m][0][1],Not(mns[0][0]),Not(v[m][0][0]) ),	
				), True)
		   	 	for m in range(k)]

move_h_0_1 = [  If(h[m][0][1], eo( 
					h[m+1][0][1],
					And(h[m+1][0][2],Not(mns[0][3]),Not(h[m][0][3]),Not(r[m][0][3]),Not(v[m][0][3]) ),
					And(h[m+1][0][0],Not(mns[0][0]),Not(v[m][0][0]) )	
					), True)
		   		for m in range(k)]

move_h_0_2n3 = [ If(h[m][0][j], eo( 
					h[m+1][0][j],
					And(h[m+1][0][j+1],Not(mns[0][j+2]),Not(h[m][0][j+2]),Not(r[m][0][j+2]),Not(v[m][0][j+2]) ),
					And(h[m+1][0][j-1],Not(mns[0][j-1]),Not(h[m][0][j-2]),Not(r[m][0][j-2]),Not(v[m][0][j-1]) )	
					), True)
		   		 for m in range(k) for j in range(2,n-2)]

move_h1_0_j = [ If(h[m+1][0][j], eo( 
					h[m][0][j],
					And(h[m][0][j+1],Not(mns[0][j]),Not(h[m][0][j-1]),Not(r[m][0][j-1]),Not(v[m][0][j]) ),
					And(h[m][0][j-1],Not(mns[0][j+1]),Not(h[m][0][j+1]),Not(r[m][0][j+1]),Not(v[m][0][j+1]) )	
					), True)
		   		 for m in range(k) for j in range(1,n-1)]

move_h_0_n2 = [If(h[m][0][n-2], Xor( 
				h[m+1][0][n-2],
				And(h[m+1][0][n-3],Not(mns[0][n-3]),Not(h[m][0][n-4]),Not(r[m][0][n-4]),Not(v[m][0][n-3]))	
				), True)
		   		for m in range(k)]

# movement restriction(RED)
move_red = []
if red[0] != 0:
	move_r = [ If(r[m][red[0]][j], eo( 
				r[m+1][red[0]][j],
				And(r[m+1][red[0]][j+1],Not(mns[red[0]][j+2]),Not(h[m][red[0]][j+2]),Not(v[m][red[0]-1][j+2]),Not(v[m][red[0]][j+2]) ),
				And(r[m+1][red[0]][j-1],Not(mns[red[0]][j-1]),Not(h[m][red[0]][j-2]),Not(v[m][red[0]-1][j-1]),Not(v[m][red[0]][j-1]) )	
				), True)
		   	for m in range(k) for j in range(2,n-2)]
	
	move_r1 = [ If(r[m+1][red[0]][j], eo( 
			r[m][red[0]][j],
			And(r[m][red[0]][j+1],Not(mns[red[0]][j]),Not(h[m][red[0]][j-1]),Not(v[m][red[0]-1][j]),Not(v[m][red[0]][j]) ),
			And(r[m][red[0]][j-1],Not(mns[red[0]][j+1]),Not(h[m][red[0]][j+1]),Not(v[m][red[0]-1][j+1]),Not(v[m][red[0]][j+1]) )	
			), True)
		   for m in range(k) for j in range(1,n-1)]

	move_r_red_0 = [ If(r[m][red[0]][0], Xor( 
				r[m+1][red[0]][0],
				And(r[m+1][red[0]][1],Not(mns[red[0]][2]),Not(h[m][red[0]][2]),Not(v[m][red[0]-1][2]),Not(v[m][red[0]][2]) ),	
				), True)
		   	for m in range(k)]
	
	move_r1_i_0 = [ If(r[m+1][red[0]][0], Xor( 
				r[m][red[0]][0],
				And(r[m][red[0]][1],Not(mns[red[0]][0]),Not(v[m][red[0]-1][0]),Not(v[m][red[0]][0]) ),	
				), True)
		   	 for m in range(k)]

	move_r_red_1 = [  If(r[m][red[0]][1], eo( 
					r[m+1][red[0]][1],
					And(r[m+1][red[0]][2],Not(mns[red[0]][3]),Not(h[m][red[0]][3]),Not(v[m][red[0]-1][3]),Not(v[m][red[0]][3]) ),
					And(r[m+1][red[0]][0],Not(mns[red[0]][0]),Not(v[m][red[0]-1][0]),Not(v[m][red[0]][0]) )	
					), True)
		   		for m in range(k)]

	move_r_red_n2 = [ If(r[m][red[0]][n-2], Xor( 
					r[m+1][red[0]][n-2],
					And(r[m+1][red[0]][n-3],Not(mns[red[0]][n-3]),Not(h[m][red[0]][n-4]),Not(v[m][red[0]-1][n-3]),Not(v[m][red[0]][n-3]) )	
					), True)
		   		   for m in range(k)]
	move_red = move_r + move_r_red_0 + move_r_red_1 + move_r_red_n2 + move_r1 + move_r1_i_0
else:
	move_r_0_0 = [ If(r[m][0][0], Xor( 
					r[m+1][0][0],
					And(r[m+1][0][1],Not(mns[0][2]),Not(h[m][0][2]),Not(v[m][0][2]) ),	
					), True)
					for m in range(k)]

	move_r1_0_0 = [ If(r[m+1][0][0], Xor( 
				r[m][0][0],
				And(r[m][0][1],Not(mns[0][0]),Not(v[m][0][0]) ),	
				), True)
		   	 	for m in range(k)]

	move_r_0_1 = [  If(r[m][0][1], eo( 
						r[m+1][0][1],
						And(r[m+1][0][2],Not(mns[0][3]),Not(h[m][0][3]),Not(v[m][0][3]) ),
						And(r[m+1][0][0],Not(mns[0][0]),Not(v[m][0][0]) )	
						), True)
					for m in range(k)]

	move_r_0_2n3 = [ If(r[m][0][j], eo( 
						r[m+1][0][j],
						And(r[m+1][0][j+1],Not(mns[0][j+2]),Not(h[m][0][j+2]),Not(v[m][0][j+2]) ),
						And(r[m+1][0][j-1],Not(mns[0][j-1]),Not(h[m][0][j-2]),Not(v[m][0][j-1]) )	
						), True)
					for m in range(k) for j in range(2,n-2)]

	move_r1_0_j = [ If(r[m+1][0][j], eo( 
					r[m][0][j],
					And(r[m][0][j+1],Not(mns[0][j]),Not(h[m][0][j-1]),Not(v[m][0][j]) ),
					And(r[m][0][j-1],Not(mns[0][j+1]),Not(h[m][0][j+1]),Not(v[m][0][j+1]) )	
					), True)
		   		 for m in range(k) for j in range(1,n-1)]

	move_r_0_n2 = [If(r[m][0][n-2], Xor( 
					r[m+1][0][n-2],
					And(r[m+1][0][n-3],Not(mns[0][n-3]),Not(h[m][0][n-4]),Not(v[m][0][n-3]))	
					), True)
					for m in range(k)]
	move_red = move_r_0_0 + move_r_0_1 + move_r_0_2n3 + move_r_0_n2 + move_r1_0_j + move_r1_0_0

movev =  move_red + move_v + move_v_00 + move_v_0j + move_v_10 + move_v_1j + move_v_2n3_0 + move_v_n2_0 + move_v_n2_j
movev1 = move_v1 + move_v1_00 + move_v1_0j + move_v1_i_0
moveh = move_h + move_h_0_0 + move_h_0_1 + move_h_0_2n3 + move_h_0_n2 + move_h_i_0 + move_h_i_1 + move_h_i_n2
moveh1 = move_h1 + move_h1_0_j + move_h1_0_0 + move_h1_i_0
move = movev + movev1 + moveh + moveh1

# 1 position change
opc = []
V = [[[ Bool("V_%s_%s_%s" % (m,i,j)) for j in range(n)] for i in range(n)] for m in range(1,k+1)]
H = [[[ Bool("H_%s_%s_%s" % (m,i,j)) for j in range(n)] for i in range(n)] for m in range(1,k+1)]
R = [[[ Bool("R_%s_%s_%s" % (m,i,j)) for j in range(n)] for i in range(n)] for m in range(1,k+1)]

Vnorm = [ V[m-1][i][j] == And(v[m][i][j], Xor(v[m-1][i-1][j],v[m-1][i+1][j])) for m in range(1,k+1) for i in range(1,n-1) for j in range(n)]
Hnorm = [ H[m-1][i][j] == And(h[m][i][j], Xor(h[m-1][i][j-1],h[m-1][i][j+1])) for m in range(1,k+1) for i in range(n) for j in range(1,n-1) ]
Rnorm = [ R[m-1][i][j] == And(r[m][i][j], Xor(r[m-1][i][j-1],r[m-1][i][j+1])) for m in range(1,k+1) for i in range(n) for j in range(1,n-1)]
V0j = [ V[m-1][0][j] == And(v[m][0][j], v[m-1][1][j])	for m in range(1,k+1) for j in range(n) ]
Vn21j = [ V[m-1][n-1][j] == False 	for m in range(1,k+1) for j in range(n) ]
Hi0 = [ H[m-1][i][0] == And(h[m][i][0],h[m-1][i][1]) for m in range(1,k+1) for i in range(n) ]
Hin1 = [ H[m-1][i][n-1] == False for m in range(1,k+1) for i in range(n) ]
Ri0 = [ R[m-1][i][0] == And(r[m][i][0],r[m-1][i][1]) for m in range(1,k+1) for i in range(n) ]
Rin1 = [ R[m-1][i][n-1] == False for m in range(1,k+1) for i in range(n) ]
mv = Vnorm + Hnorm + Rnorm + V0j + Vn21j + Hi0 + Hin1 + Ri0 + Rin1

def at_most_one(literals):
	x = []
	for pair in combinations(literals, 2):
		a, b = pair[0], pair[1]
		x += [Or(Not(a), Not(b))]
	return And(x)

for m in range(1,k+1):
	ls = []
	for i in range(n):
		ls += V[m-1][i][:]
		ls += H[m-1][i][:]
		ls += R[m-1][i][:]
	opc.append(And(AtLeast(*ls,1), AtMost(*ls,1)))
	#opc.append(And(at_most_one(ls), Or(ls)))

s = Solver()
s.add(move_0)
s.add(bc)
s.add(process_r)
s.add(move)
s.add(mv)
s.add(opc)

if s.check() == sat:
	mod = s.model()
	for m in range(1,k+1):
		if mod.evaluate(R[m-1][red[0]][n-2]) == True:
			print(red[0],",",n-2,sep="")
			break
		done = False
		for j in range(n-1):
			if mod.evaluate(R[m-1][red[0]][j]):
				if j==0:
					print(red[0],",",1,sep="")
				elif mod.evaluate(r[m-1][red[0]][j+1]):
					print(red[0],",",j+1,sep="")
				else:
					print(red[0],",",j,sep="")
				done=True
				break
		if done:
			continue
		for i in range(n):
			for j in range(n):
				if mod.evaluate(V[m-1][i][j]):
					if i==0:
						print(1,",",j,sep="")
					elif i==n-2:
						print(n-2,",",j,sep="")
					elif mod.evaluate(v[m-1][i+1][j]):
						print(i+1,",",j,sep="")
					else:
						print(i,",",j,sep="")
					done = True
					break
				elif mod.evaluate(H[m-1][i][j]):
					if j==0:
						print(i,",",1,sep="")
					elif j==n-2:
						print(i,",",n-2,sep="")
					elif mod.evaluate(h[m-1][i][j+1]):
						print(i,",",j+1,sep="")
					else:
						print(i,",",j,sep="")
					done = True
					break
			if done:
				break
else:
	print("unsat")

#for m in range(k+1):
		#for i in range(n):
			#for j in range(n):
				#print(mod.evaluate(v[m][i][j]), "v",m,i,j)
				#print("--------")
				#print(mod.evaluate(h[m][i][j]), "h",m,i,j)
				#print("--------")
				#print(mod.evaluate(r[m][i][j]), "r",m,i,j)
				#print("--------------------------------")





