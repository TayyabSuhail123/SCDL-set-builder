from langgraph.graph import StateGraph, END
from app.track_downloader import download_track_audio
from app.track_analyzer import analyze_tracks
from app.track_summarizer import summarize_set

def download_node(state):
    print("Step 1: Downloading tracks...")
    state["downloaded_files"] = download_track_audio(state["url"], state["output_dir"])
    return state

def analyze_node(state):
    print("Step 2: Analyzing tracks...")
    tracks_metadata = analyze_tracks(state["output_dir"])
    print("Analyze tracks output:")
    for track in tracks_metadata:
        print(track)
    state["tracks_metadata"] = tracks_metadata
    if not tracks_metadata:
        print("No tracks analyzed successfully. Skipping summary.")
        state["summary"] = None
        return state
    return state

def summarize_node(state):
    if not state["tracks_metadata"]:
        print("No valid tracks to summarize. Skipping summary step.")
        state["summary"] = None
        return state
    print("Step 3: Summarizing DJ set...")
    state["summary"] = summarize_set(state["tracks_metadata"])
    return state

class DJSetState(dict):
    def __init__(self, url, output_dir):
        super().__init__()
        self["url"] = url
        self["output_dir"] = output_dir
        self["downloaded_files"] = []
        self["tracks_metadata"] = []
        self["summary"] = None

graph = StateGraph(dict)
graph.add_node("download", download_node)
graph.add_node("analyze", analyze_node)
graph.add_node("summarize", summarize_node)

graph.add_edge("download", "analyze")
graph.add_edge("analyze", "summarize")
graph.add_edge("summarize", END)

graph.set_entry_point("download")

def run_agent(url, output_dir):
    state = {"url": url, "output_dir": output_dir, "downloaded_files": [], "tracks_metadata": [], "summary": None}
    compiled_graph = graph.compile()
    final_state = compiled_graph.invoke(state)
    print("\nFinal summary:\n", final_state["summary"])
    return final_state["summary"]

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="DJ Set Agent: Download, analyze, and summarize tracks.")
    parser.add_argument("url", help="SoundCloud track or playlist URL")
    parser.add_argument("output_dir", help="Directory to save MP3 files")
    args = parser.parse_args()
    run_agent(args.url, args.output_dir)
