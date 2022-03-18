import subprocess
import time

def measure_temp():
    out = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("utf-8")
    temp = float(out.replace("temp=", "").replace("'C", ""))
    print('Run: measure_temp() ', temp)
    return temp

def measure_core_frequency():
    out = subprocess.check_output(["vcgencmd", "measure_clock arm"]).decode("utf-8")
    frequency = float(out.split("=")[1]) / 1000000
    print('Run: measure_core_frequency() ', frequency)
    return frequency

def cooldown(interval=40, threshold=0.2):
    prev_temp = measure_temp()
    while True:
        print("attempting cooldown")
        time.sleep(interval)
        temp = measure_temp()
        print(
            f"Current temperature: {temp:4.1f}°C - "
            f"Previous temperature: {prev_temp:4.1f}°C"
        )
        if abs(temp - prev_temp) < threshold:
            break
        prev_temp = temp
    return temp

def measure_timer(duration=305):
    time.sleep(duration)
    
def write_measurements(testingRecordsFilePath, times, temperatures, frequencies):
    testFile = open(testingRecordsFilePath, 'w')
    
    testFile.write('times = [ \n')
    for time in times:
        testFile.write(str(time))
        testFile.write('\n')
    testFile.write('] \n')
    
    testFile.write('temperatures = [ \n')
    for temperature in temperatures:
        testFile.write(str(temperature))
        testFile.write('\n')
    testFile.write('] \n')

    testFile.write('frequencies = [ \n')
    for frequency in frequencies:
        testFile.write(str(frequency))
        testFile.write('\n')
    testFile.write('] \n')