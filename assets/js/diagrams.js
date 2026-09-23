(() => {
  async function initialize() {
    if (!window.mermaid) return;
    document.querySelectorAll('.post-content code.language-mermaid').forEach(code => {
      const diagram = document.createElement('div');
      diagram.className = 'mermaid';
      diagram.textContent = code.textContent;
      code.parentElement.replaceWith(diagram);
    });

    const diagrams = document.querySelectorAll('.post-content .mermaid');
    if (!diagrams.length) return;
    mermaid.initialize({ startOnLoad: false });

    const dialog = document.createElement('dialog');
    dialog.className = 'diagram-dialog';
    dialog.setAttribute('aria-labelledby', 'diagram-dialog-title');
    dialog.setAttribute('aria-describedby', 'diagram-dialog-help');
    dialog.innerHTML = `
      <div class="diagram-toolbar">
        <h2 id="diagram-dialog-title">Diagram</h2>
        <div class="diagram-controls">
          <button type="button" data-zoom="out" aria-label="Zoom out">−</button>
          <output class="diagram-scale" aria-live="polite">125%</output>
          <button type="button" data-zoom="in" aria-label="Zoom in">+</button>
          <button type="button" class="diagram-close" autofocus>Close</button>
        </div>
      </div>
      <p id="diagram-dialog-help">Scroll or swipe to explore. Use + or − to zoom. Escape closes this view.</p>
      <div class="diagram-viewport" tabindex="0" role="region" aria-label="Enlarged diagram; scroll to explore"></div>`;
    document.body.append(dialog);

    const viewport = dialog.querySelector('.diagram-viewport');
    const close = dialog.querySelector('.diagram-close');
    const zoomOut = dialog.querySelector('[data-zoom="out"]');
    const zoomIn = dialog.querySelector('[data-zoom="in"]');
    let current = null;
    let scale = 1.25;

    function resize() {
      if (!current) return;
      current.svg.style.width = `${current.width * scale}px`;
      current.svg.style.height = `${current.height * scale}px`;
      current.svg.style.maxWidth = 'none';
      dialog.querySelector('output').value = `${Math.round(scale * 100)}%`;
      zoomOut.disabled = scale <= 0.5;
      zoomIn.disabled = scale >= 3;
    }

    function open(diagram, svg, trigger, number) {
      if (dialog.open) return;
      const box = svg.viewBox.baseVal;
      const rect = svg.getBoundingClientRect();
      current = {
        svg, diagram, trigger, next: svg.nextSibling,
        style: svg.getAttribute('style'),
        width: box.width || rect.width,
        height: box.height || rect.height,
        overflow: document.body.style.overflow,
      };
      // Move the original SVG so Mermaid IDs, markers, and scoped styles stay valid.
      viewport.append(svg);
      scale = 1.25;
      resize();
      dialog.querySelector('h2').textContent = `Diagram ${number}`;
      document.body.style.overflow = 'hidden';
      dialog.showModal();
      viewport.scrollTo(0, 0);
      close.focus();
    }

    close.addEventListener('click', closeDialog);
    let backdropPress = false;
    dialog.addEventListener('pointerdown', event => { backdropPress = event.target === dialog; });
    dialog.addEventListener('click', event => {
      if (backdropPress && event.target === dialog) closeDialog();
      backdropPress = false;
    });
    // Native dialog supplies focus containment and an inert page. Restore the
    // SVG synchronously so rapid close/reopen cannot race a queued close event.
    dialog.addEventListener('cancel', event => {
      event.preventDefault();
      closeDialog();
    });
    function closeDialog() {
      if (!current) return;
      const { svg, diagram, next, style, trigger, overflow } = current;
      dialog.close();
      diagram.insertBefore(svg, next);
      if (style === null) svg.removeAttribute('style');
      else svg.setAttribute('style', style);
      document.body.style.overflow = overflow;
      current = null;
      trigger.focus({ preventScroll: true });
    }
    zoomOut.addEventListener('click', () => { scale = Math.max(0.5, scale - 0.25); resize(); });
    zoomIn.addEventListener('click', () => { scale = Math.min(3, scale + 0.25); resize(); });

    for (const [index, diagram] of [...diagrams].entries()) {
      try {
        await mermaid.run({ nodes: [diagram] });
      } catch (error) {
        console.error('Could not render Mermaid diagram', error);
        continue;
      }
      const svg = diagram.querySelector('svg');
      if (!svg || typeof dialog.showModal !== 'function') continue;
      const trigger = document.createElement('button');
      trigger.type = 'button';
      trigger.className = 'diagram-zoom-trigger';
      trigger.textContent = 'Enlarge diagram';
      trigger.setAttribute('aria-label', `Enlarge diagram ${index + 1}`);
      trigger.setAttribute('aria-haspopup', 'dialog');
      diagram.after(trigger);
      diagram.classList.add('diagram-zoomable');
      trigger.addEventListener('click', () => open(diagram, svg, trigger, index + 1));
      diagram.addEventListener('click', event => {
        if (!event.target.closest('a')) open(diagram, svg, trigger, index + 1);
      });
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initialize);
  else initialize();
})();
