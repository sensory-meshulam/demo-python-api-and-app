// You can get data from the URL and use it

const urlParams = new URLSearchParams(window.location.search);
console.log(urlParams);
const confirmationNumber = urlParams.get('confirmation_number');
document.getElementById("confirmationNumber").textContent = 'confirmationNumber: ' + confirmationNumber ;