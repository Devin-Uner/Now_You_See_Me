import speech_recognition as sr

# obtain audio from the microphone
r = sr.Recognizer()
m = sr.Microphone()
with m as source:
        # r.adjust_for_ambient_noise(source)
        # print("Set minimum energy threshold to {}".format(r.energy_threshold))
        r.energy_threshold = 100
        print("Say something!")
        while(1):
                audio = r.listen(source)
                # recognize speech using Sphinx
                try:
                        if r.recognize_google(audio) == 'abracadabra':
				f = open('invis.txt', 'w')
				f.write('1')
			elif r.recognize_google(audio) == 'off':
				f = open('invis.txt', 'w')
				f.write('0')
			f.close()
                except sr.UnknownValueError:
			pass
