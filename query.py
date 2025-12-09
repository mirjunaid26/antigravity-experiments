import pandas as pd

class QueryEngine:
    def __init__(self, data_path):
        self.data_path = data_path
        self.df = pd.read_csv(data_path)

    def summary(self):
        """Returns a summary of tracked instances."""
        summary_df = self.df.groupby('track_id').agg(
            start_frame=('frame', 'min'),
            end_frame=('frame', 'max'),
            count=('frame', 'count'),
            class_id=('class_id', 'first') # Assuming class doesn't change
        ).reset_index()
        return summary_df

    def get_instance_appearances(self, track_id):
        """Returns a list of timestamps where the instance appears."""
        instance_data = self.df[self.df['track_id'] == track_id]
        if instance_data.empty:
            return []
        return instance_data['timestamp'].tolist()

    def get_first_appearance(self, track_id):
        """Returns the first timestamp the instance appears."""
        instance_data = self.df[self.df['track_id'] == track_id]
        if instance_data.empty:
            return None
        return instance_data['timestamp'].min()
    
    def get_time_ranges(self, track_id, gap_threshold=1.0):
        """
        Returns a list of (start, end) tuples for when the object is visible.
        gap_threshold: max seconds between frames to consider it the same "appearance" segment.
        """
        timestamps = self.get_instance_appearances(track_id)
        if not timestamps:
            return []
        
        timestamps.sort()
        ranges = []
        start = timestamps[0]
        prev = timestamps[0]
        
        for t in timestamps[1:]:
            if t - prev > gap_threshold:
                ranges.append((start, prev))
                start = t
            prev = t
        ranges.append((start, prev))
        
        return ranges

if __name__ == "__main__":
    # Test
    qe = QueryEngine('tracking_results.csv')
    print(qe.summary())
