class BookReader extends HTMLElement {
  connectedCallback() {
    setTimeout(() => {
      const contents = this.querySelector("#book-contents");
      console.log(contents);

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
