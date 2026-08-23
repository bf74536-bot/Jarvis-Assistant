Jarvis — Your Own Voice Assistant
A simple, working voice assistant you run on your own laptop. Talk to it, it listens, thinks (using Claude), and talks back.
What you need
Python 3.9 or newer (python.org)
A microphone (built-in laptop mic is fine)
A free Anthropic API key (console.anthropic.com)
Setup (one-time)
Install the required packages. Open a terminal in this folder and run:
pip install SpeechRecognition pyttsx3 anthropic pyaudio
If pyaudio fails to install:
Mac: run brew install portaudio first, then retry the pip command
Windows: run pip install pipwin then pipwin install pyaudio
Linux: run sudo apt-get install python3-pyaudio (Debian/Ubuntu) then retry
Add your API key. The easiest way is to set it as an environment variable:
Mac/Linux: export ANTHROPIC_API_KEY=your-key-here
Windows (PowerShell): $env:ANTHROPIC_API_KEY="your-key-here"
(Or just paste it directly into the API_KEY line near the top of jarvis.py — fine for testing, just don't share the file with your key still in it.)
Run it:
python jarvis.py
Wait for it to say "Jarvis online. How can I help?", then just talk. Say "goodbye" anytime to exit.
How it works
Your mic picks up audio
SpeechRecognition converts it to text (via Google's free speech API)
The text gets sent to Claude, which generates a short spoken-style reply
pyttsx3 speaks the reply out loud, completely offline
Loops back to listening
Troubleshooting
"Could not understand audio" — happens if you're too quiet/far from the mic or there's background noise. Just try again.
No sound coming out — check your system's output volume/device; pyttsx3 uses your OS's default voice engine.
It doesn't understand accents/technical words well — that's a limitation of free Google speech recognition. Swapping in OpenAI's Whisper (pip install openai-whisper) gives much better accuracy — happy to help you upgrade to that next.
Ideas for leveling this up (whenever you're ready)
Wake word ("Hey Jarvis") instead of always-listening — using pvporcupine (free, offline)
Better voice — swap pyttsx3 for ElevenLabs for a much more natural-sounding voice
Better hearing — swap Google speech recognition for local Whisper (works offline, more accurate)
Actions — let Jarvis actually open apps, check your calendar, control smart home devices, etc. using Claude's tool-use feature
