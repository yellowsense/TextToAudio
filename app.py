# from flask import Flask, jsonify, send_file, make_response
# import logging
# import pyodbc
# import azure.cognitiveservices.speech as speechsdk
# import time
# import uuid

# app = Flask(__name__)


# # Database connection setup
# SERVER = 'serviceproviderdatasqlsever.database.windows.net'
# DATABASE = 'Yellowsensesqldatabase'
# USERNAME = 'ysadmin'
# PASSWORD = 'yellowsense@1234'
# connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'

# try:
#     with pyodbc.connect(connectionString) as conn:
#         app.logger.info("Connected to the database.")
#         cursor = conn.cursor()
# except pyodbc.Error as e:
#     app.logger.error("Error connecting to the database: %s", e)
#     raise


# # @app.route('/synthesize', methods=['GET'])
# # def synthesize_and_download():
# #     try:
# #         # Assuming you have the database connection and cursor available
# #         cursor.execute('''
# #             SELECT TOP 1 servicetype, starttime, apartment, area, startdate
# #             FROM dynamic_greeting
# #             ORDER BY id DESC
# #         ''')
# #         latest_data = cursor.fetchone()

# #         if not latest_data:
# #             return jsonify({'message': 'No data available'}), 404

# #         # Extracting data from the database
# #         servicetype = latest_data.servicetype
# #         starttime = latest_data.starttime
# #         apartment = latest_data.apartment
# #         area = latest_data.area
# #         startdate = latest_data.startdate

# #         # Generating greeting text
# #         location = apartment if apartment else area
# #         greeting_text = f"नमस्ते येलोसेंस में आपका स्वागत है! किसी {location} से कॉल किया है और आपकी {servicetype} सेवा के लिए बुकिंग की है।\n"
# #         if starttime:
# #             greeting_text += f"{starttime} पर काम शुरू करने के लिए"
# #         greeting_text += f" {startdate} को।\n"
# #         greeting_text += "कृपया 1 दबाकर booking की confirm। reject के लिए, 2 दबाएँ।"

# #         # Perform text-to-speech synthesis
# #         speech_key = "3757c00a36324059afa95cff5ed8731d"
# #         service_region = "centralindia"
# #         voice_name = "hi-IN-MadhurNeural"
# #         audio_file = text_to_speech(greeting_text, speech_key, service_region, voice_name)

# #         if audio_file:
# #             # Set appropriate headers for the audio file
# #             headers = {
# #                 'Content-Disposition': f'attachment; filename="{audio_file}"',
# #                 'Content-Type': 'audio/wav'
# #             }
# #             # Create response object
# #             response = make_response(send_file(audio_file, as_attachment=True))
# #             # Set headers for the response
# #             for key, value in headers.items():
# #                 response.headers[key] = value
# #             return response
# #         else:
# #             return "Error synthesizing speech", 500

# #     except Exception as e:
# #         logging.exception("An error occurred")
# #         return "An error occurred", 500
    
# # def text_to_speech(text, speech_key, service_region, voice_name):
# #     try:
# #         # Set the speech configuration
# #         speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# #         # Customize the audio output format
# #         speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Riff8Khz16BitMonoPcm)

# #         # Set the audio output file name with a timestamp
# #         timestamp = time.strftime("%Y%m%d-%H%M%S")
# #         file_name = f"outputaudio_{timestamp}.wav"
        
# #         # Create an audio config with custom settings
# #         audio_config = speechsdk.audio.AudioOutputConfig(filename=file_name)

# #         # Create a speech synthesizer using the configured speech and audio output
# #         speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
# #         logging.info("Speech synthesizer initialized successfully.")

# #         # Synthesize the text with adjusted speaking rate using SSML
# #         ssml = f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="hi-IN"><voice name="{voice_name}"><prosody rate="-5.0%">{text}</prosody></voice></speak>'

# #         # Synthesize the text
# #         result = speech_synthesizer.speak_ssml_async(ssml).get()

# #         # Check the result
# #         if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
# #             logging.info("Speech synthesis is complete.")
# #             return file_name
# #         else:
# #             logging.error("Error synthesizing speech: %s", result.reason)
# #             return None
# #     except Exception as e:
# #         logging.error("An error occurred during text-to-speech synthesis: %s", e)
# #         return None

