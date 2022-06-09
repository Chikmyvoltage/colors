from json import dumps
from requests import post
from time import sleep

__all__ = ['upload_emote']

def upload_emote(token: str,
		 guild: [str, int],
		 name : str,
		 image: [str, bytes] ) -> str:
	""" upload_emote(token, guild, name, image)

	    token : type str
	    	To authenticate requests made to discord

	    guild : type [id, int]
		Guild id used to specify which guild/server to upload the emote to.

	    name  : type str
	   	The name of the emote

	    image : type [str, bytes] BASE64 ENCODED
	   	The image data of the emote, PNG and base64 encoded.


	    Returns:
	    	str: "<:emote_name:emote_id>"

	    Raises:

	    	EncodingWarning: The image is not PNG encoded.

	    	ValueError: Request failed

	"""


	if type(image) is bytes:
		image = image.decode()

	if not image.startswith('iVBORw0KGgo'):
		raise EncodingWarning("image headers invalid, most likely image isn't PNG encoded.")


	for _ in range(4): # Four attempts
		data = dumps( {"image":f"data:image/png;base64,{image}", "name":name} )

		resp = post(f"https://discord.com/api/v9/guilds/{guild}/emojis",

			headers = {"authorization":token,
				   "content-type":"application/json",
				   "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"},

			data    =  data
			)

		match resp.status_code:
			case 201:

				json = resp.json()
				name = json['name']
				id   = json['id']

				ret  = f"<:{name}:{id}>"
				return ret

			case 429:

				t = resp.json()['retry_after']
				print(f"sleeping for {t}")
				sleep( t )
				continue

			case 400:

				msg = dumps( resp.json(), sort_keys=True, indent=4 )
				raise ValueError(msg)

			case _:

				raise ValueError(f'UNKNOWN ERROR {resp.status_code} {resp.reason}')

