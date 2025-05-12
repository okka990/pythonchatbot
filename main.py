from openai import OpenAI
from fastapi import FastAPI , Form ,Request, WebSocket
from typing import Annotated

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

client = OpenAI(
    api_key = os.getenv('OPENAI_API_KEY') 
)

templates = Jinja2Templates(directory="templates")

app.mount('/static',StaticFiles(directory="static"),name="static")


chatlogs = [{
	"role":"system",
	"content":"You are a friend of DLT , \
	also you know everything about general knowledge \
	tell the joke for webdevelopment"  # \ mean new line
}]

datas = []

#  text generate


@app.get("/",response_class=HTMLResponse)
async def chatpage(request:Request):
	return templates.TemplateResponse(
		# request = request,name = "layout.html"
		# "layout.html",{"request":request}
		# request = request,name = "layout.html",context={"datas":datas}

		"layout.html",{"request":request,"datas":datas}

	)


# =>  text generate (before websocket)
# https://fastapi.tiangolo.com/reference/templating/
# @app.post('/',response_class=HTMLResponse)
# async def chat(request:Request,userinput:Annotated[str,Form()]):

# 	chatlogs.append({"role":"user","content":userinput})

# 	datas.append(userinput)

# 	completion = client.chat.completions.create(
# 		model = "gpt-3.5-turbo",
# 		# store = False,
# 		messages = chatlogs,
# 		temperature = 0.6
# 	)

# 	botresponse = completion.choices[0].message.content
# 	chatlogs.append({"role":"assistant","content":botresponse})
# 	datas.append(botresponse)

# 	# return (botresponse)
# 	return templates.TemplateResponse(
# 		"layout.html",{"request":request,"datas":datas}

# 		# request = request,name = "layout.html",context={"datas":datas}

# 		)


# =>  text generate (after websocket)
# @app.post('/',response_class=HTMLResponse)
# async def chat(request:Request,userinput:Annotated[str,Form()]):

# 	chatlogs.append({"role":"user","content":userinput})

# 	datas.append(userinput)

# 	completion = client.chat.completions.create(
# 		model = "gpt-3.5-turbo",
# 		# store = False,
# 		messages = chatlogs,
# 		temperature = 0.6
# 	)

# 	botresponse = completion.choices[0].message.content
# 	chatlogs.append({"role":"assistant","content":botresponse})
# 	datas.append(botresponse)

# 	# return (botresponse)
# 	return templates.TemplateResponse(
# 		"layout.html",{"request":request,"datas":datas}

# 		# request = request,name = "layout.html",context={"datas":datas}

# 		)


# text generate (after WebSocket)
# exe1
# @app.websocket("/ws")


# async def chat(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         userinput = await websocket.receive_text()

#         chatlogs.append({"role": "user", "content": userinput})
#         datas.append(userinput)
#         try:
#             completion = client.chat.completions.create(
#                 model="gpt-3.5-turbo",
#                 # store = False,
#                 messages=chatlogs,
#                 temperature=0.6
#             )
#             botresponse = completion.choices[0].message.content

#             chatlogs.append({"role": "assistant", "content": botresponse})
#             datas.append(botresponse)

#             await websocket.send_text(str(completion))
			
#             await websocket.send_text(botresponse)


#         except Exception as err:
#             await websocket.send_text(f"error found,{str(err)}")
#             break


# exe 3 

@app.websocket("/ws")
async def chat(websocket: WebSocket):
    await websocket.accept()
    while True:
        userinput = await websocket.receive_text()

        chatlogs.append({"role": "user", "content": userinput})

        fullresponse = ""
        try:
            completion = client.chat.completions.create(
                model="gpt-4.1",
                # store = False,
                messages=chatlogs,
                temperature=0.6,
                stream=True
            )

            for chunk in completion:
            	botresponse = chunk.choices[0].delta.content

            	if botresponse is not None:
            		fullresponse += botresponse
            		await websocket.send_text(str(botresponse))
            		chatlogs.append({"role": "assistant", "content": fullresponse})


	            # botresponse = completion.choices[0].message.content

	            # chatlogs.append({"role": "assistant", "content": botresponse})
	            # datas.append(botresponse)

	            # await websocket.send_text(botresponse)


        except Exception as err:
            await websocket.send_text(f"error found,{str(err)}")
            break






# exe2

# completion = client.chat.completions.create(
#     # model="gpt-4o",
#     model="gpt-3.5-turbo",
#     messages=[
#         {
#             "role": "system",
#             "content": "You are a helpful assistant"
#         },
#         {
#             "role": "user",
#             "content": "who is the owner of meta?"
#         }
#     ],	
#     temperature = 0.6
# )
# print(completion.choices[0].message.content)



#  image generate
# => before webscoket 
# @app.get("/image",response_class=HTMLResponse)
# async def image(request:Request):
# 	return templates.TemplateResponse(
# 		# request = request,name = "image.html"
# 		# "image.html",{"request":request}
# 		# request = request,name = "image.html"

# 		"image.html",{"request":request,"datas":None,"error":None}

# 	)

# @app.post('/image',response_class=HTMLResponse)
# async def generateimage(request:Request,userinput:Annotated[str,Form()]):

# 	error = None
# 	data = None

# 	try:

# 	# datas.append(userinput)

# 		completion = client.images.generate(
# 			model="dall-e-2",
# 	        prompt=userinput,
# 	        size="256x256",  # "256x256" "512x512" "1024x1024"
# 	        # quality="standard", # standard   hd
# 	        n=1,
# 		)

# 		botresponse = completion.data[0].url

# 		if not completion.data or not botresponse:
# 			raise ValueError("No image generated")


# 		# updated data to template
# 		return templates.TemplateResponse(
# 			# "image.html",{"request":request,"datas":datas}

# 			request = request,name = "image.html",context={"data":botresponse,"error":error}

# 			)	



# 	except Exception as e:	
# 		return templates.TemplateResponse(
# 		"image.html",{"request":request,"datas":datas,"error":f"Error generate image : {str(e)}"}


# 		)	


# => after websocket
@app.get("/image",response_class=HTMLResponse)
async def image(request:Request):
	return templates.TemplateResponse(
		# request = request,name = "image.html"
		# "image.html",{"request":request}
		# request = request,name = "image.html"

		"image.html",{"request":request,"datas":None,"error":None}

	)


# // 
@app.websocket("/image")
async def generateimage(websocket: WebSocket):
    await websocket.accept()
    while True:
        userinput = await websocket.receive_text()

        chatlogs.append({"role": "user", "content": userinput})
        try:
            completion = client.images.generate(
				model="dall-e-2",
		        prompt=userinput,
		        size="256x256",  # "256x256" "512x512" "1024x1024"
		        # quality="standard", # standard   hd
		        n=1
            )

            botresponse = completion.data[0].url
            	
            if not completion.data or not botresponse :
            	raise ValueError("no image generate")

            await websocket.send_text(str(botresponse))


            # for chunk in completion:

            		# chatlogs.append({"role": "assistant", "content": botresponse})


	            # botresponse = completion.choices[0].message.content

	            # chatlogs.append({"role": "assistant", "content": botresponse})
	            # datas.append(botresponse)

	            # await websocket.send_text(botresponse)


        except Exception as err:
            await websocket.send_text(f"error found,{str(err)}")
            break




# templates = Jinja2Templates(directory="templates")
# https://fastapi.tiangolo.com/advanced/templates/#using-jinja2templates
# 22MA

# 28ER



# 5WS