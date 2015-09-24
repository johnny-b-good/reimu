function onAnyError(){
    console.error('ERROR:', arguments);
    alert('Ошибка!!');
}


var PostModel = Backbone.Model.extend({
    idAttribute: 'pid',

    urlRoot: '/admin/api/posts',

    defaults: {
        pid: undefined,
        title: '',
        content: '',
        created_at: '',
        updated_at: '',
        is_published: false
    },

    private: ['_month', '_year', '_monthYear'],

    initialize: function(attributes, options){
        this.setDateParams(this.get('created_at'));
        this.on('change:created_at', function(model, createdAt){
            this.setDateParams(createdAt);
        }, this);
    },

    setDateParams: function(createdAt){
        var monthNames = {
            '01': 'Январь', '02': 'Февраль', '03': 'Март', '04': 'Апрель', '05': 'Май', '06': 'Июнь',
            '07': 'Июль', '08': 'Август', '09': 'Сентябрь', '10': 'Октябрь', '11': 'Ноябрь', '12': 'Декабрь'
        };
        if (!createdAt) return;
        var dateArray = createdAt.split('.');
        var year = dateArray[2];
        var month = dateArray[1];
        var monthName = monthNames[month];
        var monthYear = monthName + ' ' + year;

        this.set({_month: month, _year: year, _monthYear: monthYear});
    },

    postUrl: function(){
        return '#posts/' + this.get('pid')
    },

    toJSON: function(){
        return this.omit.apply(this, this.private);
    }
});


var PostsCollection = Backbone.Collection.extend({
    model: PostModel,
    url: '/admin/api/posts'
});


var Router = Backbone.Router.extend({
    routes: {
        'posts/new(/)': 'post_edit',
        'posts/:pid(/)': 'post_edit',
        'posts(/)': 'post_list',
        '': 'post_list'
    }
});


var ListView = Backbone.View.extend({
    initialize: function(opt){
        _.bindAll(this, 'render', 'filter');
        this.filterThrottled = _.throttle(this.filter, 1000);
    },

    template: _.template($('.list-template').text()),

    events: {
        'input': 'filterThrottled'
    },

    render: function(){
        this.$el.html(
            this.template({groups: this.makeGroups(this.collection)})
        );
        return this;
    },

    update: function(){
        this.collection.fetch().done(this.render).fail(onAnyError);
    },

    setLock: function(state){
        this.locked = state;
    },

    markCurrent: function(pid){},

    makeGroups: function(collection){
        var groupedCollection = [];
        var table = {};
        collection.each(function(model, index, list){
            var group = model.get('_monthYear');
            if (!table.hasOwnProperty(group)) {
                table[group] = [];
                groupedCollection.push({monthYear: group, posts: table[group]});
            }
            table[group].push(model);
        });
        return groupedCollection;
    },

    filter: function(ev){
        var filterString = this.$('.list__filter').val();
        var hiddenPosts = [];
        this.collection.each(function(post){
            var titleMatches = false;
            var dateMatches = false;
            if (post.get('title')){
                dateMatches = post.get('title').search(filterString) !== -1;
            }
            if (post.get('created_at')){
                titleMatches = post.get('created_at').search(filterString) !== -1;
            }
            if (!(titleMatches || dateMatches)) {
                // hiddenPosts.push(post.get('pid'));
                this.find('.list-item[' +  + ']');
            };
        });

        console.log(filterString, hiddenPosts);
    }
});


var EditorView = Backbone.View.extend({
    initialize: function(opt){
        _.bindAll(this, 'render', 'onSaveSuccess', 'onSaveError');
        this.unsaved = false;
    },

    template: _.template($('.editor-template').html()),

    events: {
        'submit': 'onSubmit',
        'click .editor__save': 'onSaveButtonClick',
        'input': 'onInput'
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
            this.model = new PostModel({
                created_at: this.getTodayDate()
            });
            this.render();
        }
    },

    getTodayDate: function(){
        var today = new Date();
        var month = ((today.getMonth() + 1) >= 10) ? (today.getMonth() + 1) : ('0' + (today.getMonth() + 1))
        var day = (today.getDate() >= 10) ? today.getDate() : ('0' + today.getMonth());
        var year = today.getFullYear();
        return day + '.' + month + '.' + year;
    },

    onInput: function(ev) {
        var formFieldsArray = this.$('.editor__form').serializeArray();
        var formFields = {};
        _.forEach(formFieldsArray, function(el){
            formFields[el.name] = el.value;
        });
        this.model.set(formFields);
        this.toggleUnsaved(true);
    },

    onSubmit: function(ev){
        ev.preventDefault();
    },

    onSaveSuccess: function(){
        this.toggleUnsaved(false);
    },

    onSaveError: function(res){
        // Handle data errors
        if (res.status === 422) {
            var errorText = res.responseJSON.error;
            alert(errorText);
        }
        // Handle any other errors
        else {
            onAnyError.apply(this, arguments);
        }

    },

    toggleUnsaved: function(state){
        this.unsaved = state;
        this.$el.find('.editor__unsaved').toggleClass('editor__unsaved--visible', state);
        this.$el.find('.editor__save').toggleClass('editor__save--visible', state);
        this.$el.find('.editor__cancel').text(state ? 'Отмена' : 'Назад');
    },

    onSaveButtonClick: function(){
      this.model
          .save({
              title: this.$('.editor__title').val(),
              content: this.$('.editor__content').val(),
              created_at: this.$('.editor__created-at').val(),
              is_published: this.$('.editor__is-published').is(':checked')
          })
          .done(this.onSaveSuccess)
          .fail(this.onSaveError);
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

        // Configure navigation handlers
        // Should be done before `Backbone.history.start` to itercept nav events
        _.bindAll(this, 'onWindowHashChange', 'onWindowBeforeUnload');
        this.cancelNavigate = false;
        this.confirmationMessage = 'Есть несохраненные изменения. Покинуть страницу?';
        $(window).on('hashchange', this.onWindowHashChange);
        $(window).on('beforeunload', this.onWindowBeforeUnload);

        // Configure routes
        this.list.listenTo(this.router, 'route:post_list', this.list.update);
        this.editor.listenTo(this.router, 'route:post_edit', this.editor.update);

        // Start routing
        Backbone.history.start({
            root: '/admin'
        });
    },

    onWindowHashChange: function(ev){
        // Do not cancel navigation if there are no unsaved changes in editor
        if (!this.editor.unsaved) return;

        // Prevent navigate events when going back to previous url
        if (this.cancelNavigate) {
      	     ev.stopImmediatePropagation();
             this.cancelNavigate = false;
             return;
      	}

        // Ask user's confirmation on leaving unsaved editor
        var dialog = confirm(this.confirmationMessage);
        if (dialog) {
            // Continue navigation if user agrees
            this.editor.unsaved = false;
        } else {
            // Prevent nav event
            ev.stopImmediatePropagation();
            // Prevent navigate events when going back to previous url
            this.cancelNavigate = true;
            // Go to the previous url
            window.location.href = ev.originalEvent.oldURL;
        }
    },

    onWindowBeforeUnload: function(){
        if (this.editor.unsaved) return this.confirmationMessage;
    }
});

// START!!
var main = new MainView({
    el: $('body')
});
