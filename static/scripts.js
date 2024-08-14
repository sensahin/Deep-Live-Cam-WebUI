let isRecording = false;

function uploadFace() {
    var formData = new FormData(document.getElementById('upload-form'));
    var xhr = new XMLHttpRequest();
    xhr.open('POST', uploadUrl, true);

    xhr.onload = function () {
        if (xhr.status === 200) {
            document.getElementById('live-button').disabled = false;
            document.getElementById('record-button').disabled = false;

            var fileInput = document.getElementById('face');
            var storedFilename = document.getElementById('stored-filename');
            storedFilename.value = fileInput.value.split('\\').pop();

            var messageElement = document.getElementById('message');
            messageElement.innerText = "File uploaded successfully!";
            document.getElementById('error-message').innerText = "";

            setTimeout(function() {
                messageElement.innerText = "";
            }, 5000);

        } else {
            document.getElementById('message').innerText = "";
            document.getElementById('error-message').innerText = "An error occurred during file upload.";
        }
    };

    xhr.send(formData);
}

function startLive() {
    var progressBar = document.getElementById('progress-bar');
    var img = document.getElementById('live-stream');
    var stopButton = document.getElementById('stop-button');

    progressBar.style.display = "block";
    img.style.display = "none";
    stopButton.disabled = false;

    img.onload = function() {
        progressBar.style.display = "none";
        img.style.display = "block";
    };

    img.src = liveUrl;
}

function stopLive() {
    var img = document.getElementById('live-stream');
    var stopButton = document.getElementById('stop-button');

    img.src = "";
    img.style.display = "none";
    stopButton.disabled = true;

    // Stop recording if it's active
    if (isRecording) {
        stopRecording();
    }
}

function startRecording() {
    isRecording = true;
    document.getElementById('record-button').disabled = true;
    document.getElementById('stop-record-button').disabled = false;

    // Send a request to the server to start recording
    var xhr = new XMLHttpRequest();
    xhr.open('POST', startRecordUrl, true);
    xhr.send();
}

function stopRecording() {
    isRecording = false;
    document.getElementById('record-button').disabled = false;
    document.getElementById('stop-record-button').disabled = true;

    // Send a request to the server to stop recording
    var xhr = new XMLHttpRequest();
    xhr.open('POST', stopRecordUrl, true);
    xhr.send();
}
