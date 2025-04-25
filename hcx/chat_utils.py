import time

def streaming_data(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.05)
