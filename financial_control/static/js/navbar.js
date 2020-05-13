class NavBar extends HTMLElement {
  connectedCallback() {
    const home_url = this.getAttribute("home-url");
    const car_list_url = this.getAttribute("car-list-url");
    this.innerHTML = `<nav class="navbar navbar-expand-lg navbar-light bg-light">
      <a class="navbar-brand" href="${home_url ? home_url : "#"}">Car Finder</a>
      <button
        class="navbar-toggler"
        type="button"
        data-toggle="collapse"
        data-target="#conteudoNavbarSuportado"
        aria-controls="conteudoNavbarSuportado"
        aria-expanded="false"
        aria-label="Alterna navegação"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="conteudoNavbarSuportado">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item active">
            <a class="nav-link" href="${car_list_url ? car_list_url : "#"}"
              >Cars<span class="sr-only"></span
            ></a>
          </li>
        </ul>
      </div>
    </nav>
  `;
  }
}

customElements.define("nav-bar", NavBar);
