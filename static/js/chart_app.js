d3.json("/table_data").then(function(data) {
    var tableData = data;
  
    // POST HTML
    d3.select('#filter-button').on('click', function() {
    d3.event.preventDefault();
  
    // filters df by selected city value
  
    var brewery_records = brewery_filter(tableData);
    var style_records = style_filter(brewery_records);
    var score_records = score_filter(style_records);
    var abv_records = abv_filter(score_records);
    var filtered_records = abv_records;
  
  
    buildTable(filtered_records);
    all_list_populator(filtered_records);
  
    })
  
    // print whole DF
    d3.select('#show-all').on('click', function() {
      d3.event.preventDefault();
  
      buildTable(tableData);
      all_list_populator(tableData);
  
    })
  
  });
  