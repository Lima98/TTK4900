# variation.py
def transpose(phrase, interval):
    return [ (note+interval, dur) for note, dur in phrase ]
