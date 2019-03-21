var checkExist = setInterval(function() {
  pol_list = document.getElementById('politician-list');
  if (pol_list) {
    pol_list.onmouseout = function() {
        highlightAllTrace();
    };
    var pol_items = pol_list.getElementsByTagName("a");
    for (i = 0; i < pol_items.length; i++) {
      pol_items[i].number = i;
      pol_items[i].onmouseover = function() {
        lowlightAllTrace();
        highlightTrace(this.number)
      };
    }
  clearInterval(checkExist);
  }
}, 100); // check every 100ms

function highlightTrace(trace_id) {
  Plotly.restyle('politician-mention-graph', {opacity: 1}, trace_id);
}

function lowlightAllTrace() {
  Plotly.restyle('politician-mention-graph', {opacity: 0.4});
}

function highlightAllTrace() {
  Plotly.restyle('politician-mention-graph', {opacity: 1});
}