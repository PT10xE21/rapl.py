import time

fp = '/sys/devices/virtual/powercap/intel-rapl/intel-rapl:0/energy_uj'
multiplier_j = 1000000
start_time = time.time()
start_pwr = 0
sleep = 2
col_spacing = 25

file = open(fp, 'r')
start_pwr = int(file.read().strip())
prev_pwr = 0
prev_time = 0
watts_since_last = 0
headers = ['time', 'J since start', 'w since start', 'w since last poll']

header_str = ''.join(x + ' ' * (col_spacing - len(x)) for x in headers)
print(header_str)

while True:
    file.seek(0)
    pwr_uj = int(file.read().strip())
    pwr_since_start = pwr_uj - start_pwr
    pwr_j = pwr_since_start / multiplier_j

    now = time.time()
    sample_time = now - start_time
    watts = 0
    if sample_time > 0:
        watts = pwr_j / sample_time

    if prev_time > 0:
        watts_since_last = (pwr_j - prev_pwr) / (now - prev_time)
    last_watts_str = f'{watts_since_last:.3f}w' if watts_since_last > 0 else "0"

    data = [str(int(now)), f'{pwr_j:.3f}J', f'{watts:.3f}w', last_watts_str]
    data_str = ''.join(x + ' ' * (col_spacing - len(x)) for x in data)

    print(data_str, end='\r')

    prev_pwr = pwr_j
    prev_time = now

    time.sleep(sleep)