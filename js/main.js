(function () {
	var codebox, venster, closebox, pane, editor, demo_code;

	venster = document.getElementById('venster');
	codebox = document.getElementById('codebox');
	closebox = document.getElementById('close');
	pane = document.getElementById('modal-editor');
	demo_code = document.getElementById('demo_code');

	venster.contentDocument.documentElement.style.background = '#fff';

	var set_frame = function(str) {
		venster.contentDocument.documentElement.getElementsByTagName('body')[0].innerHTML = str;
	}

	var options = CodeMirror.defaults;
	options.lineNumbers = true;
	options.value = demo_code.innerHTML;


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