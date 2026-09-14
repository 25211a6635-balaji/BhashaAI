const textInput =
    document.getElementById("textInput");

const detectButton =
    document.getElementById("detectButton");

const voiceButton =
    document.getElementById("voiceButton");

const loading =
    document.getElementById("loading");

const voiceStatus =
    document.getElementById("voiceStatus");

const result =
    document.getElementById("result");

const inputText =
    document.getElementById("inputText");

const dialect =
    document.getElementById("dialect");

const standardHindi =
    document.getElementById("standardHindi");

const confidence =
    document.getElementById("confidence");

const confidenceDisplay =
    document.getElementById("confidenceDisplay");

const confidenceBar =
    document.getElementById("confidenceBar");


/* ==========================================
   DIALECT PROBABILITY ELEMENTS
========================================== */

const probabilityElements = {

    HIN: {
        text: document.getElementById(
            "hindiProbability"
        ),
        bar: document.getElementById(
            "hindiBar"
        )
    },

    BRA: {
        text: document.getElementById(
            "brajProbability"
        ),
        bar: document.getElementById(
            "brajBar"
        )
    },

    AWA: {
        text: document.getElementById(
            "awadhiProbability"
        ),
        bar: document.getElementById(
            "awadhiBar"
        )
    },

    BHO: {
        text: document.getElementById(
            "bhojpuriProbability"
        ),
        bar: document.getElementById(
            "bhojpuriBar"
        )
    },

    MAG: {
        text: document.getElementById(
            "magahiProbability"
        ),
        bar: document.getElementById(
            "magahiBar"
        )
    }

};


/* ==========================================
   VOICE RECOGNITION
========================================== */

let recognition = null;

let isListening = false;


if (
    "webkitSpeechRecognition" in window ||
    "SpeechRecognition" in window
) {

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;


    recognition =
        new SpeechRecognition();


    recognition.lang =
        "hi-IN";


    recognition.continuous =
        false;


    recognition.interimResults =
        true;


    /* --------------------------------------
       VOICE START
    -------------------------------------- */

    recognition.onstart =
        function () {

            isListening = true;


            voiceButton.classList.add(
                "listening"
            );


            voiceButton.innerText =
                "🔴 Listening...";


            voiceStatus.style.display =
                "block";


            voiceStatus.innerText =
                "🎤 Listening... Please speak in Hindi.";

        };


    /* --------------------------------------
       VOICE RESULT
    -------------------------------------- */

    recognition.onresult =
        function (event) {

            let transcript = "";


            for (
                let i = event.resultIndex;
                i < event.results.length;
                i++
            ) {

                transcript +=
                    event.results[i][0].transcript;

            }


            textInput.value =
                transcript;


            voiceStatus.innerText =
                "✅ Voice captured successfully.";

        };


    /* --------------------------------------
       VOICE END
    -------------------------------------- */

    recognition.onend =
        function () {

            isListening = false;


            voiceButton.classList.remove(
                "listening"
            );


            voiceButton.innerText =
                "🎤 Voice Input";

        };


    /* --------------------------------------
       VOICE ERROR
    -------------------------------------- */

    recognition.onerror =
        function (event) {

            console.error(
                "Speech recognition error:",
                event.error
            );


            isListening = false;


            voiceButton.classList.remove(
                "listening"
            );


            voiceButton.innerText =
                "🎤 Voice Input";


            if (
                event.error ===
                "not-allowed"
            ) {

                voiceStatus.style.display =
                    "block";


                voiceStatus.innerText =
                    "❌ Microphone permission was denied.";

            }

            else if (
                event.error ===
                "no-speech"
            ) {

                voiceStatus.style.display =
                    "block";


                voiceStatus.innerText =
                    "⚠️ No speech detected. Please try again.";

            }

            else {

                voiceStatus.style.display =
                    "block";


                voiceStatus.innerText =
                    "❌ Voice recognition error. Please try again.";

            }

        };

}


/* ==========================================
   START VOICE INPUT
========================================== */

function startVoiceTyping() {

    if (!recognition) {

        alert(
            "Voice input is not supported in this browser.\n\n" +
            "Please use Google Chrome or Microsoft Edge."
        );

        return;

    }


    /* Stop if already listening */

    if (isListening) {

        recognition.stop();

        return;

    }


    voiceStatus.style.display =
        "block";


    voiceStatus.innerText =
        "🎤 Starting microphone...";


    try {

        recognition.start();

    }

    catch (error) {

        console.error(error);

    }

}


/* ==========================================
   DETECT DIALECT
========================================== */

