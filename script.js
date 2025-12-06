const panes = document.querySelectorAll('.pane');
const reportbuttons = document.querySelectorAll('.reportbutton');
const reports = document.querySelectorAll('.report');

panes.forEach(pane => {
  pane.addEventListener('click', () => {
    panes.forEach(p => {
      p.classList.remove('expanded');
      p.querySelectorAll('*:not(.hidden-exempt)').forEach(child => {
        child.classList.add('hidden');
      });
    });

    pane.classList.add('expanded');
    pane.querySelectorAll('*:not(.hidden-exempt):not(.report)').forEach(child => {
      child.classList.remove('hidden');
    });
  });
});

reportbuttons.forEach(reportbutton => {
  reportbutton.addEventListener('click', (e) => {
    e.stopPropagation();  // Prevent triggering the pane click handler
    console.log('Report button clicked');
    const pane = reportbutton.closest('.pane');
    const report = pane.querySelector('.report');
    if (report) {
      report.classList.remove('hidden');
      report.querySelectorAll('*').forEach(child => {
        child.classList.remove('hidden');
      });
    }
  });
});

