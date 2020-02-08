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
		print("got it! analyzing...")
		# recognize speech using Sphinx
		try:
			print("command recognized as " + r.recognize_google(audio))
		except sr.UnknownValueError:
			print("stupid google could not understand audio")