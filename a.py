from flask import Flask, request, render_template
import logging
import os
import io
import base64
import socket
import PIL.Image as Image
app = Flask(__name__)
BUFF_SIZE = 65536
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print("here"+str(host_ip))
port = 7350
socket_address = (host_ip, port)
server_socket.bind(socket_address)
print('Listening at:'+str(socket_address))
#
# while True:
#     msg, client_addr = server_socket.recvfrom(BUFF_SIZE)
#     print('GOT connection from', client_addr)
#     print(msg)
# logging.basicConfig(level=logging.DEBUG) #for better debuging, we will log out every request with headers and body.
@app.before_request
def log_request_info():
    logging.info('Headers: %s', request.headers)
    logging.info('Body: %s', request.get_data())

@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():

    if request.method == "POST": #if we make a post request to the endpoint, look for the image in the request body
        image_raw_bytes = request.get_data()  #get the whole body
        b = base64.b64encode(image_raw_bytes)
        igm = Image.open(io.BytesIO(image_raw_bytes))
        igm.show()
        save_location = (os.path.join(app.root_path, "static/test.jpg")) #save to the same folder as the flask app live in
        f = open(save_location,'wb+' ) # wb for write byte data in the file instead of string
        f.write(image_raw_bytes) #write the bytes from the request body to the file
        f.close()
        print("Image saved")

        return image_raw_bytes

    if request.method == "GET": #if we make a get request (for example with a browser) show the image.
# The browser will cache this image so when you want to actually refresh it, press ctrl-f5
        return render_template("image_show.html")
    return "if you see this, that is bad request method"

app.run(host='0.0.0.0', port= 7350)