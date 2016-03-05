screen 800,800
title "Maze generator"
dim sides, 80, 80
dim downs, 80, 80
dim visited, 80, 80
for x, 0, 79
	for y, 0, 79
		if (x = 0) or (x = 79) or (y = 0) or (y = 79)
			let visited(x,y), 1
		else
			let visited(x,y), 0
		end
		let sides(x,y), 1
		let downs(x,y), 1
	end
end

dim stackx, 80*80+1
dim stacky, 80*80+1
let spointerx, 1
let spointery, 1

let px, 1
let py, 1
let stackx(0), 1
let stacky(0), 1

color 0,0,0
rect 0,0,800,800
color 255,255,255
update

while spointerx != 0
	let visited(px, py), 1
	gosub choosedir
	let xval, px
	let yval, py
	if spointerx != 0
		gosub push
	end
	gosub render
	if dir = 1
		let sides(px, py), 0
		let px, px+1
	end
	if dir = 2
		let downs(px, py), 0
		let py, py+1
	end
	if dir = 3
		let sides(px-1, py), 0
		let px, px-1
	end
	if dir = 4
		let downs(px, py-1), 0
		let py, py-1
	end
end

while clickx() = -1
end

goto game

label choosedir
	let done, 0
	gosub backtrack
	while not(done) and (spointerx != 0)
		let dir, randint(1, 4)
		if (dir = 1) and (visited(px+1, py) = 0)
			let done, 1
		end
		if (dir = 2) and (visited(px, py+1) = 0)
			let done, 1
		end
		if (dir = 3) and (visited(px-1, py) = 0)
			let done, 1
		end
		if (dir = 4) and (visited(px, py-1) = 0)
			let done, 1
		end
	end
return

label backtrack
	while (visited(px+1, py) = 1) and (visited(px, py-1) = 1) and (visited(px-1, py) = 1) and (visited(px, py+1) = 1) and (spointerx != 0)
		gosub pop
		let px, xval
		let py, yval
	end
return

label push
	let stackx(spointerx), xval
	let stacky(spointery), yval
	let spointerx, spointerx+1
	let spointery, spointery+1
return

label pop
	let spointerx, spointerx-1
	let spointery, spointery-1
	let xval, stackx(spointerx)
	let yval, stacky(spointery)
return

label render
	let xc, px*10
	let yc, py*10
	rect xc, yc, xc+5, yc+5
	if dir = 1
		rect xc+5, yc, xc+10, yc+5
	end
	if dir = 2
		rect xc, yc+5, xc+5, yc+10
	end
	if dir = 3
		rect xc-5, yc, xc, yc+5
	end
	if dir = 4
		rect xc, yc-5, xc+5, yc
	end
	update
return

label rendergame
	let xc, npx*10
	let yc, npy*10
	let lxc, lastpx*10
	let lyc, lastpy*10
	let axc, ax*10
	let ayc, ay*10
	color 255, 255, 255
	rect lxc, lyc, lxc+5, lyc+5
	color 0,255,0
	rect axc, ayc, axc+5, ayc+5
	color 0,0,255
	rect xc, yc, xc+5, yc+5
	update
return

label createapple
	let ax, randint(1, 78)
	let ay, randint(1, 78)
	let axc, ax*10
	let ayc, ay*10
	color 0,255,0
	rect axc, ayc, axc+5, ayc+5
	print ax, ay
	update
return

label game
let px, 1
let py, 1
gosub createapple
let done, 0
while not(done)
	let k, keypress()
	let lastpx, px
	let lastpy, py
	let npx, px
	let npy, py
	if k != -1
		if chr(k) = "q"
			let done, 1
		end
		if (chr(k) = "w") and (downs(px, py-1) = 0)
			let npy, py-1
			gosub rendergame
		end
		if (chr(k) = "s") and (downs(px, py) = 0)
			let npy, py+1
			gosub rendergame
		end
		if (chr(k) = "a") and (sides(px-1, py) = 0)
			let npx, px-1
			gosub rendergame
		end
		if (chr(k) = "d") and (sides(px, py) = 0)
			let npx, px+1
			gosub rendergame
		end
		let px, npx
		let py, npy
		if (px = ax) and (py = ay)
			gosub createapple
		end
	end
end