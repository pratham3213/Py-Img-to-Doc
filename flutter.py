from ast import Lambda
from email.mime import image
from PIL import ImageTk,Image
from tkinter import *
from attr import define
import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup
#from urllib import request
img_list=[]	
def getdata():
    query=input("What do you wanna search?\n:-")
    query='+'.join(query.split())
#    query1='-'.join(query.split())
    payload={'tbm':'isch',"q":query,'ie':'UTF-8'}
    page=requests.get('https://www.google.com/search', params=payload)
#    pexel=requests.get(f"https://pexel.com/search/{query1}/")
#    usplash=requests.get(f'https://usplash.com/s/photos/{query1}')
    urls=[]
    soup = BeautifulSoup(page.content, 'html.parser')
    for item in tqdm(soup.find_all('img'),'Extracting Images'):
        img_url=item.attrs.get("src")
        if '.gif' in img_url:
            continue
        urls.append(img_url)
    return urls

def download(url,img_counter):
    
    imgpath="img-app"
    # if path doesn't exist, make that path dir
    if not os.path.isdir(imgpath):
        os.makedirs(imgpath)
    # download the body of response by chunk, not immediately
    response = requests.get(url)
    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))
    # get the file name
    global filename
    filename = os.path.join(imgpath, f"{str(img_counter)}.jpeg")
    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for data in progress.iterable:
            # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))
    img_list.append(filename)
    img_show(filename)

def main():
    img_counter=0
    # get all images
    imgs = getdata()
    for img in imgs:
        # for each image, download it
        download(img,img_counter)
        img_counter+=1

def img_show(filename):
    def forward():
        global my_label
        global button_next
        global button_back
        my_label.grid_forget()
        my_label=Label(image=)

    def back():
        global my_label
        global button_next
        global button_back

    root=Tk()
    root.title("Image Downloader")
    my_img=ImageTk.PhotoImage(Image.open(filename))
    mylabel=Label(image=my_img)
    mylabel.grid(row=0,column=0,columnspan=3)
    button_next=Button(root, text="Next Image")
    button_back=Button(root, text="Previous Image")
    button_exit=Button(root, text="Exit", command=root.quit)
    button_back.grid(row=1,column=0)
    button_exit.grid(row=1,column=1)
    button_next.grid(row=1,column=2)

    root.mainloop()

main()