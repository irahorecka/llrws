/**
 * All var(--*) variables are sourced from css/main.css
 */


function invokeJobReady() {
    /**
     * Sets border color of #mave-upload-csv element to green and enables
     * submit button.
     */
    invokeBorderColor("var(--success-color)");
    invokeFileStatus(".file-valid");
    setDefaultButtonState();
    $('#mave-button-submit').prop('disabled', false);
}

function invokeJobSuspension() {
    /**
     * Sets border color of #mave-upload-csv element to red and disables
     * submit button.
     */
    invokeBorderColor("var(--failure-color)");
    invokeFileStatus(".file-invalid");
    $('#mave-button-submit').prop('disabled', true);
}

function invokeJobOpen() {
    /**
     * Sets border color of #mave-upload-csv element to blue and disables
     * submit button.
     */
    invokeBorderColor("var(--neutral-color)");
    invokeFileStatusHidden();
    $('#mave-button-submit').prop('disabled', true);
}

function invokeBorderColor(color) {
    /**
     * Sets border color of #mave-upload-csv element
     * @param  {[string]} color Color to set border color.
     */
    setTimeout(function(){
        $("#mave-upload-csv").css("border-color", color);
    }, 200);
}

function invokeFileStatus(selector) {
    /**
     * Sets selector CSS attribute "visibility" to "visible"
     * @param  {[string]} selector Selector to make visible.
     * @param  {[string]} visibility Visibility attribute.
     */
    invokeFileStatusHidden();
    setTimeout(function(){
        $(selector).show();
    }, 200);
}

function invokeFileStatusHidden() {
    /**
     * Sets the following selector CSS classes visibility to hidden:
     * - .file-valid
     * - .file-invalid
     */
    $(".file-valid").hide();
    $(".file-invalid").hide();
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
