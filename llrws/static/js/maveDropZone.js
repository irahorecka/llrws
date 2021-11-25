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
            if (anyErrorFilesPresent()) {
                invokeJobSuspension();
                return;
            }
            // Cleans up file type dictionary of removed files.
            if (maveCSVDropzone.files.length == 1 && Object.keys(loadedFileTypes).length > 1) {
                delete loadedFileTypes[file.name];
            }
            if (areBothBenchmarkAndScoreFilesLoaded(maveCSVDropzone, loadedFileTypes)) {
                invokeJobReady();
                return;
            }
            invokeJobOpen();
        });

        this.on("success", function(file, response) {
            // On successful upload, the number of uploads should equal the max size
            // and there should be no error files present.
            if (maveCSVDropzone.files.length == maveCSVDropzone.options.maxFiles) {
                if (anyErrorFilesPresent() || isDuplicateFile(maveCSVDropzone)) {
                    invokeJobSuspension();
                } else {
                    invokeJobReady();
                }
                return;
            }
            // Check both correct filetypes are loaded
            loadedFileTypes[file.name] = response;
            if (areBothBenchmarkAndScoreFilesLoaded(maveCSVDropzone, loadedFileTypes)) {
                invokeJobReady();
            } else {
                invokeJobOpen();
            }
        });
    }
});

function invokeJobReady() {
    invokeBorderColor("rgb(52, 168, 83)");
    $('#mave-button-submit').prop('disabled', false);
}

function invokeJobSuspension() {
    invokeBorderColor("rgb(220, 53, 69)");
    $('#mave-button-submit').prop('disabled', true);
}

function invokeJobOpen() {
    invokeBorderColor("rgb(0, 135, 247)");
    $('#mave-button-submit').prop('disabled', true);
}

function invokeBorderColor(color) {
    setTimeout(function(){
        $("#mave-upload-csv").css("border", "2px dashed " + color);
    }, 200);
}

function anyErrorFilesPresent() {
    var errorMessages = new Set();
    $(".dz-error-message span").each(function(){
        errorMessages.add($(this).text().trim().length);
    });
    if (errorMessages.size > 1 && errorMessages.values().next() != 0) {
        // 0 represents a valid file
        return true;
    }
    return false;
}

function areBothBenchmarkAndScoreFilesLoaded(DropzoneObj, loadedFileTypes) {
    var filesInDropzone = DropzoneObj.getAcceptedFiles()
    var filenamesInDropzone = filesInDropzone.map(x => loadedFileTypes[x.name])
    if (filesInDropzone.length == 2) {
        if ("benchmark" in filenamesInDropzone && "score" in filenamesInDropzone) {
            return true;
        }
    }
    return false;
}

function isDuplicateFile(DropzoneObj) {
    var fileNames = DropzoneObj.getAcceptedFiles().map(x => x.name);
    var uniqueFileNames = new Set(fileNames)
    if (uniqueFileNames.size == 1) {
        return true;
    }
    return false;
}
