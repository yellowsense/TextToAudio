from flask import Flask, jsonify, send_file, make_response
import logging
import pyodbc
import azure.cognitiveservices.speech as speechsdk
import time

app = Flask(__name__)

# Database connection setup
SERVER = 'maidsqlppserver.database.windows.net'
DATABASE = 'miadsqlpp'
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

@app.route('/synthesize', methods=['GET'])
def synthesize_and_download():
    try:
        # Assuming you have the database connection and cursor available
        cursor.execute('''
            SELECT TOP 1 servicetype, starttime, apartment, area, startdate, customernumber, serviceprovider_number, serviceprovider_name
            FROM dynamic_greeting
            ORDER BY id DESC
        ''')
        latest_data = cursor.fetchone()

        if not latest_data:
            return jsonify({'message': 'No data available'}), 404

        # Extracting data from the database
        servicetype = latest_data.servicetype
        starttime = latest_data.starttime
        apartment = latest_data.apartment
        area = latest_data.area
        startdate = latest_data.startdate
        serviceprovider_name = latest_data.serviceprovider_name

        # Generating greeting text
        location = apartment if apartment else area
        greeting_text = f"नमस्ते {serviceprovider_name},\n येलोसेंस में आपका स्वागत है! किसी {location} से कॉल किया है और आपकी {servicetype} सेवा के लिए बुकिंग की है।\n"
        if starttime:
            greeting_text += f"{starttime} पर काम शुरू करने के लिए"
        greeting_text += f" {startdate} को।\n"
        greeting_text += "कृपया 1 दबाकर booking की confirm। reject के लिए, 2 दबाएँ।"

        # Perform text-to-speech synthesis
        speech_key = "3757c00a36324059afa95cff5ed8731d"
        service_region = "centralindia"
        voice_name = "hi-IN-MadhurNeural"
        audio_file = text_to_speech(greeting_text, speech_key, service_region, voice_name)

        if audio_file:
            # Set appropriate headers for the audio file
            headers = {
                'Content-Disposition': f'attachment; filename="{audio_file}"',
                'Content-Type': 'audio/wav'
            }
            # Create response object
            response = make_response(send_file(audio_file, as_attachment=True))
            # Set headers for the response
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
        # Set the speech configuration
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

        # Customize the audio output format
        speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Riff8Khz16BitMonoPcm)

        # Set the audio output file name with a timestamp
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        file_name = f"outputaudio_{timestamp}.wav"
        
        # Create an audio config with custom settings
        audio_config = speechsdk.audio.AudioOutputConfig(filename=file_name)

        # Create a speech synthesizer using the configured speech and audio output
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        logging.info("Speech synthesizer initialized successfully.")

        # Synthesize the text with adjusted speaking rate using SSML
        ssml = f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="hi-IN"><voice name="{voice_name}"><prosody rate="-5.0%">{text}</prosody></voice></speak>'

        # Synthesize the text
        result = speech_synthesizer.speak_ssml_async(ssml).get()

        # Check the result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            logging.info("Speech synthesis is complete.")
            return file_name
        else:
            logging.error("Error synthesizing speech: %s", result.reason)
            return None
    except Exception as e:
        logging.error("An error occurred during text-to-speech synthesis: %s", e)
        return None
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)  # Set logging level to INFO
    app.run(debug=True)