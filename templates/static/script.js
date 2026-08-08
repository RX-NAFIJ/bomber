$(document).ready(() => {
    $(document).on('click', '#send', function (e) {
        e.preventDefault();
        $('#logs').addClass('visually-hidden');
        var amount = $("#amount").val();
        var mobile = $("#mobile").val().replace(/^0/, "");
        if (amount > 0 && mobile.length == 10) {
            $('#logs').removeClass('visually-hidden');
            $('#logs').text("⏳ Processing...");

            fetch("/api/attack", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ phone: mobile, amount: parseInt(amount) || 1 })
            })
            .then(r => r.json())
            .then(data => {
                if (data.error) {
                    $('#logs').text("❌ " + data.error);
                    return;
                }
                $('#logs').text("✅ " + data.success + " SMS sent to " + mobile);
                console.log(data);
            })
            .catch(error => {
                $('#logs').text("❌ Connection error!");
                console.error('Error', error);
            });

        } else {
            $('#logs').removeClass('visually-hidden');
            $('#logs').text("Invalid Number or Amount is null");
        }
    });
});