var checkExist = setInterval(function() {
  party_list = document.getElementById('party-list');
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
  if (party_list) {
    party_list.onmouseout = function() {
        highlightAllTrace('party-mention-graph');
    };
    var party_items = party_list.getElementsByTagName("a");
    for (i = 0; i < party_items.length; i++) {
      party_items[i].number = i;
      party_items[i].onmouseover = function() {
        lowlightAllTrace('party-mention-graph');
        highlightTrace('party-mention-graph', this.number)
      };
    }
  clearInterval(checkExist);
  }
}, 100); // check every 100ms

var checkModeBar = setInterval(function() {
  modebarButtons = document.getElementsByClassName("modebar-btn");

  if (modebarButtons.length > 0) {
    for (i = 0; i < modebarButtons.length; i++) {
      modebarButtons[i].attributes["data-title"].value="Download deze afbeelding";
    }
    clearInterval(checkModeBar);
  }
}, 100);

function highlightTrace(graph_id, trace_id) {
  Plotly.restyle(graph_id, {opacity: 1}, trace_id);
}

function lowlightAllTrace(graph_id) {
  Plotly.restyle(graph_id, {opacity: 0.4});
}

function highlightAllTrace(graph_id) {
  Plotly.restyle(graph_id, {opacity: 1});
}