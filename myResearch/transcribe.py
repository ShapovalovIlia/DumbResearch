import requests, time
import pandas as pd

# Replace with your AssemblyAI API key
API_KEY = "47a356522b784ade852e7965e9756087"


def upload_file(file_path):
    def read_file(filename, chunk_size=5242880):
        with open(filename, "rb") as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    headers = {"authorization": API_KEY}
    response = requests.post(
        "https://api.assemblyai.com/v2/upload",
        headers=headers,
        data=read_file(file_path),
    )

    if response.status_code == 200:
        print(f"Upload URL : {response.json()['upload_url']}\n")
        return response.json()["upload_url"]
    else:
        print(f"Error uploading file: {response.text}")
        return None


def submit_transcription_job(audio_url):
    endpoint = "https://api.assemblyai.com/v2/transcript"
    json = {
        "audio_url": audio_url,
        "punctuate": True,  # Add punctuation
        "format_text": True,  # Add formatting (e.g., capitalization)
        "speaker_labels": True,  # Try to label different speakers
    }
    headers = {"authorization": API_KEY, "content-type": "application/json"}
    response = requests.post(endpoint, json=json, headers=headers)
    if response.status_code == 200:
        print(f"Transcription ID: {response.json()['id']}")
        return response.json()["id"]
    else:
        print(f"Error submitting transcription job: {response.text}")
        return None


def get_transcription_result(transcription_id):
    endpoint = f"https://api.assemblyai.com/v2/transcript/{transcription_id}"
    headers = {
        "authorization": API_KEY,
    }
    while True:
        response = requests.get(endpoint, headers=headers)
        response_json = response.json()

        # print(response_json)
        # print(f'Transcription ID: {transcription_id}')

        if response_json["status"] == "completed":
            endpoint = endpoint + "/sentences"
            response = requests.get(endpoint, headers=headers)
            response_json = response.json()
            return response_json
        elif response_json["status"] == "failed":
            print(f"Transcription failed: {response_json['error']}")
            return None
        else:
            print("Transcription processing...")
            time.sleep(5)  # Wait for 5 seconds before polling again


def save_transcription_to_csv(sentences, output_file):
    if sentences:
        # Create a list of dictionaries to store the data
        data = []
        for sentence in sentences["sentences"]:
            start_time = sentence["start"]
            text = sentence["text"]
            data.append(
                {
                    "Time": start_time
                    / 1000,  # Convert milliseconds to seconds and rename column to 'Time'
                    "text": text,
                }
            )

        # Create a pandas DataFrame from the list of dictionaries
        df = pd.DataFrame(data)

        # Save the DataFrame to a CSV file
        df.to_csv(output_file, index=False)

        print(f"Transcription saved to {output_file}")
    else:
        print("Error: No sentences found in the transcription result.")


# Main execution
if __name__ == "__main__":
    # 1. Get the current working directory and construct file paths
    # Ensure the output directory exists
    # 2. Upload the audio file
    audio_url = upload_file("data/audios/test.mp3")
    # audio_url = 1

    if audio_url:
        # 3. Submit the transcription job
        transcription_id = submit_transcription_job(audio_url)
        # transcription_id = ''

        if transcription_id:
            # 4. Get the transcription result
            sentences = get_transcription_result(
                transcription_id
            )  # Note: Now gets sentences

            # 5. Save the transcription to a CSV file
            save_transcription_to_csv(sentences, "data/processedData/test.csv")
        else:
            print("Error: Could not submit transcription job")
    else:
        print("Error: Could not upload file")
