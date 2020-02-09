import speech_recognition as sr

# obtain audio from the microphone
r = sr.Recognizer()
m = sr.Microphone()

dev = 0
ev = 0

def write_to_file():
    f = open('invis.txt', 'w')
    inputs = str(dev) + str(ev)
    f.write(inputs)
    f.close()

write_to_file()

with m as source:
    r.adjust_for_ambient_noise(source)
    print("Set minimum energy threshold to {}".format(r.energy_threshold))
    # r.energy_threshold = 4500
    print("Say something!")
    while(1):
        audio = r.listen(source)
        # recognize speech using Sphinx
        try:
            text = r.recognize_google(audio)
            print(text)
            if 'now you don\'t' in text:
                print("on for devin")
                dev = 1
            elif 'Now You See Me' in text:
                print("off for devin")
                dev = 0
            elif 'I don\'t know' in text:
                print("on for evan")
                ev = 1
            elif 'you' in text:
                print("off for evan")
                ev = 0
            write_to_file()
        except sr.UnknownValueError:
                pass
