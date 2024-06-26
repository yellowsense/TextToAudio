from flask import Flask, jsonify, send_file, make_response
import logging
import pyodbc
import azure.cognitiveservices.speech as speechsdk
import time
import uuid

app = Flask(__name__)

# Database connection setup
SERVER = 'serviceproviderdatasqlsever.database.windows.net'
DATABASE = 'Yellowsensesqldatabase'
USERNAME = 'ysadmin'
PASSWORD = 'yellowsense@1234'
connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'

try:
    with pyodbc.connect(connectionString) as conn:
        app.logger.info("Connected to the database.")
        cursor = conn.cursor()
except pyodbc.Error as e:
    app.logger.error("Error connecting to the database: %s", e)
    raise


# @app.route('/synthesize', methods=['GET'])
# def synthesize_and_download():
#     try:
#         # Assuming you have the database connection and cursor available
#         cursor.execute('''
#             SELECT TOP 1 servicetype, starttime, apartment, area, startdate
#             FROM dynamic_greeting
#             ORDER BY id DESC
#         ''')
#         latest_data = cursor.fetchone()

#         if not latest_data:
#             return jsonify({'message': 'No data available'}), 404

#         # Extracting data from the database
#         servicetype = latest_data.servicetype
#         starttime = latest_data.starttime
#         apartment = latest_data.apartment
#         area = latest_data.area
#         startdate = latest_data.startdate

#         # Generating greeting text
#         location = apartment if apartment else area
#         greeting_text = f"नमस्ते येलोसेंस में आपका स्वागत है! किसी {location} से कॉल किया है और आपकी {servicetype} सेवा के लिए बुकिंग की है।\n"
#         if starttime:
#             greeting_text += f"{starttime} पर काम शुरू करने के लिए"
#         greeting_text += f" {startdate} को।\n"
#         greeting_text += "कृपया 1 दबाकर booking की confirm। reject के लिए, 2 दबाएँ।"

#         # Perform text-to-speech synthesis
#         speech_key = "3757c00a36324059afa95cff5ed8731d"
#         service_region = "centralindia"
#         voice_name = "hi-IN-MadhurNeural"
#         audio_file = text_to_speech(greeting_text, speech_key, service_region, voice_name)

#         if audio_file:
#             # Set appropriate headers for the audio file
#             headers = {
#                 'Content-Disposition': f'attachment; filename="{audio_file}"',
#                 'Content-Type': 'audio/wav'
#             }
#             # Create response object
#             response = make_response(send_file(audio_file, as_attachment=True))
#             # Set headers for the response
#             for key, value in headers.items():
#                 response.headers[key] = value
#             return response
#         else:
#             return "Error synthesizing speech", 500

#     except Exception as e:
#         logging.exception("An error occurred")
#         return "An error occurred", 500
    
# def text_to_speech(text, speech_key, service_region, voice_name):
#     try:
#         # Set the speech configuration
#         speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

#         # Customize the audio output format
#         speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Riff8Khz16BitMonoPcm)

#         # Set the audio output file name with a timestamp
#         timestamp = time.strftime("%Y%m%d-%H%M%S")
#         file_name = f"outputaudio_{timestamp}.wav"
        
#         # Create an audio config with custom settings
#         audio_config = speechsdk.audio.AudioOutputConfig(filename=file_name)

#         # Create a speech synthesizer using the configured speech and audio output
#         speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
#         logging.info("Speech synthesizer initialized successfully.")

#         # Synthesize the text with adjusted speaking rate using SSML
#         ssml = f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="hi-IN"><voice name="{voice_name}"><prosody rate="-5.0%">{text}</prosody></voice></speak>'

#         # Synthesize the text
#         result = speech_synthesizer.speak_ssml_async(ssml).get()

#         # Check the result
#         if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
#             logging.info("Speech synthesis is complete.")
#             return file_name
#         else:
#             logging.error("Error synthesizing speech: %s", result.reason)
#             return None
#     except Exception as e:
#         logging.error("An error occurred during text-to-speech synthesis: %s", e)
#         return None

@app.route('/dynamicgreeting', methods=['GET'])
def synthesize_and_download():
    try:
        cursor.execute("""
            SELECT TOP 1 servicetype, starttime, apartment, area, startdate
            FROM dynamic_greeting
            ORDER BY id DESC
        """)
        latest_data = cursor.fetchone()

        if not latest_data:
            return jsonify({'message': 'No data available'}), 404

        servicetype = latest_data.servicetype
        starttime = latest_data.starttime
        apartment = latest_data.apartment
        area = latest_data.area
        startdate = latest_data.startdate

        location = apartment if apartment else area
        greeting_text = f"नमस्ते येलोसेंस में आपका स्वागत है! किसी {location} से कॉल किया है और आपकी {servicetype} सेवा के लिए बुकिंग की है।\n"
        if starttime:
            greeting_text += f"{starttime} पर काम शुरू करने के लिए"
        greeting_text += f" {startdate} को।\n"
        greeting_text += "कृपया 1 दबाकर booking की confirm। reject के लिए, 2 दबाएँ।"

        speech_key = "3757c00a36324059afa95cff5ed8731d"
        service_region = "centralindia"
        voice_name = "hi-IN-MadhurNeural"
        audio_file_name = text_to_speech(greeting_text, speech_key, service_region, voice_name)

        if audio_file_name:
            headers = {
                'Content-Disposition': f'attachment; filename="{audio_file_name}"',
                'Content-Type': 'audio/wav'
            }
            response = make_response(send_file(audio_file_name, as_attachment=True))
            for key, value in headers.items():
                response.headers[key] = value
            return response
        else:
            return "Error synthesizing speech", 500

    except Exception as e:
        logging.exception("An error occurred")
        return "An error occurred", 500

def text_to_speech(text, speech_key, service_region, voice_name):
    try:
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Riff8Khz16BitMonoPcm)
        #Riff8Khz8BitMonoMULaw
        # Generate a unique identifier for the audio file name
        unique_id = str(uuid.uuid4())[:8]  # Using the first 8 characters of UUID
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        audio_file_name = f"greetingaudio_{timestamp}_{unique_id}.wav"  
        # timestamp = time.strftime("%Y%m%d-%H%M%S")
        # audio_file_name = f"greetingaudio_{timestamp}.wav"
        audio_config = speechsdk.audio.AudioOutputConfig(filename=audio_file_name)
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        logging.info("Speech synthesizer initialized successfully.")
        ssml = f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="hi-IN"><voice name="{voice_name}"><prosody rate="-5.0%">{text}</prosody></voice></speak>'
        result = speech_synthesizer.speak_ssml_async(ssml).get()
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            logging.info("Speech synthesis is complete.")
            return audio_file_name
        else:
            logging.error("Error synthesizing speech: %s", result.reason)
            return None
    except Exception as e:
        logging.error("An error occurred during text-to-speech synthesis: %s", e)
        return None

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)  # Set logging level to INFO
    app.run(debug=True)
