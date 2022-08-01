import numpy 	as np
from colors 	import * # test_color, clrsd

from cv2 	import (
			circle,
			imencode
			)

from time 	import perf_counter


import base64



start = perf_counter()
for rgb, string in clrsd.items():

	if x := test_color(*rgb):
		clrsd[rgb] = x
	else:
		img = np.zeros( (300,300, 4) ) # Include the alpha channel (4)
		img = circle(img, (150, 150), 150, rgb[::-1] + (255,) , 7)
		img = imencode('.png', img)

		arr = img[1]
		arr = arr.tobytes()
		enc = base64.encodebytes(arr).decode()



print(clrsd)
print(f"Generated in { round(perf_counter() - start, 4) }s...")
