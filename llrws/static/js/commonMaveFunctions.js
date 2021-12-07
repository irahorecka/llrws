/**
 * All var(--*) variables in this file are sourced from css/main.css
 */


function invokeJobReady(borderSelector, fileStatusSelector) {
    /**
     * Sets border color of Dropzone element to green and enables
     * submit button.
     * @param  {[string]} borderSelector Border selector to change color
     * @param  {[string]} fileStatusSelector File status selector to make visible
     */
    setBorderColor(borderSelector, "var(--success-color)");
    setFileStatusVisible(fileStatusSelector);
    setDefaultButtonState();
    $('#mave-button-submit').prop('disabled', false);
}

function invokeJobSuspension(borderSelector, fileStatusSelector) {
    /**
     * Sets border color of Dropzone element to red and disables
     * submit button.
     * @param  {[string]} borderSelector Border selector to change color
     * @param  {[string]} fileStatusSelector File status selector to make visible
     */
    setBorderColor(borderSelector, "var(--failure-color)");
    setFileStatusVisible(fileStatusSelector);
    $('#mave-button-submit').prop('disabled', true);
}

function invokeJobOpen(borderSelector, fileStatusSelector) {
    /**
     * Sets border color of Dropzone element to blue and disables
     * submit button.
     * @param  {[string]} borderSelector Border selector to change color
     * @param  {[string]} fileStatusSelector File status selector to hide
     */
    setBorderColor(borderSelector, "var(--neutral-color)");
    setFileStatusHidden(fileStatusSelector);
    $('#mave-button-submit').prop('disabled', true);
}

function setBorderColor(borderSelector, borderColor) {
    /**
     * Sets border color of `borderSelector` element to `color`
     * @param  {[string]} color Color to set border color
     */
    setTimeout(function(){
        $(borderSelector).css("border-color", borderColor);
    }, 200);
}

function setFileStatusVisible(fileStatusSelector) {
    /**
     * Sets `fileStatusSelector` visibility to visible
     * @param  {[string]} fileStatusSelector Selector to make visible
     */
    setFileStatusHidden(fileStatusSelector);
    setTimeout(function(){
        $(fileStatusSelector).fadeIn(200);
    }, 100);
}

function setFileStatusHidden(fileStatusSelector) {
    /**
     * Sets `fileStatusSelector` visibility to hidden
     * * @param  {[string]} fileStatusSelector Selector to hide
     */
     setTimeout(function(){
        $(fileStatusSelector).fadeOut(200);
    }, 100);
}

function setLoadingButtonState(buttonSelector) {
    /**
     * Sets button text to 'Loading...' and disables button.
     */
	$(buttonSelector).val('Loading...').prop('disabled', true);
}

function setDefaultButtonState(buttonSelector) {
    /**
     * Sets button text to 'Get MAVE LLR' and disables button.
     */
	$(buttonSelector).val('Get MAVE LLR').prop('disabled', true);
}

function scrollToBottomOfPage() {
    /**
     * Scrolls to bottom of page to show table.
     */
	$("html, body").animate({
		scrollTop: document.body.scrollHeight
	}, "slow");
}
