const status = document.getElementById("status");
const videoTitle = document.getElementById("videoTitle");

const processBtn = document.getElementById("processBtn");
const askBtn = document.getElementById("askBtn");

const questionBox = document.getElementById("question");
const chatContainer = document.getElementById("chatContainer");

let chatHistory = [];
let currentVideo = null;
let isIndexed = false;

askBtn.disabled = true;

function renderChat(){
    chatContainer.innerHTML = "";
    chatHistory.forEach(message=>{
        const div=document.createElement("div");
        div.className=`message ${message.role}`;
        div.innerHTML=`
            <strong>${message.role==="user" ? "👤 You":"🤖 TLDW AI"}</strong>
            ${
                message.role==="assistant"
                ? marked.parse(message.content)
                : message.content
            }
        `;
        chatContainer.appendChild(div);
    });
    chatContainer.scrollTop=chatContainer.scrollHeight;
}

processBtn.addEventListener("click", async () => {
    if (!currentVideo) return;

    status.textContent = "⏳ Processing video...";
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
                    youtube_url: currentVideo.url
                })
            }
        );

        if (!response.ok) {
            throw new Error("Indexing failed");
        }

        const data = await response.json();

        status.textContent = data.from_cache ? "⚡ Already Indexed" : "🟢 Ready";

        isIndexed = true;
        askBtn.disabled = false;
        processBtn.textContent = "Processed ✓";
        processBtn.disabled = true;

        console.log(data);
    }
    catch (err) {
        status.textContent = "🔴 Failed";
        isIndexed = false;
        askBtn.disabled = true;
        console.error(err);
    }
    finally {
        // processBtn.disabled = false;
    }
});

askBtn.addEventListener("click", async () => {
    if (!isIndexed) return;

    const question = questionBox.value.trim();

    if (!question) {
        chatContainer.textContent = "Please enter a question.";
        return;
    }

    chatHistory.push({
        role:"user",
        content:question
    });

    chatHistory.push({
        role:"assistant",
        content:"<div class='loading'>Generating answer...</div>"
    });

    renderChat();
    askBtn.disabled = true;

    try {
        const response = await fetch(
            "http://localhost:8000/ask",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    youtube_url: currentVideo.url,
                    question
                })
            }
        );

        if (!response.ok) {
            throw new Error("Failed to get answer");
        }

        const data = await response.json();
        
        chatHistory.pop();

        chatHistory.push({
            role:"assistant",
            content:data.answer
        });

        renderChat();
    }
    catch (err) {
        console.error(err);
        chatHistory.pop();

        chatHistory.push({
            role:"assistant",
            content:"❌ Something went wrong."
        });

        renderChat();
    }
    finally {
        askBtn.disabled = false;
    }
});

function updateUI(video) {
    currentVideo = video;
    isIndexed = false;
    askBtn.disabled = true;
    questionBox.value = "";
    chatHistory=[];

    renderChat();

    if (!video) {
        status.textContent = "🔴 No Video";
        videoTitle.textContent = "No Video Detected";
        processBtn.disabled = true;
        return;
    }

    processBtn.disabled = false;
    status.textContent = "📺 Video Detected";
    videoTitle.textContent = video.title;
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