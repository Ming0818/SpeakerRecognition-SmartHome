window.Fr = typeof Fr == "undefined" ? {} : window.Fr;
(function ($) {
    Fr.voice = {
        workerPath: "js/recorderWorker.js",
        stream: false,

        init_called: false,

        init: function () {
            try {
                // Fix up for prefixing
                
                window.URL = window.URL || window.webkitURL;
                if (navigator.getUserMedia === false) {
                    alert('getUserMedia() is not supported in your browser');
                }
                
            } catch (e) {
                alert('Web Audio API is not supported in this browser');
            }
        },

        /**
         * Start recording audio
         */
        successCallback: function (stream) {
            
            debugger
            // this.context = new AudioContext();
            // audio_context = new AudioContext;

            var audioContext = window.AudioContext || window.webkitAudioContext;
            var context = new audioContext();

            var input = context.createMediaStreamSource(stream);
           
            
            input.connect(context.destination);
            
            this.recorder = new Recorder(input, {
                workerPath: this.workerPath
            });
            this.stream = stream;
            this.recorder.record();
            callback(stream);
        },
        errorCallback: function (err) {
            debugger
            console.log(err)
            alert('No live audio input');
        },

        record: function (output, callback) {
            debugger
            if (this.init_called === false) {
                this.init();
                this.init_called = true;
            }
            navigator.mediaDevices.getUserMedia({ audio: true }).then(this.successCallback).catch(this.errorCallback);
        },

        /**
         * Stop recording audio
         */
        stop: function () {
            this.recorder.stop();
            this.recorder.clear();
            this.stream.stop();
            return this;
        },

        /**
         * Export the recorded audio to different formats :
         * BLOB, MP3, Base64, BLOB URL
         */
        export: function (callback, type) {
            if (type == "mp3") {
                this.recorder.exportMP3(callback);
            } else {
                this.recorder.exportWAV(function (blob) {
                    if (type == "" || type == "blob") {
                        callback(blob);
                    } else if (type == "base64") {
                        var reader = new window.FileReader();
                        reader.readAsDataURL(blob);
                        reader.onloadend = function () {
                            base64data = reader.result;
                            callback(base64data);
                        };
                    } else if (type == "URL") {
                        var url = URL.createObjectURL(blob);
                        callback(url);
                    }
                });
            }
        }
    };
})(jQuery);
