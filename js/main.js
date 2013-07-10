(function () {

	window.onload = function () {

		var codebox, venster, closebox, editor, demo_code;

		venster = document.getElementById('venster');
		codebox = document.getElementById('codebox');
		closebox = document.getElementById('close');
		editor = document.getElementById('modal-editor');
		demo_code = document.getElementById('demo_code');


		venster.contentDocument.documentElement.style.background = '#fff';


		var the_code = function() { return codebox.value; };
		var set_frame = function(str) {
			venster.contentDocument.documentElement.getElementsByTagName('body')[0].innerHTML = str;
		}


		var options = CodeMirror.defaults;
		options.lineNumbers = true;
		options.value = demo_code.innerHTML;



		var editor = CodeMirror(codebox, options);
		editor.on("change", function () {
			set_frame(editor.getValue());
		});


		set_frame(editor.getValue())

	};
})();
