var PostModel = Backbone.Model.extend({
    idAttribute: 'pid',
    defaults: {
        pid: null,
        title: '',
        content: '',
        created_at: '',
        updated_at: '',
        is_published: false
    },
    urlRoot: '/admin/api/posts'
});


var PostsCollection = Backbone.Collection.extend({
    model: PostModel,
    url: '/admin/api/posts'
});


var Router = Backbone.Router.extend({
    initialize: function(opt){},
    routes: {
        '(:pid)(/)': 'post'
    },
    open: function(pid){
        this.navigate(pid, {trigger: true});
    }
});


function onAnyError(){
    console.error('ERROR:', arguments);
    alert('Ошибка!!');
}


var ListView = Backbone.View.extend({
    initialize: function(opt){
        _.bindAll(this, 'render');
    },

    template: _.template($('.list-template').text()),

    events: {
        'click .list__item-link': 'onItemClick'
    },

    render: function(){
        this.$el.html(
            this.template({posts: this.collection})
        );
        return this;
    },

    update: function(){
        this.collection.fetch().done(this.render).fail(onAnyError);
    },

    setLock: function(state){
        this.locked = state;
    },

    onItemClick: function(ev){
        ev.preventDefault();
        if (!this.locked){
            var pid = String($(ev.target).data('pid'));
            this.trigger('open', pid);
        }
    },

    markCurrent: function(pid){}
});


var EditorView = Backbone.View.extend({
    initialize: function(opt){
        _.bindAll(this, 'render', 'onEdit');
        this.onEditDebounced = _.debounce(this.onEdit, 5000);
    },

    template: _.template($('.editor-template').html()),

    events: {
        'submit': 'onSubmit',
        'click .editor__save': 'onSaveButtonClick',
        'input': 'onEditDebounced'
    },

    render: function(){
        this.$el.html(
            this.template(this.model.attributes)
        );
        return this;
    },

    update: function(pid){
        if (pid) {
            this.model.set('pid', pid);
            this.model.fetch().done(this.render).fail(onAnyError);
        }
        else {
            this.model = new PostModel({});
            this.render();
        }
    },

    onSubmit: function(ev){
        ev.preventDefault();
    },

    onEdit: function(){
        this.model
            .save({
                title: this.$('.editor__title').val(),
                content: this.$('.editor__content').val(),
                created_at: this.$('.editor__created-at').val(),
                is_published: this.$('.editor__is-published').is(':checked')
            })
            .fail(onAnyError);
    },

    onSaveButtonClick: function(){
        this.model.save().fail(onAnyError);
    },

    onCancelButtonClick: function(){},
});


var MainView = Backbone.View.extend({
    initialize: function(opt){
        // Posts collection
        this.posts = new PostsCollection();

        // Current post model storage
        this.currentPost = new PostModel({});

        // Initialize posts list
        this.list = new ListView({
            el: this.$('.list'),
            collection: this.posts
        });

        // Intialize editor
        this.editor = new EditorView({
            el: this.$('.editor'),
            model: this.currentPost
        });

        // Configure router
        this.router = new Router({});
        this.list.listenTo(this.router, 'route:post', this.list.update);
        this.editor.listenTo(this.router, 'route:post', this.editor.update);
        Backbone.history.start({
            root: '/admin/posts',
            pushState: true
        });

        // Connect object events listeners
        this.router.listenTo(this.list, 'open', this.router.open);
        // this.list.listenTo(this.editor, 'edit', this.list.setLock);


        // $(window).on('beforeunload', function(){
        //     return "А может нинада?";
        // });
    }
});

// START!!
var main = new MainView({
    el: $('body')
});
