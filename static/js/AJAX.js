$(document).ready(function () {
    $('.table-responsive').on('click', '.delete-btn', function () {
        let id = $(this).data('id');
        let url = 'delete/' + id;
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'csrfmiddlewaretoken': csrftoken,
            },
            success: function (data) {
                $('.table-responsive').html($(data).find('.table-responsive').html());
                $('.pagination').html($(data).find('.pagination').html());
            },
            error: function (xhr, status, error) {

                console.error(error);
            }
        });
    });
});