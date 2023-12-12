var ax = document.querySelectorAll('.cfc-external-link-content');
var s = ``;
for (let i = 0; i < ax.length; i++) {
    s += `"${ax[i].children[0].innerHTML}", `;
}