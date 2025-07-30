from moviepy.editor import VideoFileClip, concatenate_videoclips
from typing import List

def combine_videos(video_paths: List[str], output_path: str) -> str:
    """
    Combine multiple videos in sequence and save to a new file.
    Each clip will be cut to 3 seconds.
    
    Args:
        video_paths: List of paths to video files to combine in order
        output_path: Path where the combined video should be saved
        
    Returns:
        str: Path to the combined video file
    """
    # Load all video clips and cut to 3 seconds
    clips = []
    for path in video_paths:
        clip = VideoFileClip(path)
        if clip.duration > 3:
            clip = clip.subclip(0, 3)
        clips.append(clip)
    
    # Concatenate all clips
    final_clip = concatenate_videoclips(clips, method="compose")
    
    # Write the result to a file
    final_clip.write_videofile(output_path)
    
    # Close all clips to free up resources
    for clip in clips:
        clip.close()
    final_clip.close()
    
    return output_path

if __name__ == "__main__":
    # Example usage:
    videos = ["photo_0.mp4", "photo_1.mp4", "photo_3.mp4", "photo_4.mp4"]
    result = combine_videos(videos, "combined_output.mp4")
    print(f"Combined video saved to: {result}")