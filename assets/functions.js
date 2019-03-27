var checkExist = setInterval(function() {
  parties_list = document.getElementById('parties-list');
  politician_list = document.getElementById('politician-list');

  if (politician_list) {
    politician_list.onmouseout = function() {
        highlightAllTrace('politician-mention-graph');
    };
    var politician_items = politician_list.getElementsByTagName("a");
    for (i = 0; i < politician_items.length; i++) {
      politician_items[i].number = i;
      politician_items[i].onmouseover = function() {
        lowlightAllTrace('politician-mention-graph');
        highlightTrace('politician-mention-graph', this.number)
      };
    }
  clearInterval(checkExist);
  }
  if (parties_list) {
    parties_list.onmouseout = function() {
        highlightAllTrace('parties-mention-graph');
    };
    var parties_items = parties_list.getElementsByTagName("a");
    for (i = 0; i < parties_items.length; i++) {
      parties_items[i].number = i;
      parties_items[i].onmouseover = function() {
        lowlightAllTrace('parties-mention-graph');
        highlightTrace('parties-mention-graph', this.number)
      };
    }
  clearInterval(checkExist);
  }
}, 100); // check every 100ms

function highlightTrace(graph_id, trace_id) {
  Plotly.restyle(graph_id, {opacity: 1}, trace_id);
}

function lowlightAllTrace(graph_id) {
  Plotly.restyle(graph_id, {opacity: 0.4});
}

function highlightAllTrace(graph_id) {
  Plotly.restyle(graph_id, {opacity: 1});
}