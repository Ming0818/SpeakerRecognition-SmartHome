/**
 * Created by Vishv on 5/10/17.
 */
function restore(){
    $("#record, #live").removeClass("disabled");
    Fr.voice.stop();
//    $(".one").addClass("disabled");
}
$(document).ready(function(){
    // Record the audio on clicking record button
    $(document).on("click", "#record:not(.disabled)", function(){
	debugger
        elem = $(this);
        Fr.voice.record($("#live").is(":checked"), function(){
            elem.addClass("disabled");
            $("#live").addClass("disabled");
            $(".one").removeClass("disabled");

            // get the 2 second binary data
            setTimeout(function() {
                Fr.voice.export(function(blob){

                    console.log("called");
                    var data = new FormData();
                    // data.append('fname', 'test.wav');
                    data.append('file', blob);
                    console.log(blob);
                    // send binary data to backend server for storage.
                    $.ajax({
                        url: "/save/wavfile",
                        type: 'POST',
                        data: data,
                        contentType: false,
                        processData: false,
                        success: function(data) {
                            console.log(data);
                            //clear the audio buffer
                            restore();
                        }
                    });
                }, "blob");
            }, 3000);
        });

    });

});
