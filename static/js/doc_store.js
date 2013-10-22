var document_store = function () {
	return {
		docs : {},
		current : '',

		set : function (s) {
			this.docs[this.current].content = s;
		},

		get : function() {
			return this.docs[this.current].content;
		},

		add : function (name) {
			this.docs[name] = {
				name : name,
				content : '',
				set : function (s) {
					this.content = s;
				},
				get : function () {
					return this.content;
				}
			}
		},

		change : function (e) {
			this.current = e;
		}
	};
}