// Handler that uses various data-* attributes to trigger
// specific actions, mimicing bootstraps attributes
const triggers = Array.from(document.querySelectorAll('[data-trigger="switch"]'));

window.addEventListener('click', (ev) => {
  const el = ev.target;
  if (triggers.includes(el)) {
    const elements = el.getElementsByClassName("switch");
    switchVisibility(elements, 'toggle');
  } else if (triggers.includes(el.parentElement)){
    const elements = el.parentElement.getElementsByClassName("switch");
    switchVisibility(elements, 'toggle');
  }
}, false);


const fnmap = {
  'toggle': 'toggle',
  'show': 'add',
  'hide': 'remove'
};
const switchVisibility = (selectors, cmd) => {
    for (var i = 0; i < selectors.length; i++) {
        selectors[i].classList[fnmap[cmd]]('show');
    }
}