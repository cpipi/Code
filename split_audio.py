from pydub import AudioSegment
from pydub.utils import make_chunks
import webrtcvad

vad = webrtcvad.Vad()

audio_name = "example"
audio_format = ".wav"
catalog_dir = "dataset/"


myaudio = AudioSegment.from_file(catalog_dir + audio_name + audio_format, "wav") 
chunk_length_ms = 1000 # pydub calculates in millisec
chunks = make_chunks(myaudio, chunk_length_ms) #Make chunks of one sec

#Export all of the individual chunks as wav files

for i, chunk in enumerate(chunks):
    chunk_name = catalog_dir + audio_name + "_chunks/" + audio_name + str(i) + audio_format
    print "exporting", chunk_name
    chunk.export(chunk_name, format="wav")