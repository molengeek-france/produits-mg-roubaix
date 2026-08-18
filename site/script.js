document.documentElement.classList.add("js");

const menuButton = document.querySelector("[data-menu-toggle]");
const navigation = document.querySelector("[data-navigation]");

if (menuButton && navigation) {
  menuButton.hidden = false;

  const closeMenu = () => {
    navigation.dataset.open = "false";
    menuButton.setAttribute("aria-expanded", "false");
    menuButton.textContent = "Menu";
  };

  menuButton.addEventListener("click", () => {
    const willOpen = navigation.dataset.open !== "true";
    navigation.dataset.open = String(willOpen);
    menuButton.setAttribute("aria-expanded", String(willOpen));
    menuButton.textContent = willOpen ? "Fermer" : "Menu";
  });

  navigation.addEventListener("click", (event) => {
    if (event.target.closest("a")) closeMenu();
  });

  window.addEventListener("resize", () => {
    if (window.innerWidth > 920) closeMenu();
  });
}
