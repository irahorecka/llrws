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
    setInactiveButtonState();
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
    setInactiveButtonState();
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
    setInactiveButtonState();
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

function setLoadingButtonState() {
    /**
     * Sets MAVE submit button text to 'Loading...' and disables button.
     */
	$('#mave-button-submit').val('Loading...').prop('disabled', true);
}

function setActiveButtonState() {
    /**
     * Sets MAVE submit button text to 'Get MAVE LLR' and enables button.
     */
	$('#mave-button-submit').val('Get MAVE LLR').prop('disabled', false);
}

function setInactiveButtonState() {
    /**
     * Sets MAVE submit button text to 'Get MAVE LLR' and disables button.
     */
	$('#mave-button-submit').val('Get MAVE LLR').prop('disabled', true);
}

function scrollToBottomOfPage() {
    /**
     * Scrolls to bottom of page to show table.
     */
	$("html, body").animate({
		scrollTop: document.body.scrollHeight
	}, "slow");
}
