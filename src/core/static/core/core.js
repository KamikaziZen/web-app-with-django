$(document).ready(
    function() {


        $('.autoload').each(function () {
            $(this).load($(this).attr('data-url'));
        });

        $('.CommentsSection').each(function () {
            $(this).load($(this).attr('data-url'));
        });

        $('.LeaveCommentForm').each(function() {
            $(this).load($(this).attr('data-url'));
        })

        $(document).on('submit', '.LeaveCommentForm', function() {
            $.post(
                $(this).data('url'),
                $(this).serialize()
            ).done( function() {
                $('.CommentsSection').load($('.CommentsSection').attr('data-url'));
                $('.LeaveCommentForm').load($('.LeaveCommentForm').attr('data-url'));
            });
            return false;
        });

        $(document).on('submit', '.PostScoreForm', function() {
            $.post(
                $(this).data('url'),
                $(this).serialize()
            ).done( function() {
                $('.ScoreSection').each (function () {
                    $(this).load($(this).attr('data-url'));
                })
            });
            return false;
        });

        $('.CreatePostForm').each(function () {
            $(this).load($(this).attr('data-url'));
        });

        $(document).on('submit', '.CreateSubredditForm', function() {
            $.post(
                $(this).data('url'),
                $(this).serialize()
            ).done( function() {
                 $('.modal').modal('toggle');
                 $('.SubredditsListSection').load($('.SubredditsListSection').attr('data-url'));
                 $('.CreateSubredditForm').load($('.CreateSubredditForm').attr('data-url'));
            });
            return false;
        });


    })