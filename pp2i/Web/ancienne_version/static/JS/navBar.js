const burgerToggler = document.querySelector(".burger")
const navLinksContainer = document.querySelector(".navlinks-container");

const toggleNav = () => {
  burgerToggler.classList.toggle("open")

  const ariaToggle = burgerToggler.getAttribute("aria-expanded") === "true" ?  "false" : "true";
  burgerToggler.setAttribute("aria-expanded", ariaToggle)

  navLinksContainer.classList.toggle("open")
}
burgerToggler.addEventListener("click", toggleNav)

new ResizeObserver(entries => {
  if(entries[0].contentRect.width <= 900){
    navLinksContainer.style.transition = "transform 0.3s ease-out"
  } else {
    navLinksContainer.style.transition = "none"
  }
}).observe(document.body)

