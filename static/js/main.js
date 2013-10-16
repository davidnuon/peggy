(function () {
	// Helpers
	function $(id) {
		return document.getElementById(id);
	}

	function getChildNodes(el) {
		var out = [];
 
		for (var i = el.childNodes.length - 1; i >= 0; i--) {
			out[out.length] = el.childNodes[i];
		};
 
 		return out;
	}


	// Helper to set the content of the document of the iframe
	var set_frame = function(str) {
		venster.contentDocument.documentElement.getElementsByTagName('body')[0].innerHTML = str;
	}

	// Helper to set the content of the document of the iframe
	var set_css = function(str) {
		venster.contentDocument.documentElement.getElementsByTagName('style')[0].innerHTML = str;
	}

	var codebox, venster, pane, editor, demo_code;
	var the_docs = document_store();

	// This is the iframe where we will be updating content
	venster = $('venster');

	// Left-side pane where we have controls
	pane = $('modal-editor');
	
	// <div> to hold the codemirror editor
	codebox = $('codebox');

	// <template> that holds initial content for the editor
	demo_code = $('demo_code');

	// Making the document
	// Set the iframe background color to white
	//venster.contentDocument.documentElement.style.background = '#fff';
	var head = venster.contentDocument.documentElement.getElementsByTagName('head')[0];
	var style = venster.contentDocument.createElement('style');
	head.insertBefore(style, head[head.length+1]);


	// Editor Controls
	var the_tabs = getChildNodes($('tabs'));
	for (var i = the_tabs.length - 1; i >= 0; i--) {
		if(the_tabs[i].getAttribute) {
			var id = the_tabs[i].getAttribute('id');
			the_docs.add(id);
		};
	};


	the_docs.docs.css.set('body {\n\tbackground:#fff;\n};');

	the_docs.change('html');
	the_docs.set(demo_code.innerHTML);

	// Codemirror options
	var options = CodeMirror.defaults;
	options.lineNumbers = true;
	options.value = the_docs.get();
	options.lineWrapping = true;

	// Make all tabs clickable
	the_tabs.map( function(e) {
		e.onclick = function(event) {
			var me = this;
			var siblings =  getChildNodes(me.parentNode);
			
			if(me.getAttribute('class') === 'selected') { return; }

			for (var i = siblings.length - 1; i >= 0; i--) {
				if(siblings[i].setAttribute) {				
					if(siblings[i] === this) {
						siblings[i].setAttribute('class', 'selected');
					} else {
						siblings[i].setAttribute('class', '');
					} 
				}
			};
			

			the_docs.change(me.getAttribute('id'));
			editor.setValue(the_docs.get());
		};
	});

	window.onload = function () {
		$('html').setAttribute('class', 'selected');

		editor = CodeMirror(codebox, options);
		editor.on("change", function () {
			the_docs.set(editor.getValue());

			if(the_docs.current === 'html') {
				set_frame(the_docs.get());
			}

			if(the_docs.current === 'css') {
				set_css(the_docs.get());		
			}
		});


		window.onresize();

		set_css(the_docs.docs.css.get());
		set_frame(the_docs.docs.html.get());
	};

	window.onresize = function () {
		editor.setSize("100%", pane.offsetHeight - 40);
	}

})();