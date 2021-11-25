function invokeJobReady() {
    /**
     * Sets border color of #mave-upload-csv element to green and enables
     * submit button.
     */
    invokeBorderColor("rgb(52, 168, 83)");
    setDefaultButtonState();
    $('#mave-button-submit').prop('disabled', false);
}

function invokeJobSuspension() {
    /**
     * Sets border color of #mave-upload-csv element to red and disables
     * submit button.
     */
    invokeBorderColor("rgb(220, 53, 69)");
    $('#mave-button-submit').prop('disabled', true);
}

function invokeJobOpen() {
    /**
     * Sets border color of #mave-upload-csv element to blue and disables
     * submit button.
     */
    invokeBorderColor("rgb(0, 135, 247)");
    $('#mave-button-submit').prop('disabled', true);
}

function invokeBorderColor(color) {
    /**
     * Sets border color of #mave-upload-csv element
     * @param  {[string]} color Color to set border color.
     */
    setTimeout(function(){
        $("#mave-upload-csv").css("border", "2px dashed " + color);
    }, 200);
}

function setLoadingButtonState() {
    /**
     * Sets MAVE submit button text to 'Loading...' and disables button.
     */
	$('#mave-button-submit').val('Loading...').prop('disabled', true);
}

function setDefaultButtonState() {
    /**
     * Sets MAVE submit button text to 'Get MAVE' and disables button.
     */
	$('#mave-button-submit').val('Get MAVE').prop('disabled', true);
}

function scrollToBottomOfPage() {
    /**
     * Scrolls to bottom of page to show table.
     */
	$("html, body").animate({
		scrollTop: document.body.scrollHeight
	}, "slow");
}
