input screenx, "enter screen x size: "
let screenx, int(screenx)
input screeny, "enter screen y size: "
let screeny, int(screeny)
input mazex, "enter maze x size: "
let mazex, int(mazex)
input mazey, "enter maze y size: "
let mazey, int(mazey)

print "Preparing maze... "
let squarex, screenx/mazex
let squarey, screeny/mazey

screen screenx, screeny
fullscreen 1
title "Maze generator"
keyrepeat 1, 200
dim sides, mazex, mazey
dim downs, mazex, mazey
dim visited, mazex, mazey
for x, 0, mazex-1
	for y, 0, mazey-1
		if (x = 0) or (x = (mazex-1)) or (y = 0) or (y = (mazey-1))
			let visited(x,y), 1
		else
			let visited(x,y), 0
		end
		let sides(x,y), 1
		let downs(x,y), 1
	end
end

dim stackx, mazex*mazey+1
dim stacky, mazex*mazey+1
let spointerx, 1
let spointery, 1

let px, 1
let py, 1
let stackx(0), 1
let stacky(0), 1

color 0,0,0
rect 0,0,screenx, screeny
color 255,255,255
update

for mx, 1, mazex-2
	for my, 1, mazey-2
		let xc, mx*squarex
		let yc, my*squarey
		line int(xc), int(yc+squarey), int(xc+squarex), int(yc+squarey),3
		line int(xc+squarex), int(yc), int(xc+squarex), int(yc+squarey),3
		line int(xc), int(yc), int(xc+squarex), int(yc),3
		line int(xc), int(yc), int(xc), int(yc+squarey),3
	end
end

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

let px, 1
let py, 1
let dir, 4
gosub render

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
	let xc, px*squarex
	let yc, py*squarey
	color 0,0,0
	if dir = 1
		line int(xc+squarex), int(yc+1), int(xc+squarex), int(yc+squarey-1),3
	end
	if dir = 2
		line int(xc+1), int(yc+squarey), int(xc+squarex-1), int(yc+squarey),3
	end
	if dir = 3
		line int(xc), int(yc+1), int(xc), int(yc+squarey-1),3
	end
	if dir = 4
		line int(xc+1), int(yc), int(xc+squarex-1), int(yc),3
	end
	color 255,255,255
	update
return

label rendergame
	let xc, npx*squarex
	let yc, npy*squarey
	let lxc, lastpx*squarex
	let lyc, lastpy*squarey
	let axc, ax*squarex
	let ayc, ay*squarey
	color 0, 0, 0
	rect int(lxc+4), int(lyc+4), int(lxc+squarex-4), int(lyc+squarey-4)
	color 0,255,0
	rect int(axc+4), int(ayc+4), int(axc+squarex-4), int(ayc+squarey-4)
	color 0,0,255
	rect int(xc+4), int(yc+4), int(xc+squarex-4), int(yc+squarey-4)
	update
return

label createapple
	let ax, randint(1, mazex-2)
	let ay, randint(1, mazey-2)
	let axc, ax*squarex
	let ayc, ay*squarey
	color 0,255,0
	rect int(axc+4), int(ayc+4), int(axc+squarex-4), int(ayc+squarey-4)
	update
return

label game
let px, 1
let py, 1
let npx, 1
let npy, 1
gosub createapple
gosub rendergame
let done, 0
while not(winexit()) and not(done)
	let k, keypress()
	let lastpx, px
	let lastpy, py
	let npx, px
	let npy, py
	if not(k < 0) and not(k > 255)
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