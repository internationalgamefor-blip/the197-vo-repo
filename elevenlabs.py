#!/usr/bin/env python3
"""ElevenLabs helper using Muse's surrogate credential exchange.
Usage:
  elevenlabs.py user
  elevenlabs.py voices
  elevenlabs.py tts --voice-id ID --text "text" --out file.mp3 [--model eleven_multilingual_v2] [--stability 0.5] [--similarity 0.75] [--style 0.0]
No secret is stored in this file or in arguments; the surrogate is swapped
in only on an approved request to api.elevenlabs.io.
"""
import argparse, json, sys, urllib.request
sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response

BASE = "https://api.elevenlabs.io"
PROVIDER = "custom.elevenlabs"

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        raise RuntimeError("redirect refused, verify the endpoint")

def call(method, path, body=None, raw=False):
    req = urllib.request.Request(BASE + path, method=method)
    if body is not None:
        data = json.dumps(body).encode()
        req.data = data
        req.add_header("Content-Type", "application/json")
    add_surrogate_to_request(req, PROVIDER, allowed_hosts=["api.elevenlabs.io"])
    with urllib.request.build_opener(NoRedirect()).open(req, timeout=60) as resp:
        if raw:
            return resp.read()
        return read_json_response(resp)

def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("user")
    sub.add_parser("voices")
    t = sub.add_parser("tts")
    t.add_argument("--voice-id", required=True)
    t.add_argument("--text", required=True)
    t.add_argument("--out", required=True)
    t.add_argument("--model", default="eleven_multilingual_v2")
    t.add_argument("--stability", type=float, default=0.5)
    t.add_argument("--similarity", type=float, default=0.75)
    t.add_argument("--style", type=float, default=0.0)
    args = p.parse_args()
    if args.cmd == "user":
        print(json.dumps(call("GET", "/v1/user"), indent=2))
    elif args.cmd == "voices":
        print(json.dumps(call("GET", "/v1/voices"), indent=2))
    elif args.cmd == "tts":
        audio = call("POST", f"/v1/text-to-speech/{args.voice_id}",
                     {"text": args.text, "model_id": args.model,
                      "voice_settings": {"stability": args.stability,
                                         "similarity_boost": args.similarity,
                                         "style": args.style,
                                         "use_speaker_boost": True}}, raw=True)
        with open(args.out, "wb") as f:
            f.write(audio)
        print(f"wrote {args.out} ({len(audio)} bytes)")
if __name__ == "__main__":
    main()
