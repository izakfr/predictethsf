'use strict';

$(function () {
    'use strict';
    // Change this to the location of your server-side upload handler:
    var url = "https://jquery-file-upload.appspot.com/";
    $('#fileupload').fileupload({
        url: url,
        dataType: 'json',
        done: function (e, data) {
            $.each(data.result.files, function (index, file) {
                $('<p/>').text(file.name).appendTo('#files');
            });
        },
        progressall: function (e, data) {
            var progress = parseInt(data.loaded / data.total * 100, 10);
            $('#progress .progress-bar').css({
                'width': progress + '%',
                'text-align': 'center'
            })
                .text(progress + '%');
        }
    }).prop('disabled', !$.support.fileInput)
        .parent().addClass($.support.fileInput ? undefined : 'disabled');
});