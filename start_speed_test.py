import sys
from helium import *

HEADLESS = sys.argv.count('--headless') > 0

SPEEDTESTER_URL = "librespeed.org"
START_SELECTOR = "#startStopBtn"
FINISHED_SELECTOR = "#shareArea"

QUALITY_SELECTOR = ".testArea2"
SPEED_SELECTOR = ".testArea"

start_firefox(SPEEDTESTER_URL, headless=HEADLESS)
print("Firefox loaded. Waiting for site to load...")
wait_until(S(START_SELECTOR).exists, timeout_secs=30, interval_secs=1)
print("Site loaded. Waiting for test to finish...")

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


print()
print("  Results:  ".center(60, '*'))
print(ping, jitter, download, upload, sep='\n')

kill_browser()
