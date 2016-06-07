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
        return '#posts/' + this.get('pid');
    },

    toJSON: function(){
        return this.omit.apply(this, this.private);
    }
});


var PostsCollection = Backbone.Collection.extend({
    model: PostModel,
    url: '/admin/api/posts'
});