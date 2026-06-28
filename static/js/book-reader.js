class BookReader extends HTMLElement {
  connectedCallback() {
    // timeout is used to ensure component has had a chance to parse the nested
    // content before setting up the observer
    setTimeout(() => {
      const contents = this.querySelector("#book-contents");

      const bookContentObserver = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
          contents.scrollTop = contents.scrollHeight;
        });
      });

      bookContentObserver.observe(contents, {
        childList: true,
        subtree: true,
      });
    });
  }
}

customElements.define("book-reader", BookReader);
