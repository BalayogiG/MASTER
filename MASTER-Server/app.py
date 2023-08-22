from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
import webbrowser
import json
import uvicorn
from utils import *
from PIL import Image
import base64
from io import BytesIO

app = FastAPI()
origins = ["*"]

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory='templates/')

host = "0.0.0.0"
port = 5000

user_data = []
content = ""
result = ""


@app.get('/')
async def home(request : Request):
	return templates.TemplateResponse('index.html', context={'request': request})

@app.get('/register')
async def register(request: Request):
	return templates.TemplateResponse('register.html', context={'request': request})

@app.post('/register',response_class=HTMLResponse)
async def register(request:Request, username:str = Form(...), password:str = Form(...)):
	user_data.append(username)
	user_data.append(password)
	return RedirectResponse(url="/confirmRegistration", status_code=302)

@app.get('/confirmRegistration')
async def confirmRegistration(request: Request):
	return templates.TemplateResponse('confirmRegistration.html', context={'request':request})

@app.post('/confirmRegistration', response_class=HTMLResponse)
async def confirmRegistration(request: Request):
	data = await request.json()
	result = data['message']
	global content
	content = str(result)
	res = content.split('$')
	if (res[0] == user_data[0]):  
		resp = {"message": "Data Transmitted"}
		response = json.dumps(resp)
		return response
	else:
		resp = {"message": "Data Not Transmitted"}
		response = json.dumps(resp)
		return response

@app.post('/originalRegistration', response_class=HTMLResponse)
async def originalRegistration(request:Request):
	feedback = ""
	res = content.split("$")
	result = random_hash_splitter(user_data[1])
	first_enc = dna_encrypt(user_data[0] + "#" + result[1] + "#" + result[2] + "#" + res[1])
	qrimg = generate_qr_code(first_enc)
	stegimg = hide_message(qrimg, result[3])
	qimg = image_to_bytes(qrimg)
	simg = image_to_bytes(stegimg)
	if (len(get_user(uname=user_data[0])) == 0):
		status = add_user(username=user_data[0],passwordHash=result[0], randomVal=result[1], secID = res[1], qrImg=qimg, stegQRImg=simg)
		if status == 'done':
			feedback = "Account Created Successfully"
			return templates.TemplateResponse('feedback.html', context={'request':request, 'data':feedback})
		feedback = "Account not Created"
	return templates.TemplateResponse('feedback.html', context={'request':request, 'data':feedback})
	

@app.get("/user_search")
async def user_search(request: Request):
    data = "static/brain.png"
    return templates.TemplateResponse('user_search.html',context={'request':request, 'data':data})

@app.post("/user_search", response_class=HTMLResponse)
async def user_search(request: Request, username:str = Form(...)):
	data = "static/brain.png"
	if (len(get_user(uname=username)) != 0):
		record = get_user(uname=username)
		qrimg = base64.b64encode(bytes(record[0][4])).decode('utf-8')
		data = "data:image/png;base64," + qrimg
		return templates.TemplateResponse('user_search.html', context={'request':request, 'data':data})
	return templates.TemplateResponse('user_search.html',context={'request':request, 'data':data})

@app.post("/Login", response_class=HTMLResponse)
async def Login(request: Request):
	data = await request.json()
	global result
	result = data['message']


@app.post("/originalLogin", response_class=HTMLResponse)
async def originalLogin(request: Request):
	feedback = ""
	data = result
	s_data = data.split("$")
	if (len(get_user(uname=s_data[0])) != 0):
		record = get_user(uname=s_data[0])
		if(record[0][0] == s_data[0]):
			image_stream = BytesIO(bytes(record[0][5]))
			image = Image.open(image_stream)
			msg = reveal_message(image)
			value = s_data[1]
			hash = re_get(value, s_data[2], msg)
			if hash == record[0][1]:
				feedback = "Account Logged in Successfully"
				return templates.TemplateResponse('feedback.html', context={'request':request, 'data':feedback})
			feedback = "Account Login Unsuccessful"
			return templates.TemplateResponse('feedback.html', context={'request':request, 'data':feedback})



if __name__ == "__main__":
    uvicorn.run(app, host=host, port=port)