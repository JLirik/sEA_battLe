$(document).ready(function() {
            $('.button').click(function() {
                $(this).toggleClass('clicked');
            });

            $('#save').click(function() {
                var data = '';
                $('.button').each(function() {
                    if ($(this).hasClass('clicked')) {
                        data += 'k';
                    } else {
                        data += '-';
                    }
                });
                $('input[name=data]').val(data.trim());
            });
        });