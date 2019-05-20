setInterval(function() {
  party_list = document.getElementById('party-list');
  politician_list = document.getElementById('politician-list');
  theme_list = document.getElementById('theme-list');

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
  }

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
  }

  if (theme_list) {
    theme_list.onmouseout = function() {
        highlightAllTrace('theme-mention-graph');
    };
    var theme_items = theme_list.getElementsByTagName("span");
    for (i = 0; i < theme_items.length; i++) {
      theme_items[i].number = i;
      theme_items[i].onmouseover = function() {
        lowlightAllTrace('theme-mention-graph');
        highlightTrace('theme-mention-graph', this.number)
      };
    }
  }

}, 100); // check every 100ms

setInterval(function() {
  modebarButtons = document.getElementsByClassName("modebar-btn");

  if (modebarButtons.length > 0) {
    for (i = 0; i < modebarButtons.length; i++) {
      modebarButtons[i].attributes["data-title"].value="Download deze afbeelding";
    }
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