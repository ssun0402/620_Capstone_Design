from face_win import nn 
from respeak3 import  ree, re
from face_win import star
from respeak3 import speak_jetson
import threading
import multiprocessing as Process

p0 = Process(target=star)
p1 = Process(target=speak_jetson)
p0.start()
p1.start()

p0.join()
p1.join()