# @app.route('/dynamicgreeting', methods=['GET'])
# def synthesize_and_download():
#     try:
#         cursor.execute("""
#             SELECT TOP 1 servicetype, starttime, apartment, area, startdate
#             FROM dynamic_greeting
#             ORDER BY id DESC
#         """)
#         latest_data = cursor.fetchone()

#         if not latest_data:
#             return jsonify({'message': 'No data available'}), 404

#         servicetype = latest_data.servicetype
#         starttime = latest_data.starttime
#         apartment = latest_data.apartment
#         area = latest_data.area
#         startdate = latest_data.startdate

#         location = apartment if apartment else area
#         greeting_text = f"नमस्ते येलोसेंस में आपका स्वागत है! किसी {location} से कॉल किया है और आपकी {servicetype} सेवा के लिए बुकिंग की है।\n"
#         if starttime:
#             greeting_text += f"{starttime} पर काम शुरू करने के लिए"
#         greeting_text += f" {startdate} को।\n"
#         greeting_text += "कृपया 1 दबाकर booking की confirm। reject के लिए, 2 दबाएँ।"

#         speech_key = "3757c00a36324059afa95cff5ed8731d"
#         service_region = "centralindia"
#         voice_name = "hi-IN-MadhurNeural"
#         audio_file_name = text_to_speech(greeting_text, speech_key, service_region, voice_name)

#         if audio_file_name:
#             headers = {
#                 'Content-Disposition': f'attachment; filename="{audio_file_name}"',
#                 'Content-Type': 'audio/wav'
#             }
#             response = make_response(send_file(audio_file_name, as_attachment=True))
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
#         speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
#         speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Riff8Khz16BitMonoPcm)
#         #Riff8Khz8BitMonoMULaw
#         # Generate a unique identifier for the audio file name
#         unique_id = str(uuid.uuid4())[:8]  # Using the first 8 characters of UUID
#         timestamp = time.strftime("%Y%m%d-%H%M%S")
#         audio_file_name = f"greetingaudio_{timestamp}_{unique_id}.wav"  
#         # timestamp = time.strftime("%Y%m%d-%H%M%S")
#         # audio_file_name = f"greetingaudio_{timestamp}.wav"
#         audio_config = speechsdk.audio.AudioOutputConfig(filename=audio_file_name)
#         speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
#         logging.info("Speech synthesizer initialized successfully.")
#         ssml = f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="hi-IN"><voice name="{voice_name}"><prosody rate="-5.0%">{text}</prosody></voice></speak>'
#         result = speech_synthesizer.speak_ssml_async(ssml).get()
#         if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
#             logging.info("Speech synthesis is complete.")
#             return audio_file_name
#         else:
#             logging.error("Error synthesizing speech: %s", result.reason)
#             return None
#     except Exception as e:
#         logging.error("An error occurred during text-to-speech synthesis: %s", e)
#         return None

# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO)  # Set logging level to INFO
#     app.run(debug=True)


from flask import Flask, request, jsonify, render_template
import pyaudio
import wave
import os
import threading
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

app = Flask(__name__)

# Global variable to control recording
is_recording = False
audio_frames = []
audio_stream = None
audio_instance = None

# Azure Blob Storage Configuration
connect_str = "DefaultEndpointsProtocol=https;AccountName=twittermelody;AccountKey=/+IBhdozqgO94QCBlVCv7fJ3AIm7X0cVfLxg7t50Xf980pExPYu+l+fpbonI5VEDhEqTtuSDGcZP+ASt5F4gmw==;EndpointSuffix=core.windows.net"  # Replace with your Azure Storage connection string
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_name = "melody-audiofiles"

# Function to start recording audio
def start_recording(output_file, sample_rate=44100, channels=2, chunk=1024, format=pyaudio.paInt16):
    global is_recording, audio_frames, audio_stream, audio_instance
    
    is_recording = True
    audio_frames = []

    # Initialize PyAudio
    audio_instance = pyaudio.PyAudio()

    # Define parameters for recording
    audio_stream = audio_instance.open(format=format,
                                       channels=channels,
                                       rate=sample_rate,
                                       input=True,
                                       frames_per_buffer=chunk)

    print("Recording started...")
    while is_recording:
        data = audio_stream.read(chunk)
        audio_frames.append(data)
    
    # Stop and close the stream
    audio_stream.stop_stream()
    audio_stream.close()
    audio_instance.terminate()

    # Save the recorded audio to a WAV file
    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio_instance.get_sample_size(format))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(audio_frames))

    print(f"Audio saved to {output_file}")

    # Upload to Azure Blob Storage
    upload_to_azure_blob(output_file)

