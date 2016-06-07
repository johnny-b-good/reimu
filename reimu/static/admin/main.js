var Router = Backbone.Router.extend({
    routes: {
        'posts/new(/)': 'create',
        'posts/:pid(/)': 'edit',
        'posts(/)': 'list',
        '': 'list',
        '*fuck': 'none'
    }
});



var MainView = Backbone.View.extend({
    initialize: function(opt){
        // Posts collection
        this.posts = new PostsCollection();

        // Initialize posts list
        this.list = new ListView({
            el: this.$('.admin'),
            collection: this.posts
        });

        // Intialize editor
        this.editor = new EditorView({
            el: this.$('.admin'),
            model: new PostModel({})
        });

        // Configure router
        this.router = new Router({});

        // Listen to router events
        this.editor.listenTo(this.router, 'route:create', this.editor.update);
        this.editor.listenTo(this.router, 'route:edit', this.editor.update);
        this.list.listenTo(this.router, 'route:list', this.list.update);

        this.router.on('route', console.log);

        // Start routing
        Backbone.history.start({
            root: '/admin/',
            pushState: true
        });
    }
});

// START!!
var main = new MainView({
    el: $('body')
});