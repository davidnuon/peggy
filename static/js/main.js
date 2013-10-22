(function () {
	// Helpers
	function getElem(id) {
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
	venster = getElem('venster');

	// Left-side pane where we have controls
	pane = getElem('modal-editor');
	
	// <div> to hold the codemirror editor
	codebox = getElem('codebox');

	// <template> that holds initial content for the editor
	demo_code  = getElem('demo_code');
	demo_css   = getElem('demo_css');
	human_name = getElem('humanname');

	// Making the document
	// Set the iframe background color to white

	var head = venster.contentDocument.documentElement.getElementsByTagName('head')[0];
	var style = venster.contentDocument.createElement('style');
	head.insertBefore(style, head[head.length+1]);


	// Editor Controls
	var the_tabs = getChildNodes(getElem('tabs'));
	for (var i = the_tabs.length - 1; i >= 0; i--) {
		if(the_tabs[i].getAttribute) {
			var id = the_tabs[i].getAttribute('id');
			the_docs.add(id);
		};
	};

	the_docs.add('humanname');
	the_docs.change('humanname');
	the_docs.set(human_name.innerHTML);

	the_docs.change('html');
	the_docs.set(demo_code.innerHTML);
	the_docs.docs.css.set(demo_css.innerHTML);

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
		getElem('html').setAttribute('class', 'selected');

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

		$('#rename').click( function() {
			the_docs.docs.humanname.set(prompt('Enter new name here', the_docs.docs.humanname.get()));
		});
		$('#save').click( function() {
			$.post( "/save", { 
				htmlcontent: the_docs.docs.html.get(), 
				csscontent: the_docs.docs.css.get(),
				humanname: the_docs.docs.humanname.get(),
				documentName: $('#modal-editor').data('docid') } )
			.done(
				function() {
					alert("Saved!");
				})
			.fail(
				function() {

					alert("Error!");
				})
		});
	};

	window.onresize = function () {
		editor.setSize("100%", pane.offsetHeight - 40);
	}

})();