# Function to upload file to Azure Blob Storage
def upload_to_azure_blob(file_path):
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=os.path.basename(file_path))

    # Check if the file already exists in the blob
    if blob_client.exists():
        print(f"File {os.path.basename(file_path)} already exists in Azure Blob Storage")
        return False

    with open(file_path, "rb") as data:
        blob_client.upload_blob(data)
    print(f"Uploaded {file_path} to Azure Blob Storage")
    return True

# API endpoint to start recording
@app.route('/start_recording_context', methods=['POST'])
def start_recording_endpoint():
    data = request.json
    if not data or 'username' not in data:
        return jsonify({"error": "Invalid JSON body"}), 400
    
    username = data['username']
    if ' ' in username:
        return jsonify({"error": "Username should not contain spaces. Please provide another name."}), 400
    output_file = f"VoiceTalentVerbalStatement_{username}.wav"

    # Check if the file already exists in the blob storage
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=os.path.basename(output_file))
    if blob_client.exists():
        return jsonify({"error": "Username already exists, please provide another name"}), 400

    # Start recording in a new thread
    threading.Thread(target=start_recording, args=(output_file,)).start()
    
    return jsonify({"message": "Recording started"}), 200

# API endpoint to stop recording
@app.route('/stop_recording_context', methods=['POST'])
def stop_recording_endpoint():
    global is_recording
    is_recording = False
    
    return jsonify({"message": "Recording stopped"}), 200


# Function to start recording audio
def start_recording_sample_voice(output_file, sample_rate=44100, channels=2, chunk=1024, format=pyaudio.paInt16):
    global is_recording, audio_frames, audio_stream, audio_instance
    
    is_recording = True
    audio_frames = []

    # Initialize PyAudio
    audio_instance = pyaudio.PyAudio()

    # Define parameters for recording
    audio_stream = audio_instance.open(format=format,
                                       channels=channels,
                                       rate=sample_rate,
                                       input=True,
                                       frames_per_buffer=chunk)

    print("Recording started...")
    while is_recording:
        data = audio_stream.read(chunk)
        audio_frames.append(data)
    
    # Stop and close the stream
    audio_stream.stop_stream()
    audio_stream.close()
    audio_instance.terminate()

    # Save the recorded audio to a WAV file
    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio_instance.get_sample_size(format))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(audio_frames))

    print(f"Audio saved to {output_file}")

    # Upload to Azure Blob Storage
    upload_to_azure_blob_samplevoice(output_file)
# Function to upload file to Azure Blob Storage
def upload_to_azure_blob_samplevoice(file_path):
    file_name = os.path.basename(file_path)
    username = file_name.split('_')[2].split('.')[0]
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=f"{username}/{file_name}")

    # Check if the file already exists in the blob
    if blob_client.exists():
        print(f"File {file_name} already exists in Azure Blob Storage")
        return False

    with open(file_path, "rb") as data:
        blob_client.upload_blob(data)
    print(f"Uploaded {file_path} to Azure Blob Storage in folder {username}")
    return True

# API endpoint to start recording
@app.route('/start_recording_samplevoice', methods=['POST'])
def start_recording_endpoint_samplevoice():
    data = request.json
    if not data or 'username' not in data:
        return jsonify({"error": "Invalid JSON body"}), 400
    
    username = data['username']
    
    if ' ' in username:
        return jsonify({"error": "Username should not contain spaces. Please provide another name."}), 400

    output_file = f"sample_voice_{username}.wav"

    # Check if the file already exists in the blob storage
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=f"{username}/{output_file}")
    if blob_client.exists():
        return jsonify({"error": "Username already exists, please provide another name"}), 400

    # Start recording in a new thread
    threading.Thread(target=start_recording_sample_voice, args=(output_file,)).start()
    
    return jsonify({"message": "Recording started"}), 200

# API endpoint to stop recording
@app.route('/stop_recording_samplevoice', methods=['POST'])
def stop_recording_samplevoice():
    global is_recording
    is_recording = False
    
    return jsonify({"message": "Recording stopped"}), 200



if __name__ == '__main__':
    app.run(debug=True)
