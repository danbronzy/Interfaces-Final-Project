'''
import pyaudio  
import wave  
import threading


class threadedSoundPlayer(threading.Thread):
    
    def __init__(self, wavName):
        self.wavName = wavName
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()
        
    def run(self):
        
        chunk = 1024  

        f = wave.open(self.wavName,"rb")  

        p = pyaudio.PyAudio()  

        stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                        channels = f.getnchannels(),  
                        rate = f.getframerate(),  
                        output = True)  
        data = f.readframes(chunk)  

        while data:  
            stream.write(data)  
            data = f.readframes(chunk)  

        stream.stop_stream()  
        stream.close()  

        p.terminate()
'''