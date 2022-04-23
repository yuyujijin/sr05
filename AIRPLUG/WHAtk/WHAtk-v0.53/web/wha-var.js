// Associative array of all variables of the application that may be
// updated when receiving JSON objects through the websocket.
const appvar = [];


// Variable "msg2rcv": msg received and forwared by WHAtk; to be displayed
// Standard construction until "You may perform other actions here"
// Here the action consists in updating the field "msg2rcv-tag"
appvar["msg2rcv"] = {
  value:undefined,
  get() {
    return this.value
  },
  set(val) {
    // Add a comment in the log (in case webjs option --debug is used)
    addToLog("+ set msg = [" + val + "]", "LimeGreen")
    // Affect the value
		this.value = val;

			
		// You may perform other actions here

		tag = document.getElementById("msg2rcv-tag");
		if( tag != null ) {
				tag.innerHTML = this.value;
		}
  }
};
