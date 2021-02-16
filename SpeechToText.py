import speech_recognition as sr
import os, os.path
import math 
import glob
from pydub import AudioSegment

files = glob.glob('D:/Programming/Python/speech-to-text-hu/audio/Splitted/*')
for f in files:
    os.remove(f)

#Splits audio
class SplitWavAudioMubin():
    def __init__(self, folder, filename):
        self.folder = folder
        self.filename = filename
        self.filepath = folder + '\\' + filename
        
        self.audio = AudioSegment.from_wav(self.filepath)
    
    def get_duration(self):
        return self.audio.duration_seconds
    
    def single_split(self, from_min, to_min, split_filename):
        t1 = from_min * 60 * 1000
        t2 = to_min * 60 * 1000
        split_audio = self.audio[t1:t2]
        split_audio.export((self.folder+"/Splitted") + '\\' + split_filename, format="wav")
        
    def multiple_split(self, min_per_split):
        total_mins = math.ceil(self.get_duration() / 60)
        for i in range(0, total_mins, min_per_split):
            split_fn = str(i) + '_' + 'out.wav'
            self.single_split(i, i+min_per_split, split_fn)
            if i == total_mins - min_per_split:
                print('Audio file is splitted successfully')

def AudioToText(LANGUAGE_TO_TRANSLATE):
    progress = 0
    fh = open("transcription.txt", "w+")
    flog = open("transcription.log", "w+")
    files = next(os.walk("D:/Programming/Python/speech-to-text-hu/audio/Splitted"))
    file_count = len(files)
    for i in range(0, file_count):      # set the range of the chunks
        progress += math.floor(100/file_count)
        filename = 'audio/Splitted/'+str(i)+'_out'+'.wav'
        print(f'Loading.. {progress}%\n')
        file = filename

        r = sr.Recognizer()
        with sr.AudioFile(file) as source:
    #        r.adjust_for_ambient_noise(source, duration=4000)
            audio = r.listen(source)
    
        # try converting it to text 
        try:
            rec = r.recognize_google(audio, language = LANGUAGE_TO_TRANSLATE)
            fh.write(rec+". \n") 
    
            # catch any errors    
        except sr.UnknownValueError:
            flog.write(f"file = {filename}: could not understand audio")
        
        except sr.RequestError as e:
            flog.write(f"file = {filename}: could not request results. check you internet connection")




#Initialize Path Object
folder = 'D:/Programming/Python/speech-to-text-hu/audio' #Add audio path
file = 'test.wav' #Add ur audio file
split_wav = SplitWavAudioMubin(folder, file)

#Duration of split
split_wav.multiple_split(min_per_split=1)


LANGUAGE_TO_TRANSLATE = "hu-HU"
AudioToText(LANGUAGE_TO_TRANSLATE)




