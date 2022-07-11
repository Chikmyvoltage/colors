from base_colors import base
from time 	 import perf_counter
from cv2 	 import imencode, imread, circle
from base64	 import encodebytes
from rgb_map	 import clrsd
import numpy 	 as	np

#import requests


cf1 = lambda c: ((c + 0.055) / 1.055) ** 2.4 if c > 0.04045 else c / 12.92

cf2 = lambda c: c ** 0.3333333333333333 if c > 0.008856 else ( 7.787 * c ) + 0.13793103448275862

def computeXYZ(R, G, B):

	R /= 255
	G /= 255
	B /= 255

	R,G,B = map(cf1, (R,G,B))

	R *= 100
	G *= 100
	B *= 100

	X = R * 0.4124  +  G * 0.3576  +  B * 0.1805
	Y = R * 0.2126  +  G * 0.7152  +  B * 0.0722
	Z = R * 0.0193  +  G * 0.1192  +  B * 0.9505
	return X, Y, Z


def computeLAB(X, Y, Z):

	X,Y,Z = map(cf2, (X,Y,Z))

	L = (116 * Y) - 16
	a = 500 * (X - Y)
	b = 200 * (Y - Z)

	return L, a, b



def retrgb(hexadecimal: int):
        r = (hexadecimal & 0xff0000) >> 16
        g = (hexadecimal & 0xff00) >> 8
        b = hexadecimal & 0xff
        return r,g,b



def computeMSE(R, G, B):
        closest = 0xff
        ch = None
        for (r, g, b), value in clrsd.items():
                distance = abs(R - r) + abs(G - g) + abs(B - b)
                if distance < closest:
                        closest = distance
                        ch = value
        return ch

def test_color(R, G, B):



    ret = False
    closest = 0xffff
    X, Y, Z = computeXYZ(R, G, B)
    L1, a1, b1 = computeLAB(X, Y, Z)

    for value, (r, g, b) in base.items():

        L2, a2, b2 = computeLAB( * computeXYZ(r,g,b) )

        distance = abs(L2 - L1)  +  abs(a2 - a1)  +  abs(b2 - b1)


        if distance > closest:
            continue

        closest = distance
#        print(distance)
        if not distance: # entropy matches. return base color
            print(f"{R,G,B} entropy match with {r,g,b}")
            ret =  value

        elif distance < 50:
            print(f"{R,G,B} is fairly close to {r,g,b}")
            ret =  value

        elif distance < 67:
            print(f"{R,G,B} is somewhat close to {r,g,b}")
            ret =  value

    return ret



if __name__ == "__main__":

	start = perf_counter()
	color = computeMSE(233, 25, 8) # Red
	print(color)
	print(f"Done in { round( perf_counter() - start, 4 ) }s...")

