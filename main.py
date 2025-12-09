import argparse
import sys
import os
from tracker import VideoTracker
from query import QueryEngine

def track(args):
    if not os.path.exists(args.video):
        print(f"Error: Video file '{args.video}' not found.")
        sys.exit(1)
    
    print(f"Starting tracking on {args.video}...")
    tracker = VideoTracker()
    tracker.process_video(args.video, args.output)
    print("Tracking finished.")

def query(args):
    if not os.path.exists(args.data):
        print(f"Error: Data file '{args.data}' not found. Run 'track' first.")
        sys.exit(1)

    engine = QueryEngine(args.data)
    
    if args.summary:
        print(engine.summary())
        return

    if args.id is not None:
        if args.first_appearance:
            timestamp = engine.get_first_appearance(args.id)
            if timestamp is not None:
                print(f"Instance {args.id} first appears at: {timestamp:.2f}s")
            else:
                print(f"Instance {args.id} not found.")
        elif args.list_all:
            timestamps = engine.get_instance_appearances(args.id)
            if timestamps:
                print(f"Instance {args.id} appears at: {timestamps}")
            else:
                print(f"Instance {args.id} not found.")
        elif args.ranges:
             ranges = engine.get_time_ranges(args.id)
             if ranges:
                 print(f"Instance {args.id} looks visible during: {ranges}")
             else:
                 print(f"Instance {args.id} not found.")
        else:
             # Default behavior asking for a specific query type
             print("Please specify query type: --first-appearance, --list-all, or --ranges")


def main():
    parser = argparse.ArgumentParser(description="Video Object Tracking and Query System")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Track command
    track_parser = subparsers.add_parser("track", help="Run object tracking on a video")
    track_parser.add_argument("--video", required=True, help="Path to input video file")
    track_parser.add_argument("--output", default="results.csv", help="Path to output CSV file")
    track_parser.set_defaults(func=track)

    # Query command
    query_parser = subparsers.add_parser("query", help="Query tracking results")
    query_parser.add_argument("--data", default="results.csv", help="Path to tracking CSV data")
    query_parser.add_argument("--id", type=int, help="Instance ID to query")
    query_parser.add_argument("--summary", action="store_true", help="Show summary of all instances")
    query_parser.add_argument("--first-appearance", action="store_true", help="Get first appearance timestamp")
    query_parser.add_argument("--list-all", action="store_true", help="List all appearance timestamps")
    query_parser.add_argument("--ranges", action="store_true", help="Show time ranges of visibility")
    query_parser.set_defaults(func=query)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
