import nltk
from gtts import gTTS
from speech_recognition import Recognizer, Microphone
from IPython.display import Audio, display

nltk.download('punkt')

# Braille and punctuation mappings
braille_dict = {
    'a': '100000', 'b': '101000', 'c': '110000', 'd': '110100', 'e': '100100',
    'f': '111000', 'g': '111100', 'h': '101100', 'i': '011000', 'j': '011100',
    'k': '100010', 'l': '101010', 'm': '110010', 'n': '110110', 'o': '100110',
    'p': '111010', 'q': '111110', 'r': '101110', 's': '011010', 't': '011110',
    'u': '100011', 'v': '101011', 'w': '011101', 'x': '110011', 'y': '110111',
    'z': '100111', ' ': '000000'  # Space
}

unicode_braille_map = {
    '100000': '⠁', '101000': '⠃', '110000': '⠉', '110100': '⠙', '100100': '⠑',
    '111000': '⠋', '111100': '⠛', '101100': '⠓', '011000': '⠊', '011100': '⠚',
    '100010': '⠅', '101010': '⠇', '110010': '⠍', '110110': '⠝', '100110': '⠕',
    '111010': '⠏', '111110': '⠟', '101110': '⠗', '011010': '⠎', '011110': '⠧',
    '100011': '⠥', '101011': '⠧', '011101': '⠺', '110011': '⠭', '110111': '⠽',
    '100111': '⠵', '000000': '⠠'  # Space
}

punctuation_unicode_map = {
    '.': '⠲', ',': '⠂', '?': '⠦', '!': '⠖', ';': '⠆', ':': '⠒', '"': '⠶',
    "'": '⠄', '(': '⠷', ')': '⠾', '-': '⠤'
}

# Convert text to Braille
def convert_to_braille_unicode(text):
    text = text.lower()  # Convert to lowercase
    tokens = nltk.word_tokenize(text)  # Tokenize text
    braille_output = []

    for token in tokens:
        for char in token:
            if char in braille_dict:
                braille_output.append(unicode_braille_map[braille_dict[char]])
            elif char in punctuation_unicode_map:
                braille_output.append(punctuation_unicode_map[char])
            elif char.isdigit():
                braille_output.append('⠴')  # Number sign
                braille_output.append(unicode_braille_map[braille_dict[char]])
            elif char == ' ':
                braille_output.append('⠠')  # Space
            else:
                braille_output.append('⠿')  # Placeholder for unknown characters
    return ''.join(braille_output)

# Speech-to-text function
def speech_to_text():
    recognizer = Recognizer()
    with Microphone() as source:
        print("Speak now...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"Recognized Text: {text}")
            return text
        except Exception as e:
            print(f"Error: {e}")
            return None

# Text-to-speech function
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")
    return "output.mp3"

# Play the audio file
def play_audio(audio_file):
    display(Audio(audio_file, autoplay=True))

# Main execution
print("Choose an option:\n1. Enter text manually\n2. Convert speech to Braille")
choice = input("Enter your choice (1/2): ")

if choice == '1':
    input_text = input("Enter your text: ")
elif choice == '2':
    input_text = speech_to_text()
else:
    print("Invalid choice!")
    input_text = None

if input_text:
    braille_unicode = convert_to_braille_unicode(input_text)
    print("Original Text:", input_text)
    print("Unicode Braille Representation:", braille_unicode)
    audio_file = text_to_speech(input_text)
    play_audio(audio_file)
