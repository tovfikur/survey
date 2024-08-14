document.addEventListener('DOMContentLoaded', function () {
    const nextBtn = document.querySelector('.u-btn-step-next');
    const prevBtn = document.querySelector('.u-btn-step-prev');
    const submitBtn = document.querySelector('.u-btn-submit');
    const form = document.querySelector('form.u-inner-form');
    const formSteps = document.querySelectorAll('.u-carousel-item');
    
    let currentStep = 0;

    function showStep(index) {
        formSteps.forEach((step, idx) => {
            step.classList.toggle('u-active', idx === index);
        });
        
        prevBtn.classList.toggle('u-hidden', currentStep === 0);
        nextBtn.classList.toggle('u-hidden', currentStep === formSteps.length - 1);
        submitBtn.classList.toggle('u-hidden', currentStep !== formSteps.length - 1);
    }

    nextBtn.addEventListener('click', function (event) {
        event.preventDefault();
        if (currentStep < formSteps.length - 1) {
            currentStep++;
            showStep(currentStep);
        }
    });

    prevBtn.addEventListener('click', function (event) {
        event.preventDefault();
        if (currentStep > 0) {
            currentStep--;
            showStep(currentStep);
        }
    });

    submitBtn.addEventListener('click', function (event) {
        event.preventDefault();
        const formData = new FormData(form);
        
        fetch(form.action, {
            method: form.method,
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                window.location.href = '/success';  // Redirect to the success page
            } else {
                alert('Submission failed: ' + (data.message || 'Unknown error.'));
            }
        })
        .catch(error => {
            alert('An error occurred: ' + error.message);
        });
    });

    showStep(currentStep);
});
