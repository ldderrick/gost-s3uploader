from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile 
import time
import shutil
import subprocess
from pathlib import Path
from time import gmtime, strftime

ws = Tk()
ws.title('GOST S3 Uploader')
ws.geometry('400x200') 

def open_file():
    file_path = askopenfile(mode='r', filetypes=[('CSV Files', '*.csv')])
    if file_path is not None:
        pass

def uploadFiles():
    pb1 = Progressbar(
        ws, 
        orient=HORIZONTAL, 
        length=300, 
        mode='determinate'
        )
    pb1.grid(row=4, columnspan=3, pady=20)
    for i in range(5):
        ws.update_idletasks()
        pb1['value'] += 20
        time.sleep(1)
    pb1.destroy()
    Label(ws, text='File Uploaded Successfully!', foreground='green').grid(row=4, columnspan=3, pady=10)
    
adhar = Label(
    ws, 
    text='Upload Cobwebs'
    )
adhar.grid(row=0, column=0, padx=10)

adharbtn = Button(
    ws, 
    text ='Choose File', 
    command = lambda:open_file()
    ) 
adharbtn.grid(row=0, column=1)

dl = Label(
    ws, 
    text='Upload Social-Media'
    )
dl.grid(row=1, column=0, padx=10)

dlbtn = Button(
    ws, 
    text ='Choose File', 
    command = lambda:open_file()
    ) 
dlbtn.grid(row=1, column=1)

ms = Label(
    ws, 
    text='Upload ADID'
    )
ms.grid(row=2, column=0, padx=10)

msbtn = Button(
    ws, 
    text ='Choose File', 
    command = lambda:open_file()
    ) 
msbtn.grid(row=2, column=1)

upld = Button(
    ws, 
    text='Upload Files', 
    command=uploadFiles
    )
upld.grid(row=3, columnspan=3, pady=10)

def configure_sso():
    sso_config = ["aws", "configure", "sso"]
    sso_config = " ".join(sso_config)
    result = subprocess.run(sso_config)

def sso_login():
    global profile_name
    profile_name = input("Enter profile name to login as: ")
    sso_login = ["aws", "sso", "login", "--profile", f"{profile_name}"]
    sso_login = " ".join(sso_login)
    result = subprocess.run(sso_login)

TIMENOW=strftime("%Y%m%d",gmtime())
bucket_root='s3://gost-dev-cell'
def create_dirs():
    PARENT_FOLDER = Path("C://dev")
    global gost_dev
    gost_dev = PARENT_FOLDER / "gost-dev-cell"
    gost_dev.mkdir(parents=True, exist_ok=True)
    global arch_p
    arch_p = PARENT_FOLDER / "archive"  
    arch_p.mkdir(parents=True, exist_ok=True)

def s3_upload():
    RFI_num = input("What is the RFI Number? (e.g. RFI 00027, Enter 27) ")
    for dir_p in [gost_dev]:
        bucket_dir = dir_p.name
        for path in dir_p.glob("*.csv"):  # path is cob/filename.csv
            print(path)
            # append RFI_num and date to the original file name
            new_filename = (path.stem+"_"+RFI_num+"_"+TIMENOW+".csv")
            print(new_filename)  
            # Send file w/ RFI_num & date to S3 
            key = bucket_dir + "/" + new_filename
            dest = bucket_root + "/" + new_filename   
            # abs_path = os.path.abspath(new_filename)
            # print(abs_path)
            cmd = ["aws", "s3", "cp", str(path), str(dest), "--profile", f"{profile_name}", "--region", "us-gov-west-1"]
            cmd = " ".join(cmd)
            result = subprocess.run(cmd)
        
            if not result.returncode:
                # Move file to archive folder once successfull upload to S3
                print("Upload Successful!")
                shutil.move(path, arch_p / new_filename)
            else:
                print("Error running:  ", cmd)
                #sys.exit(-1)  # ?

ws.mainloop()