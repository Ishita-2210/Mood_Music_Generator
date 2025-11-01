const moodInput = document.getElementById("moodInput");
const playButton = document.getElementById("playButton");
const emotionLabel = document.getElementById("emotionLabel");
const player = document.getElementById("player");

// Pastel colors for moods
const pastelColors = {
    happy: "#FFFACD",
    sad: "#ADD8E6",
    relaxed: "#B0E0E6",
    angry: "#FFB6C1",
    neutral: "#E0E0E0"
};

// Simple keyword-based emotion detection
const keywordEmotions = {
    motivated: "happy",
    excited: "happy",
    joyful: "happy",
    sad: "sad",
    angry: "angry",
    relaxed: "relaxed",
    calm: "relaxed",
    neutral: "neutral"
};

// Song mapping
const emotionTracks = {
    happy: ["https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"],
    sad: ["https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3"],
    relaxed: ["https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3"],
    angry: ["https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3"],
    neutral: ["https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3"]
};

// Detect emotion
function detectEmotion(text) {
    text = text.toLowerCase();
    for (let word in keywordEmotions) {
        if (text.includes(word)) return keywordEmotions[word];
    }
    return "neutral"; // fallback
}

// Play mood song
playButton.addEventListener("click", () => {
    const text = moodInput.value.trim();
    if (!text) {
        emotionLabel.textContent = "Please enter your mood!";
        return;
    }

    const emotion = detectEmotion(text);
    const songList = emotionTracks[emotion];
    const song = songList[Math.floor(Math.random() * songList.length)];

    emotionLabel.textContent = `Detected mood: ${emotion}. Playing a matching song...`;
    document.body.style.backgroundColor = pastelColors[emotion] || "#FFFFFF";

    player.src = song;
    player.play();
});
