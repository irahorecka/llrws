Dropzone.autoDiscover = false;
$("#mave-upload-csv").dropzone({
    addRemoveLinks: true,
    maxFiles: 2,
    removedfile: function(file) {
        $.ajax({
            type: "POST",
            url: "/upload",
        });
        var _ref;
        return (_ref = file.previewElement) != null ? _ref
            .parentNode.removeChild(file.previewElement) : void 0;
    },
    init: function() {
        // Get intance of Dropzone object
        var maveCSVDropzone = Dropzone.forElement("#mave-upload-csv");
        var loadedFileTypes = new Object();
        this.on("error", function(file, response) {
            invokeJobSuspension();
        });

        this.on("maxfilesexceeded", function(file, response) {
            this.removeFile(file);
        });

        this.on("removedfile", function(file, response) {
            // Keep submit button disabled unless two valid files are loaded.
            if (maveCSVDropzone.files.length != maveCSVDropzone.options.maxFiles) {
                $('#mave-button-submit').prop('disabled', true);
            }
            // Check if any error files present on file removal.
            if (anyErrorFilesPresent()) {
                invokeJobSuspension();
            } else {
                invokeJobReady();
            }
            // Cleans up file type dictionary of removed files.
            if (maveCSVDropzone.files.length == 1 && Object.keys(loadedFileTypes).length > 1) {
                delete loadedFileTypes[file.name];
            }
            // Check both correct filetypes are loaded
            if (bothBenchmarkAndScoreFilesLoaded(loadedFileTypes)) {
                invokeJobReady();
            } else {
                invokeJobSuspension();
            }
            // No more files in Dropzone instance.
            if (maveCSVDropzone.files.length == 0) {
                invokeJobReady();
            } else {
                invokeJobSuspension();
            }
        });

        this.on("success", function(file, response) {
            // On successful upload, the number of uploads should equal the max size
            // and there should be no error files present.
            if (maveCSVDropzone.files.length == maveCSVDropzone.options.maxFiles) {
                if (anyErrorFilesPresent()) {
                    invokeJobSuspension();
                } else {
                    invokeJobReady();
                }
            }
            // Check both correct filetypes are loaded
            loadedFileTypes[file.name] = response;
            if (bothBenchmarkAndScoreFilesLoaded(loadedFileTypes)) {
                invokeJobReady();
            } else {
                invokeJobSuspension();
            }
        });
    }
});

function invokeJobReady() {
    invokeBorderColor("rgb(0, 135, 247)");
    $('#mave-button-submit').prop('disabled', false);
}

function invokeJobSuspension() {
    invokeBorderColor("rgb(220, 53, 69)");
    $('#mave-button-submit').prop('disabled', true);
}

function invokeBorderColor(color) {
    setTimeout(function(){
        $("#mave-upload-csv").css("border", "2px dashed " + color);
    }, 200);
}

function anyErrorFilesPresent() {
    var noErrorMessage = new Set();
    $(".dz-error-message span").each(function(){
        noErrorMessage.add($(this).text().trim().length);
    });
    if (noErrorMessage.size > 1 && noErrorMessage.values().next() != 0) {
        return true;
    }
    return false;
}

function bothBenchmarkAndScoreFilesLoaded(loadedFileTypes) {
    currentFileTypes = new Set();
    for (var key in loadedFileTypes){
        currentFileTypes.add(loadedFileTypes[key]);
    }
    if (currentFileTypes.has("benchmark") && currentFileTypes.has("score")) {
        return true;
    }
    return false;
}
