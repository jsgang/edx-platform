;(function (define) {
    'use strict';
    define([
        'backbone',
        'underscore',
        'gettext',
        'js/components/card/views/card'
    ], function (Backbone, _, gettext, CardView) {
        var TeamMembershipView, TeamCountryLanguageView, TeamCardView;

        TeamMembershipView = Backbone.View.extend({
            tagName: 'div',
            className: 'team-members',
            template: _.template(
                '<span class="member-count"><%= membership_message %></span>' +
                '<ul class="list-member-thumbs"></ul>'
            ),

            render: function () {
                var memberships = this.model.get('membership'),
                    max_member_count = 9999;
                this.$el.html(this.template({
                    membership_message: interpolate(
                        // Translators: The following message displays the number of members on a team.
                        ngettext('%()s / %()s Member', '%()s / %()s Members', max_member_count),
                        {member_count: memberships.length, max_member_count: max_member_count}, true
                    )
                }));
                _.each(memberships, function (membership) {
                    this.$('list-member-thumbs').append(
                        '<li class="item-member-thumb"><img alt="' + membership.user.username + '" src=""></img></li>'
                    );
                });
                return this;
            }
        });

        TeamCountryLanguageView = Backbone.View.extend({
            template: _.template(
                '<p class="meta-detail project-relation"><span class="icon fa-list"></span> TODO - Figure Me Out </p>' +
                '<% if (country) { print(\'<p class="meta-detail team-location"><span class="icon fa-globe"></span><%= country %></p>\'); } %>' +
                '<% if (language) { print(\'<p class="meta-detail team-language"><span class="icon fa-chat"></span><%= language %></p>\'); } %>'
            ),

            render: function() {
                // this.$el should be the card meta div
                this.$el.append(this.template({
                    country: this.model.get('country'),
                    language: this.model.get('langauge')
                }));
            }
        });

        TeamCardView = CardView.extend({
            initialize: function () {
                CardView.prototype.initialize.apply(this, arguments);
                // TODO: show last ac tivity detail view
                this.detailViews = [
                    new TeamMembershipView({model: this.model}),
                    new TeamCountryLanguageView({model: this.model})
                ];
            },

            configuration: 'list_card',
            cardClass: 'team-card',
            title: function () { return this.model.get('name'); },
            description: function () { return this.model.get('description'); },
            details: function () { return this.detailViews; },
            actionClass: 'action-view',
            actionContent: ''
        });
        return TeamCardView;
    });
}).call(this, define || RequireJS.define);
