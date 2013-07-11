(function () {
	var codebox, venster, pane, editor, demo_code;
	
	// This is the iframe where we will be updating content
	venster = document.getElementById('venster');

	// Left-side pane where we have controls
	pane = document.getElementById('modal-editor');
	
	// <div> to hold the codemirror editor
	codebox = document.getElementById('codebox');

	// <template> that holds initial content for the editor
	demo_code = document.getElementById('demo_code');

	// Set the iframe background color to white
	venster.contentDocument.documentElement.style.background = '#fff';

	// Helper to set the content of the document of the iframe
	var set_frame = function(str) {
		venster.contentDocument.documentElement.getElementsByTagName('body')[0].innerHTML = str;
	}


	// Codemirror options
	var options = CodeMirror.defaults;
	options.lineNumbers = true;
	options.value = demo_code.innerHTML;
	options.lineWrapping = true;

	window.onload = function () {

		editor = CodeMirror(codebox, options);
		editor.on("change", function () {
			set_frame(editor.getValue());
		});

		window.onresize();

		set_frame(editor.getValue())
	};

	window.onresize = function () {
		editor.setSize("100%", pane.offsetHeight - 40);
	}
})();