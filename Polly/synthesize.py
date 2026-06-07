import boto3
import os

bucket_name = os.environ["POLLY_S3_BUCKET_NAME"]
output_key = os.environ["OUTPUT_KEY"]

polly = boto3.client("polly")
s3 = boto3.client("s3")

with open("speech.txt", "r", encoding="utf-8") as file:
    text = file.read()

response = polly.synthesize_speech(
    Text=text,
    OutputFormat="mp3",
    VoiceId="Joanna",
    Engine="neural"
)

audio_file = "output.mp3"

with open(audio_file, "wb") as file:
    file.write(response["AudioStream"].read())

s3.upload_file(audio_file, bucket_name, output_key)

print(f"Uploaded {audio_file} to s3://{bucket_name}/{output_key}")