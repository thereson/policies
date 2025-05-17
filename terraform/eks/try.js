jQuery(document).ready(function ($) {
    const cooldownTime = 60 * 60 * 1000; // 1 hour
    const cooldownKey = 'demoButtonLastClick';
    let loadingInterval;

    function updateStatus(message, color) {
        let $status = $('#processingStatus');
        if ($status.length === 0) {
            $status = $('<p id="processingStatus" style="margin-top: 10px;"></p>');
            $('#demoButton').after($status);
        }
        $status.text(message).css('color', color);

        if (loadingInterval) clearInterval(loadingInterval);

        const loadingChars = ['|', '/', '-', '\\'];
        let i = 0;
        loadingInterval = setInterval(() => {
            $status.text(message + ' ' + loadingChars[i]);
            i = (i + 1) % loadingChars.length;
        }, 250);
    }

    function stopLoading() {
        if (loadingInterval) clearInterval(loadingInterval);
    }

    function updateCooldownMessage() {
        const lastClickTime = localStorage.getItem(cooldownKey);
        const now = Date.now();

        if (lastClickTime && now - lastClickTime < cooldownTime) {
            const timeLeft = cooldownTime - (now - lastClickTime);
            const hours = Math.floor(timeLeft / 3600000);
            const mins = Math.floor((timeLeft % 3600000) / 60000);
            const secs = Math.floor((timeLeft % 60000) / 1000);

            updateStatus(`Try again in ${hours}:${mins < 10 ? '0' : ''}${mins}:${secs < 10 ? '0' : ''}${secs}`, 'orange');

            if (timeLeft > 1000) {
                setTimeout(updateCooldownMessage, 1000);
            } else {
                $('#processingStatus').remove();
                $('#demoButton').show();
            }
        }
    }

    function checkCooldown() {
        const lastClickTime = localStorage.getItem(cooldownKey);
        const now = Date.now();

        if (lastClickTime && now - lastClickTime < cooldownTime) {
            $('#demoButton').hide();
            updateCooldownMessage();
        }
    }

    $('#demoButton').click(function (e) {
        e.preventDefault();

        const now = Date.now();
        const lastClickTime = localStorage.getItem(cooldownKey);
        if (lastClickTime && now - lastClickTime < cooldownTime) return;

        $(this).hide();
        updateStatus('Processing...', '#007bff');

        const requestData = {
            action: 'create_account',
            nonce: ajax_object.nonce,
            helm_chart: 'wikijs:0.0.1-build15',
            mode: 'demo'
        };

        $.post(ajax_object.ajax_url, requestData, function (response) {
            if (!response.success) {
                updateStatus('An error occurred during account creation.', 'red');
                $('#demoButton').show();
                stopLoading();
                return;
            }

            const status = response.data.status;

            if (status === 'ACTIVE') {
                updateStatus('Deployment successful! Your account is ready. Details sent via email.', 'green');
            } else if (status === 'DEPLOYING') {
                updateStatus('Deployment in progress. Please wait and check your email shortly.', 'blue');
            } else if (status === 'FAILED') {
                updateStatus(`Deployment failed: ${response.data.deployment_message}`, 'red');
            } else {
                updateStatus('Unknown status received. Please contact support.', 'orange');
            }

            localStorage.setItem(cooldownKey, Date.now());
            stopLoading();
        }).fail(function (error) {
            console.error('AJAX error:', error);
            updateStatus('Server error. Please try again.', 'red');
            $('#demoButton').show();
            stopLoading();
        });
    });

    checkCooldown(); // Initial cooldown check on page load
});