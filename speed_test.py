import sys, time, datetime
from helium import *

HEADLESS = sys.argv.count('--headless') > 0

SPEEDTESTER_URL = "librespeed.org"
START_SELECTOR = "#startStopBtn"
FINISHED_SELECTOR = "#shareArea"

QUALITY_SELECTOR = ".testArea2"
SPEED_SELECTOR = ".testArea"
SERVERS_SELECTOR = 'Server'

TIMENOW = datetime.datetime.now().isoformat()

start_firefox(SPEEDTESTER_URL, headless=HEADLESS)
print("Firefox loaded. Waiting for site to load...")
wait_until(S(START_SELECTOR).exists, timeout_secs=90, interval_secs=1)
print("Site loaded. Gathering servers list...")

server_selector = ComboBox(SERVERS_SELECTOR)
servers_list = server_selector.options

def run_test():
    for server in servers_list:
        print(f"  {server}  ".center(60, '*'))
    select(server_selector, server)

    # Start test
    click(S(START_SELECTOR))
    wait_until(S(FINISHED_SELECTOR).exists, timeout_secs=90, interval_secs=1)
    print("\nTest complete.")

    # Test finished, collect data
    ping__jitter = find_all(S(QUALITY_SELECTOR))
    ping = ': '.join(ping__jitter[0].web_element.text.split('\n'))
    jitter = ': '.join(ping__jitter[1].web_element.text.split('\n'))

    download__upload = find_all(S(SPEED_SELECTOR))
    download = ': '.join(download__upload[0].web_element.text.split('\n'))
    upload = ': '.join(download__upload[1].web_element.text.split('\n'))


    # Print results
    print()
    print(ping, jitter, download, upload, sep='\n')

    # Save results
    dl = ''.join(download.split(':')[1:])
    ul = ''.join(upload.split(':')[1:])
    with open('test-results.csv', 'a') as out:
        out.write(f'{TIMENOW}, {server}, {ping}, {jitter}, {dl}, {ul}\n')
    print('Results saved.')

while True:
    print('Starting test at', TIMENOW)
    try:
        run_test()
    except Exception as err:
        print(err)
    time.sleep(60 * 30) # 30 mins

kill_browser()
