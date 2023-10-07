import deepspeech
import wave
import numpy as np
import datetime

def csv_writer(metadata):
    frame_words = ""
    frame_list = ["text,start_time,duration".split(",")]
    frame_start_time = 0
    # Loop through each character
    for i in range(0, metadata.num_items()):
        item = metadata.items[i]
        # Append character to word if it's not a space
        if item.character != " ":
            frame_words = frame_words + item.character
        # Word boundary is either a space or the last character in the array
        if (item.start_time >= 5 and item.character == " ") or i == metadata.num_items - 1:
            frame_duration = item.start_time - frame_start_time
            if frame_duration < 0:
                frame_duration = 0
            each_frame = dict()
            each_frame["text"] = frame_words
            each_frame["start_time "] = round(frame_start_time, 4)
            each_frame["duration"] = round(frame_duration, 4)
            frame_list.append(each_frame)
            # Reset
            word = ""
            word_start_time = 0
        else:
            if len(word) == 1:
                # Log the start time of the new word
                frame_start_time = item.start_time
    return frame_list

model_file_path = 'model/deepspeech-0.7.0-models.pbmm'
scorer = 'model/deepspeech-0.7.0-models.scorer'
beam_width = 500
model = deepspeech.Model(model_file_path)

lm_file_path = 'model/lm.binary'
trie_file_path = 'model/trie'
lm_alpha = 0.75
lm_beta = 1.85

model.setBeamWidth(beam_width)
model.enableExternalScorer(scorer)
model.setScorerAlphaBeta(lm_alpha, lm_beta)

#model.enableDecoderWithLM(scorer)
filename = 'dataset/audio/1.wav'
w = wave.open(filename, 'r')
rate = w.getframerate()
frames = w.getnframes()
buffer = w.readframes(frames)
data16 = np.frombuffer(buffer, dtype=np.int16)
type(data16)
#text = csv_writer(model.sttWithMetadata(data16))
text = model.stt(data16)

#print(text.transcripts.count())
print(text)

output = open("output/out.txt", "a+")
output.write('\n' + "Date: " + str(datetime.datetime.now()) + '\n' + text + '\r\n')
output.close



# 	with open(path, "w", newline='') as csv_file:
# 	 writer = csv.writer(csv_file, delimiter=',')
# 	 for line in data:
# 	   writer.writerow(line)