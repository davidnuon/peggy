var z;

(function () {

	window.onload = function () {

		var codebox, venster, closebox, editor, demo_code;

		venster = document.getElementById('venster');
		codebox = document.getElementById('codebox');
		closebox = document.getElementById('close');
		openbox = document.getElementById('open');
		editor = document.getElementById('modal-editor');
		demo_code = document.getElementById('demo_code');

		var the_code = function() { return codebox.value; };
		var set_frame = function(str) {
			venster.contentDocument.documentElement.getElementsByTagName('body')[0].innerHTML = str;
		}



		codebox.oninput = function(e) {
			console.log(the_code());
			set_frame(the_code());
		}

		codebox.onpropertychange = codebox.oninput;

		closebox.onclick = function() {
			editor.style.display = 'none';
			openbox.style.display = 'block';
		};

		openbox.onclick = function() {
			editor.style.display = 'block';
			openbox.style.display = 'none';
		}
		

		codebox.value = demo_code.innerHTML;
		set_frame(the_code());
	};
})();
