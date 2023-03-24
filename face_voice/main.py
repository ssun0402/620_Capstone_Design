import multiprocessing
import subprocess

if __name__ == '__main__':
    p1 = multiprocessing.Process(target=subprocess.Popen, args=(["python", "face_win.py"],))
    p2 = multiprocessing.Process(target=subprocess.Popen, args=(["python", "respeak6.py"],))

    p1.start()
    p2.start()

    p1.join()
    p2.join()