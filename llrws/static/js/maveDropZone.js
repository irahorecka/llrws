Dropzone.autoDiscover = false;

$("#score-upload-csv").dropzone({
    // Allow removal up uploaded files.
    addRemoveLinks: true,
    maxFiles: 1,
    init: function() {
        // Get intance of Dropzone object.
        var scoreCSVDropzone = Dropzone.forElement("#score-upload-csv");
        this.on("error", function(file, response) {
            invokeJobSuspension("#score-upload-csv", "#score-accordion span.file-invalid");
        });
        this.on("maxfilesexceeded", function(file, response) {
            this.removeFile(file);
        });
        this.on("removedfile", function(file, response) {
            executeOnRemovedFile("#score-upload-csv", "#score-accordion span.file-status");
        });
        this.on("success", function(file, response) {
            executeOnSuccess(scoreCSVDropzone, "#score-upload-csv", "#score-accordion span.file-valid");
        });
    }
});

$("#benchmark-upload-csv").dropzone({
    // Allow removal up uploaded files.
    addRemoveLinks: true,
    maxFiles: 1,
    init: function() {
        // Get intance of Dropzone object.
        var benchmarkCSVDropzone = Dropzone.forElement("#benchmark-upload-csv");
        this.on("error", function(file, response) {
            invokeJobSuspension("#benchmark-upload-csv", "#benchmark-accordion span.file-invalid");
        });
        this.on("maxfilesexceeded", function(file, response) {
            this.removeFile(file);
        });
        this.on("removedfile", function(file, response) {
            executeOnRemovedFile("#benchmark-upload-csv", "#benchmark-accordion span.file-status");
        });
        this.on("success", function(file, response) {
            executeOnSuccess(benchmarkCSVDropzone, "#benchmark-upload-csv", "#benchmark-accordion span.file-valid");
        });
    }
});

function executeOnRemovedFile(DropzoneElementID, fileStatusSelector) {
    if (anyErrorFilesPresent()) {
        invokeJobSuspension(DropzoneElementID, fileStatusSelector);
        return;
    }
    // Why default to invokeJobOpen()? A: You'll never be in a state to submit files for MAVE
    // processing AFTER you remove your file(s). I.e., Number of files after removal will always be
    // less than value of DropzoneObj.options.maxFiles.
    invokeJobOpen(DropzoneElementID, fileStatusSelector);
}

function executeOnSuccess(DropzoneObj, DropzoneElementID, fileStatusSelector) {
    // On successful upload, the number of uploads should equal the max size
    // and there should be no error files present.
    if (DropzoneObj.files.length == DropzoneObj.options.maxFiles) {
        if (anyErrorFilesPresent() || isDuplicateFile(DropzoneObj)) {
            invokeJobSuspension(DropzoneElementID, fileStatusSelector);
            return;
        }
        invokeJobReady(DropzoneElementID, fileStatusSelector);
        return;
    }
    // At this point, we know a 200 response was received from the server
    // - therefore we assume we have ONE valid file in the Dropzone instance.
    invokeJobOpen(DropzoneElementID, fileStatusSelector);
}

function anyErrorFilesPresent() {
    /**
     * Checks if any Dropzone-flagged error files are present on the DOM.
     * @return {[bool]} Indicates whether there are or are not error files.
     */
    var errorMessages = new Set();
    $(".dz-error-message span").each(function(){
        errorMessages.add($(this).text().trim().length);
    });
    if (errorMessages.size > 1 && errorMessages.values().next() != 0) {
        // 0 represents a valid file.
        return true;
    }
    return false;
}

function isDuplicateFile(DropzoneObj) {
    /**
     * Checks if duplicate files are present in a Dropzone object.
     * @param  {[object]} DropzoneObj An instance of the Dropzone object.
     * @return {[bool]} Indicates whether there are or are not duplicate files.
     */
    var fileNames = DropzoneObj.getAcceptedFiles().map(x => x.name);
    var uniqueFileNames = new Set(fileNames)
    if (uniqueFileNames.size != fileNames.length) {
        return true;
    }
    return false;
}
