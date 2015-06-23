var edx = edx || {};

(function(Backbone, $, _) {
    'use strict';

    edx.coursware = edx.coursware || {};
    edx.coursware.proctored_exam = {};

    edx.coursware.proctored_exam.ProctoredExamView = Backbone.View.extend({
        initialize: function (options) {
            //Backbone.$.ajaxSetup({ cache: false });
            this.$el = options.el;
            this.model = options.model;
            this.templateId = options.proctored_template;
            this.template = null;
            this.timerId = null;

            var template_html = $(this.templateId).text();
            if (template_html !== null) {
                /* don't assume this backbone view is running on a page with the underscore templates */
                this.template = _.template(template_html);
            }
            /* re-render if the model changes */
            this.listenTo(this.model,'change', this.modelChanged);

            /* make the async call to the backend REST API */
            /* after it loads, the listenTo event will file and */
            /* will call into the rendering */
            this.model.fetch();
        },
        modelChanged: function() {
            this.render();
        },
        render: function () {
            if (this.template !== null) {
                var html = this.template(this.model.toJSON());
                this.$el.html(html);
                this.$el.show();
                this.updateRemainingTime(this);
                this.timerId = setInterval(this.updateRemainingTime, 1000, this);
            }
            return this;
        },

        updateRemainingTime: function (self) {
            self.$el.find('div.exam-timer').removeClass("low-time warning critical");
            self.$el.find('div.exam-timer').addClass(self.model.getRemainingTimeState());
            self.$el.find('span#time_remaining_id b').html(self.model.getFormattedRemainingTime());
            if (self.model.getRemainingSeconds() <= 0) {
                clearInterval(self.timerId); // stop the timer once the time finishes.
            }
        }
    });
    this.edx.coursware.proctored_exam.ProctoredExamView = edx.coursware.proctored_exam.ProctoredExamView;
}).call(this, Backbone, $, _);