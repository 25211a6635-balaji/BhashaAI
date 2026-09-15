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


            voiceStatus.style.display =
                "block";


            if (
                event.error === "not-allowed"
            ) {

                voiceStatus.innerText =
                    "⚠️ Microphone permission was denied.";

            }

            else if (
                event.error === "no-speech"
            ) {

                voiceStatus.innerText =
                    "⚠️ No speech detected. Please try again.";

            }

            else {

                voiceStatus.innerText =
                    "⚠️ Voice recognition error. Please try again.";

            }

        };

}


/* ==========================================
   VOICE BUTTON
========================================== */

if (voiceButton) {

    voiceButton.addEventListener(
        "click",
        function () {

            if (!recognition) {

                alert(
                    "Voice recognition is not supported in this browser."
                );

                return;

            }


            if (isListening) {

                recognition.stop();

            }

            else {

                recognition.start();

            }

        }
    );

}


/* ==========================================
   DETECT & TRANSLATE
========================================== */

if (detectButton) {

    detectButton.addEventListener(
        "click",
        async function () {

            const sentence =
                textInput.value.trim();


            /* --------------------------------
               EMPTY INPUT
            -------------------------------- */

            if (!sentence) {

                alert(
                    "Please enter a Hindi sentence first."
                );

                return;

            }


            /* --------------------------------
               SHOW LOADING
            -------------------------------- */

            if (loading) {

                loading.style.display =
                    "block";

            }


            if (result) {

                result.style.display =
                    "none";

            }


            detectButton.disabled =
                true;


            try {

                console.log(
                    "Sending sentence to BhashaAI:",
                    sentence
                );


                /* ----------------------------
                   SEND TO FASTAPI
                ---------------------------- */

                const response =
                    await fetch(
                        "/predict",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify({
                                    text: sentence
                                })
                        }
                    );


                console.log(
                    "Backend response status:",
                    response.status
                );


                /* ----------------------------
                   CHECK RESPONSE
                ---------------------------- */

                if (!response.ok) {

                    throw new Error(
                        "Backend returned HTTP " +
                        response.status
                    );

                }


                const data =
                    await response.json();


                console.log(
                    "BhashaAI result:",
                    data
                );


                /* ----------------------------
                   CHECK API ERROR
                ---------------------------- */

                if (data.error) {

                    throw new Error(
                        data.error
                    );

                }


                /* ----------------------------
                   DISPLAY INPUT
                ---------------------------- */

                if (inputText) {

                    inputText.textContent =
                        data.input || sentence;

                }


                /* ----------------------------
                   DISPLAY DIALECT
                ---------------------------- */

                if (dialect) {

                    dialect.textContent =
                        data.dialect || "-";

                }


                /* ----------------------------
                   DISPLAY STANDARD HINDI
                ---------------------------- */

                if (standardHindi) {

                    standardHindi.textContent =
                        data.standard_hindi ||
                        data.input ||
                        sentence;

                }


                /* ----------------------------
                   DISPLAY CONFIDENCE
                ---------------------------- */

                const confidenceValue =
                    Number(
                        data.confidence || 0
                    );


                if (confidence) {

                    confidence.textContent =
                        confidenceValue.toFixed(2) +
                        "%";

                }


                if (confidenceDisplay) {

                    confidenceDisplay.textContent =
                        confidenceValue.toFixed(2) +
                        "%";

                }


                if (confidenceBar) {

                    confidenceBar.style.width =
                        confidenceValue + "%";

                }


                /* ----------------------------
                   DISPLAY PROBABILITIES
                ---------------------------- */

                if (data.probabilities) {

                    Object.keys(
                        probabilityElements
                    ).forEach(
                        function (code) {

                            const elements =
                                probabilityElements[
                                    code
                                ];


                            if (!elements) {

                                return;

                            }


                            const value =
                                Number(
                                    data.probabilities[
                                        code
                                    ] || 0
                                );


                            if (elements.text) {

                                elements.text.textContent =
                                    value.toFixed(2) +
                                    "%";

                            }


                            if (elements.bar) {

                                elements.bar.style.width =
                                    value + "%";

                            }

                        }
                    );

                }


                /* ----------------------------
                   SHOW RESULT
                ---------------------------- */

                if (result) {

                    result.style.display =
                        "block";

                }


                /* ----------------------------
                   SAVE FOR VOICE OUTPUT
                ---------------------------- */

                window.latestStandardHindi =
                    data.standard_hindi ||
                    data.input ||
                    sentence;


            }

            catch (error) {

                console.error(
                    "BhashaAI error:",
                    error
                );


                alert(
                    "Unable to connect to BhashaAI backend.\n\n" +
                    error.message
                );

            }

            finally {

                if (loading) {

                    loading.style.display =
                        "none";

                }


                detectButton.disabled =
                    false;

            }

        }
    );

}


/* ==========================================
   AI VOICE — AUTO HINDI VOICE
========================================== */

function speakResult() {

    const text =
        window.latestStandardHindi ||
        (
            standardHindi
                ? standardHindi.textContent
                : ""
        );


    if (
        !text ||
        text === "-"
    ) {

        alert(
            "Please detect and translate a sentence first."
        );

        return;

    }


    /* Stop previous speech */

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


    /* --------------------------------------
       FIND HINDI VOICE
    -------------------------------------- */

    const voices =
        window.speechSynthesis.getVoices();


    const hindiVoices =
        voices.filter(
            function (voice) {

                return voice.lang
                    .toLowerCase()
                    .startsWith("hi");

            }
        );


    if (
        hindiVoices.length > 0
    ) {

        utterance.voice =
            hindiVoices[0];

    }


    /* --------------------------------------
       SPEECH START
    -------------------------------------- */

    utterance.onstart =
        function () {

            if (voiceStatus) {

                voiceStatus.style.display =
                    "block";


                voiceStatus.innerText =
                    "🔊 BhashaAI is speaking Standard Hindi...";

            }

        };


    /* --------------------------------------
       SPEECH END
    -------------------------------------- */

    utterance.onend =
        function () {

            if (voiceStatus) {

                voiceStatus.style.display =
                    "block";


                voiceStatus.innerText =
                    "✅ Finished speaking.";

            }

        };


    /* --------------------------------------
       SPEECH ERROR
    -------------------------------------- */

    utterance.onerror =
        function (event) {

            console.error(
                "Speech synthesis error:",
                event
            );


            if (voiceStatus) {

                voiceStatus.style.display =
                    "block";


                voiceStatus.innerText =
                    "⚠️ Voice stopped.";

            }

        };


    window.speechSynthesis.speak(
        utterance
    );

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
        function (voice) {

            console.log(
                voice.name,
                "-",
                voice.lang
            );

        }
    );

}


if (
    "speechSynthesis" in window
) {

    window.speechSynthesis.onvoiceschanged =
        loadVoices;


    loadVoices();

}


/* ==========================================
   SPEAK BUTTON
========================================== */

const speakButton =
    document.getElementById("speakButton");


if (speakButton) {

    speakButton.addEventListener(
        "click",
        speakResult
    );

}


/* ==========================================
   STOP SPEAKING BUTTON
========================================== */

const stopButton =
    document.getElementById("stopButton");


if (stopButton) {

    stopButton.addEventListener(
        "click",
        function () {

            window.speechSynthesis.cancel();


            if (voiceStatus) {

                voiceStatus.style.display =
                    "block";


                voiceStatus.innerText =
                    "⏹️ Voice stopped.";

            }

        }
    );

}