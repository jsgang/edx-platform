/**
 * Model for a team.
 */
(function (define) {
    'use strict';
    define(['backbone'], function (Backbone) {
        var Team = Backbone.Model.extend({
            defaults: {
                id: '',
                name: '',
                is_active: null,
                course_id: '',
                topic_id: '',
                date_created: '',
                description: '',
                country: '',
                language: '',
                membership: []
            }
        });
        return Team;
    });
}).call(this, define || RequireJS.define);