async function detectDialect() {

    const text =
        textInput.value.trim();


    if (!text) {

        alert(
            "Please enter a sentence or use Voice Input first."
        );

        return;

    }


    /* Show loading */

    loading.style.display =
        "block";


    result.style.display =
        "none";


    detectButton.disabled =
        true;


    voiceButton.disabled =
        true;


    detectButton.innerText =
        "Analyzing...";


    try {

        const response =
            await fetch(
                "http://127.0.0.1:8000/predict",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        text: text
                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Something went wrong."
            );

        }


        if (data.error) {

            throw new Error(
                data.error
            );

        }


        /* ----------------------------------
           UPDATE INPUT
        ---------------------------------- */

        inputText.textContent =
            data.input;


        /* ----------------------------------
           UPDATE DIALECT
        ---------------------------------- */

        dialect.textContent =
            data.dialect;


        /* ----------------------------------
           UPDATE STANDARD HINDI
        ---------------------------------- */

        standardHindi.textContent =
            data.standard_hindi;


        /* ----------------------------------
           UPDATE CONFIDENCE
        ---------------------------------- */

        confidence.textContent =
            data.confidence + "%";


        confidenceDisplay.textContent =
            data.confidence + "%";


        confidenceBar.style.width =
            data.confidence + "%";


        /* ----------------------------------
           UPDATE PROBABILITIES
        ---------------------------------- */

        for (
            const code in probabilityElements
        ) {

            const percentage =
                data.probabilities[code] || 0;


            probabilityElements[code]
                .text
                .textContent =
                percentage + "%";


            probabilityElements[code]
                .bar
                .style.width =
                percentage + "%";

        }


        /* Save latest translation */

        window.latestStandardHindi =
            data.standard_hindi;


        /* Show result */

        result.style.display =
            "block";


        voiceStatus.style.display =
            "none";

    }


    catch (error) {

        console.error(
            "BhashaAI Error:",
            error
        );


        alert(
            "Unable to connect to BhashaAI backend.\n\n" +
            "Make sure FastAPI is running."
        );

    }


    finally {

        loading.style.display =
            "none";


        detectButton.disabled =
            false;


        voiceButton.disabled =
            false;


        detectButton.innerText =
            "🔍 Detect & Translate";

    }

}


/* ==========================================
   AI VOICE — AUTO HINDI VOICE
========================================== */

function speakResult() {

    const text =
        window.latestStandardHindi ||
        standardHindi.textContent;


    if (
        !text ||
        text === "-"
    ) {

        alert(
            "Please detect and translate a sentence first."
        );

        return;

    }


    /* Stop any previous speech */

    window.speechSynthesis.cancel();


    const utterance =
        new SpeechSynthesisUtterance(
            text
        );


    /* Hindi language */

    utterance.lang =
        "hi-IN";


    /* Natural speaking speed */

    utterance.rate =
        0.9;


    utterance.pitch =
        1;


    /* ----------------------------------
       FIND HINDI VOICE
    ---------------------------------- */

    const voices =
        window.speechSynthesis.getVoices();


    const hindiVoices =
        voices.filter(
            voice =>
                voice.lang
                    .toLowerCase()
                    .startsWith("hi")
        );


    if (
        hindiVoices.length > 0
    ) {

        utterance.voice =
            hindiVoices[0];

    }


    /* ----------------------------------
       SPEECH START
    ---------------------------------- */

    utterance.onstart =
        function () {

            voiceStatus.style.display =
                "block";


            voiceStatus.innerText =
                "🔊 BhashaAI is speaking Standard Hindi...";

        };


    /* ----------------------------------
       SPEECH END
    ---------------------------------- */

    utterance.onend =
        function () {

            voiceStatus.style.display =
                "block";


            voiceStatus.innerText =
                "✅ Finished speaking.";

        };


    /* ----------------------------------
       SPEECH ERROR
    ---------------------------------- */

    utterance.onerror =
        function (event) {

            console.error(
                "Speech synthesis error:",
                event
            );


            voiceStatus.style.display =
                "block";


            voiceStatus.innerText =
                "❌ Unable to play the voice.";

        };


    /* Start speaking */

    window.speechSynthesis.speak(
        utterance
    );

}


/* ==========================================
   STOP VOICE
========================================== */

function stopSpeaking() {

    window.speechSynthesis.cancel();


    voiceStatus.style.display =
        "block";


    voiceStatus.innerText =
        "⏹ Voice stopped.";

}


/* ==========================================
   LOAD AVAILABLE VOICES
========================================== */

function loadVoices() {

    const voices =
        window.speechSynthesis.getVoices();


    console.log(
        "Available browser voices:"
    );


    voices.forEach(
        voice => {

            console.log(
                voice.name,
                "-",
                voice.lang
            );

        }
    );

}


window.speechSynthesis.onvoiceschanged =
    loadVoices;


loadVoices();