var x = document.querySelectorAll('.copy-notice');
var allIP = [];
for (let i = 0; i < x.length; i++) {
    var y = x[i].parentElement.innerText;
    allIP.push(y.replace('\nCopy', ''));
}

console.log(allIP);