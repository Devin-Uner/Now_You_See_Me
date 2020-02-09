import speech_recognition as sr

# obtain audio from the microphone
r = sr.Recognizer()
m = sr.Microphone()
with m as source:
    r.adjust_for_ambient_noise(source)
    print("Set minimum energy threshold to {}".format(r.energy_threshold))
    # r.energy_threshold = 1000
    print("Say something!")
    while(1):
        audio = r.listen(source)
        print("recognizing now...")
        # recognize speech using Sphinx
        try:
            text = r.recognize_google(audio)
            print(text)
            if 'now you don\'t' in text:
                print("on")
                f = open('invis.txt', 'w')
                f.write('1')
                f.close()
            elif 'Now You See Me' in text:
                print("off")
                f = open('invis.txt', 'w')
                f.write('0')
                f.close()
        except sr.UnknownValueError:
                pass
