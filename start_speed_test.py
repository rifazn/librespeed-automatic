from helium import *

SPEEDTESTER_URL = "librespeed.org"
START_SELECTOR = "#startStopBtn"
FINISHED_SELECTOR = "#shareArea"

QUALITY_SELECTOR = ".testArea2"
SPEED_SELECTOR = ".testArea"

start_firefox(SPEEDTESTER_URL)
print("Firefox loaded. Waiting for site to load...")
wait_until(S(START_SELECTOR).exists, timeout_secs=30, interval_secs=1)
print("Site loaded. Waiting for test to finish...")

click(S(START_SELECTOR))
wait_until(S(FINISHED_SELECTOR).exists, timeout_secs=30, interval_secs=1)
print("Test complete.")

# Test finished, collect data
ping__jitter = find_all(S(QUALITY_SELECTOR))
ping = ': '.join(ping__jitter[0].web_element.text.split('\n'))
jitter = ': '.join(ping__jitter[1].web_element.text.split('\n'))

download__upload = find_all(S(SPEED_SELECTOR))
download = ': '.join(download__upload[0].web_element.text.split('\n'))
upload = ': '.join(download__upload[1].web_element.text.split('\n'))


print("\n%s", "  Results:  ".center(80, '*'))
print(ping)
print(jitter)
print(download)
print(upload)

kill_browser()
