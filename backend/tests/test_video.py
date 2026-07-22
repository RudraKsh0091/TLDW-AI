from app.utils.youtube import extract_video_id

url = "https://www.youtube.com/watch?v=J5_-l7WIO_w"

video_id = extract_video_id(url)

print(video_id)