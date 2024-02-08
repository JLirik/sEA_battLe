//$(document).ready(function() {
//            $('.button').click(function() {
//                $(this).toggleClass('clicked');
//            });
//
//            $('#save').click(function() {
//                var data = '';
//                $('.button').each(function() {
//                    if ($(this).hasClass('clicked')) {
//                        data += 'k';
//                    } else {
//                        data += '-';
//                    }
//                });
//                $('input[name=data]').val(data.trim());
//            });
//        });


document.querySelector('.saver').onclick = Field_reader;

function Field_reader() {
    var data = '';

    $('.total').find('.input-text').each(function() {
        let qq = ($(this).val());
        if (qq == '') {
            qq = '-'
        }
        data += qq
    });

    $('input[name=data]').val(data.trim());
}
