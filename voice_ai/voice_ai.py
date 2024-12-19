## speech to text: 


import azure.cognitiveservices.speech as speechsdk # type: ignore
import openai #type: ignore
import time 

def recognize_speech():
    
    subscription_key = "1q7Fk9WN4prsuLN88wY4pKMKDK40wIQMZCn7T8d8iqrV4wH3nEjfJQQJ99AKACYeBjFXJ3w3AAAYACOGP8PB"
    region = "eastus"
    speech_config = speechsdk.SpeechConfig(subscription = subscription_key, region = region)
    speech_config.speech_recognition_language = 'en-US' # setting up the language for speech recognition as english
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True) #  creating an audio configuration
    # Creating a speech recognizer: 
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config = speech_config, audio_config = audio_config)
    def speech_recognized_handler(event): # this function prints the recognized text (event.result.text)
        global recognized_text
        recognized_text = event.result.text
        print(f"{event.result.text}")
        
    speech_recognizer.recognized.connect(speech_recognized_handler) # connecting the handler to the recognizer

    print("Listening...Press Ctrl+C to stop.")
    speech_recognizer.start_continuous_recognition()

    try:
        while True:
            time.sleep(0.3)
    except KeyboardInterrupt: # pressing Ctrl+C triggers the KeyboardInterrupt
        print("Stopping recognition...")

    speech_recognizer.stop_continuous_recognition()
    
    return recognized_text

## text to speech: 

def get_text_from_azure_openai(prompt):
    openai.api_key = "AK1dtQFdwdvIlln6vT9Sr1Xhwo1L3F19ISTnScOpLY1GNamDNFWsJQQJ99AKACfhMk5XJ3w3AAAAACOGcw1x" # set your openai API key from azure here
    openai.api_base = "https://aagha-m3u87en8-swedencentral.cognitiveservices.azure.com/" # endpoint from azure
    openai.api_type = "azure"
    openai.api_version = "2024-08-01-preview"
    response = openai.ChatCompletion.create(
        engine = "gpt-4-32k", # model using
        messages = [{"role" : "user", "content": prompt}]
        )
    return response['choices'][0]['message']['content']


def text_to_speech_from_azure(text):
    subscription_key = "1q7Fk9WN4prsuLN88wY4pKMKDK40wIQMZCn7T8d8iqrV4wH3nEjfJQQJ99AKACYeBjFXJ3w3AAAYACOGP8PB" 
    # API key1 of Azure
    region = "eastus" # Azure region
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region = region) # this tells Azure that your application has permission to use its Text-to-Speech service.
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True) # this tells Azure to play the audio using your computer's default audio device (like speakers or headphones)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config = speech_config, audio_config = audio_config)
    # this connects the speech configuration (your API Key and Region) with the audio output configuration (your speaker settings).
    # Creates the object (synthesizer) that you’ll use to generate speech from text.
    synthesizer.speak_text_async(text).get()

## text to text:

# import openai #type: ignore
def get_text_from_azure_openai(prompt):
    openai.api_key = "AK1dtQFdwdvIlln6vT9Sr1Xhwo1L3F19ISTnScOpLY1GNamDNFWsJQQJ99AKACfhMk5XJ3w3AAAAACOGcw1x" # set your openai API key from azure here
    openai.api_base = "https://aagha-m3u87en8-swedencentral.cognitiveservices.azure.com/" # endpoint from azure
    openai.api_type = "azure"
    openai.api_version = "2024-08-01-preview"

    response = openai.ChatCompletion.create(
        engine = "gpt-4-32k", # model using
        messages = [{"role" : "user", "content": prompt}]
        )
    return response['choices'][0]['message']['content']


# main: 

# getting user input (voice)
# print("Please Speak")
# recognized_text = recognize_speech()
# print(f"Recognized text:\n{recognized_text}")

# response_text = get_text_from_azure_openai(recognized_text)
# text_to_speech_from_azure(response_text)
# print(f"Response:\n{response_text}")

# print("Do you want to conversate by speech or text?")
choice = input("Press 0 for text and 1 for speech: ")

# Convert the input to an integer
choice = int(choice)

if choice == 0:
    recognized_text_input = input("Please type: ")
    response_text = get_text_from_azure_openai(recognized_text_input)
    print(f"Recognized Text: {recognized_text_input}")
    print(f"Response: {response_text}")

elif choice == 1:
    print("Please Speak")
    recognized_text = recognize_speech()
    response_text = get_text_from_azure_openai(recognized_text)
    text_to_speech_from_azure(response_text)
    print(f"Response:\n{response_text}")
