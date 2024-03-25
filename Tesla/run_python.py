import os
import multiprocessing
import subprocess

# 실행할 파이썬 파일들의 경로 리스트
scripts = ['Tesla_Read_CH1.py', 'Tesla_Read_CH3.py', 'Tesla_Read_CH4.py']

def run_script(script):
    try:
        subprocess.run(['python', script,], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script}: {e}")

if __name__ == "__main__":
    processes = []
    for script in scripts:
        process = multiprocessing.Process(target=run_script, args=(script, ))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
