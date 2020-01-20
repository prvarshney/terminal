let verticalNavOpeningToggler = document.getElementById('vertical-navbar-opening-toggler');
let verticalNavbar = document.getElementsByClassName('vertical-navbar')[0];
let verticalNavBarClosingToggler = document.getElementById('vertical-navbar-closing-toggler');

verticalNavOpeningToggler.addEventListener('click', () => {
    verticalNavbar.style.left = 0;
});

verticalNavBarClosingToggler.addEventListener('click', () => {
    verticalNavbar.style.left = '-300px';
});