import logging

import outspeed as sp
from outspeed.server import RealtimeServer
from fastapi import FastAPI, File, UploadFile

app = RealtimeServer().get_app()

def check_outspeed_version():
    import importlib.metadata

    from packaging import version

    required_version = "0.1.147"

    try:
        current_version = importlib.metadata.version("outspeed")
        if version.parse(current_version) < version.parse(required_version):
            raise ValueError(f"Outspeed version {current_version} is not greater than {required_version}.")
        else:
            print(f"Outspeed version {current_version} meets the requirement.")
    except importlib.metadata.PackageNotFoundError:
        raise ValueError("Outspeed package is not installed.")


check_outspeed_version()
# Set up basic logging configuration
logging.basicConfig(level=logging.INFO)

"""
The @outspeed.App() decorator is used to wrap the VoiceBot class.
This tells the outspeed server which functions to run.
"""


@sp.App()
class VoiceBot:
    async def setup(self) -> None:
        self.llm_node = sp.OpenAIRealtime(system_prompt="""
        Only say the phrase "The sun is yellow" regardless of what is said to you.
                                          """)

    @sp.streaming_endpoint()
    async def run(self, audio_input_queue: sp.AudioStream, text_input_queue: sp.TextStream) -> sp.AudioStream:
        audio_output_stream: sp.AudioStream
        audio_output_stream = self.llm_node.run(text_input_queue, audio_input_queue)

        return audio_output_stream

    async def teardown(self) -> None:
        await self.llm_node.close()

@app.get("/ping")
def ping():
    return {"message": "pong"}

@app.post("/upload")
def upload(pdf_file: UploadFile):
    """ function to upload a PDF file to storage """
    """ https://fastapi.tiangolo.com/tutorial/request-files/#multiple-file-uploads to have a form upload"""

    return {"filename": pdf_file.filename}

if __name__ == "__main__":
    VoiceBot().start()