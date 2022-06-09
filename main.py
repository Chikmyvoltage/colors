import numpy 	as np
from colors 	import * # test_color, clrsd
#from rgb_map 	import clrsd
from emote 	import upload_emote

from cv2 	import (
			circle,
			imencode
			)

from time 	import perf_counter


import base64


guild_ids = [1]
token	  = "TOKEN"

clrsd = {(245,255,0): ':red:'}


start = perf_counter()
for tuple, string in clrsd.items():
	if len(string) < 10:

		if x := test_color(*tuple):
			clrsd[tuple] = x
		else:
			# TODO request discord server to add emoji and get ID
#			img = imread('/home/mshary/Templates/template2.png', 1)
			img = np.zeros( (300,300, 4) )
			img = circle(img, (150, 150), 150, tuple[::-1] + (255,) , 7)
			img = imencode('.png', img)

			arr = img[1]
			arr = arr.tobytes()
			enc = base64.encodebytes(arr).decode()

			""" post_emote(token, guild, name, image) """
			for guild in guild_ids:
				try:
					string = upload_emote(   token=token,
						  		guild=guild,
						  		name="anothercircle",
						  		image=enc
						)
				except ValueError as e:
					print(f"Error: {e}")
					continue

				else:
					clrsd[tuple] = string
					break
print(clrsd)
print(f"Generated in { round(perf_counter() - start, 4) }s...")
