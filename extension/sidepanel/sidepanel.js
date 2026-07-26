const status = document.getElementById("status");
const videoTitle = document.getElementById("videoTitle");
const videoId = document.getElementById("videoId");
const url = document.getElementById("url");
let currentVideo = null;

const processBtn = document.getElementById("processBtn");

processBtn.addEventListener("click", async () => {
    status.textContent = "Processing...";
    processBtn.disabled = true;
    try {
        const response = await fetch(
            "http://localhost:8000/index",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    video_url: currentVideo.url
                })
            }
        );
        const data = await response.json();
        status.textContent = "Ready";
        console.log(data);
    }
    catch (err) {
        status.textContent = "Failed";
        console.error(err);
    }
    finally {
        processBtn.disabled = false;
    }
});

function updateUI(video) {
    currentVideo = video;
    if (!video) {
        status.textContent = "No YouTube Video";
        videoTitle.textContent = "";
        videoId.textContent = "";
        url.textContent = "";
        return;
    }
    status.textContent = "✅ Video Detected";
    videoTitle.textContent = video.title;
    videoId.textContent = video.videoId;
    url.textContent = video.url;
}

document.addEventListener("DOMContentLoaded", () => {
    chrome.runtime.sendMessage(
        {
            type: "GET_CURRENT_VIDEO"
        },
        (video) => {
            updateUI(video);
        }
    );
});

chrome.runtime.onMessage.addListener((message) => {
    if (message.type !== "VIDEO_UPDATED")
        return;
    updateUI(message.payload);
});