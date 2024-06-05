document.addEventListener('DOMContentLoaded', function() {
    const subcatSelect = document.querySelector('select[name="subcat"]');
    const brandSelect = document.querySelector('select[name="brand"]');
    const productSelect = document.querySelector('select[name="product"]');

    function filterOptions(){
        const selectedSubcat = subcatSelect.value;

        for (let i = 0; i < brandSelect.options.length; i++) {
            const option = brandSelect.options[i];
            option.style.display = option.getAttribute('data-subcat') === selectedSubcat ? 'block' : 'none';
        }

        for(let i = 0; i < productSelect.options.length; i++) {
            const option = productSelect.options[i];
            option.style.display = option.getAttribute('data-subcat') === selectedSubcat ? 'block' : 'none';
        }
    }

    if (subcatSelect) {
        subcatSelect.addEventListener('change', filterOptions);
    }

    filterOptions();
})