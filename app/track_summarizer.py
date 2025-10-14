from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

# You will need to set your OpenAI API key in the environment
# os.environ['OPENAI_API_KEY'] = 'sk-...'

# Placeholder for LLM summary and recommendations
# You will use LangChain or similar to call an LLM and summarize the DJ set

def is_harmonically_compatible(key1, key2):
    """
    Check if two keys are harmonically compatible.
    This function assumes the use of the Camelot wheel for key compatibility.
    """
    # Simple compatibility: same key or both start with the same letter
    if key1 == key2:
        return True
    if key1 and key2 and key1[0] == key2[0]:
        return True
    return False

def filter_compatible_tracks(tracks, bpm_tolerance=3):
    compatible_pairs = []
    for i in range(len(tracks) - 1):
        t1 = tracks[i]
        t2 = tracks[i + 1]
        bpm_diff = abs(t1['bpm'] - t2['bpm'])
        # Harmonic compatibility: same key or adjacent in Camelot wheel
        key_compatible = t1['key'] == t2['key'] or is_harmonically_compatible(t1['key'], t2['key'])
        if bpm_diff <= bpm_tolerance and key_compatible:
            compatible_pairs.append((t1, t2))
    return compatible_pairs

def summarize_set(tracks):
    """
    Given a list of track dicts with title, bpm, key, and energy,
    use an LLM to summarize and recommend a DJ set order.
    """
    track_list = "\n".join([
        f"{t['title']} (BPM: {t['bpm']}, Key: {t['key']})" for t in tracks
    ])
    prompt_text = (
        "You are an expert DJ set builder. Given the following tracks with their BPM and key, "
        "summarize how to build a DJ set that flows well. For each transition, explain the mixing reason using BPM and key compatibility. "
        "Avoid transitions with big BPM jumps (greater than 4 BPM). Suggest an order and transitions based on key compatibility, energy progression, and BPM matching.\n\nTracks:\n" + track_list
    )
    llm = OpenAI(temperature=0.7)
    response = llm.invoke(prompt_text, max_tokens=1024)
    return response
