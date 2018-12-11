// prints out dataframe onto html page
function buildTable(tableData) {
    var tbody = d3.select("tbody");
  
    // First, clear out any existing data
    tbody.html("");
  
    // Next, loop through each object in the data
    // and append a row and cells for each value in the row
    tableData.forEach((dataRow) => {
      // Append a row to the table body
      var row = tbody.append("tr");
      row.append('td').text(dataRow['Brewery']);
      row.append('td').text(dataRow['Style']);
      row.append('td').text(dataRow['Name']);
      row.append('td').text(dataRow['ABV'] + ' %');
      row.append('td').text(dataRow['Score']);
  
    });
  }
  
  // ==============================
  // filter for unique items for corresponding item
  // ==============================
  
  function onlyUnique(value, index, self) {
      return self.indexOf(value) === index;
  }
  
  function unique_brewery_list(df){
    var brewery_list = [];
    df.forEach(row => brewery_list.push(row.Brewery));
    var unique_breweries = brewery_list.filter(onlyUnique)
    unique_breweries.sort();
    unique_breweries.unshift("All");
    return unique_breweries;
  }
  
  
  function unique_style_list(df){
    var style_list = [];
    df.forEach(row => style_list.push(row.Style));
    var unique_style = style_list.filter(onlyUnique);
    unique_style.sort();
    unique_style.unshift("All");
    return unique_style;
  }
  
  function unique_score_list(df){
    var score_list = [];
    df.forEach(row => score_list.push(Math.round(row.Score)));
    var unique_score = score_list.filter(onlyUnique);
    unique_score.sort();
    unique_score.unshift("All");
    return unique_score;
  }
  
  function unique_ABV_list(df){
    var abv_list = [];
    df.forEach(row => abv_list.push(Math.round(row.ABV)));
    var abv_score = abv_list.filter(onlyUnique);
    abv_score.sort();
    abv_score.unshift("All");
    return abv_score;
  }
  // ==============================
  // grab unique items and populate corresponding list
  // ==============================
  
  // populate actual dropdown filter
  function list_populator(list, d3_select){
  var options = d3.select(d3_select)
  options.html('');
  options
    .selectAll('option')
    .data(list).enter()
    .append('option')
      .text(function (d) { return d });
  }
  
  
  function all_list_populator(dataframe){
    // populate corresponding list
  
    list_populator(unique_brewery_list(dataframe), '#Brewery-Value');
    list_populator(unique_style_list(dataframe), '#Style-Value');
    list_populator(unique_score_list(dataframe), '#Score-Value');
    list_populator(unique_ABV_list(dataframe), '#ABV-Value');
  
  
  }
  
  
  // ==============================
  // filters data based on user selections
  // ==============================
  
  
  function style_filter(records) {
    var style_value = d3.select('#Style-Value').property('value');
  
    if (style_value != 'All') {
      return records.filter(row => row.Style == style_value);
    } else {
      return records.filter(row => row.Style);
    }
  
  }
  
  function brewery_filter(records) {
    var brewery_value = d3.select('#Brewery-Value').property('value');
  
    if (brewery_value != 'All') {
      return records.filter(row => row.Brewery == brewery_value);
    } else {
      return records.filter(row => row.Brewery);
    }
  
  }
  
  // CONTINUE HERE
  function abv_filter(records) {
    var abv_value = d3.select('#ABV-Value').property('value');
  
      if (abv_value != 'All') {
        return records.filter(row => {
          if (Math.floor(row.ABV) == abv_value){
            return row.ABV;
          }})
      } else {
        return records.filter(row => row.ABV);
      }
  }
  
  function score_filter(records) {
    var score_value = d3.select('#Score-Value').property('value');
  
      if (score_value != 'All') {
        return records.filter(row => {
          if (Math.floor(row.Score) == score_value){
            return row.Score;
          }})
      } else {
        return records.filter(row => row.Score);
      }
  }
  