      google.charts.load('current', {
        'packages':['geochart'],
        // Note: you will need to get a mapsApiKey for your project.
        // See: https://developers.google.com/chart/interactive/docs/basic_load_libs#load-settings
        'mapsApiKey': 'AIzaSyD-9tSrke72PouQMnMX-a7eZSW0jkFMBWY'
      });
      google.charts.setOnLoadCallback(drawRegionsMap);

      function drawRegionsMap() {
        var data = google.visualization.arrayToDataTable([
['State', 'contaminant level'],
          ['US-510', 1],
          ['US-515', 2],
          ['US-535', 3],
          ['US-516', 4],
          ['US-542', 5],
          ['US-547', 4],
          ['US-554', 5],
          ['US-558', 2],
          ['US-596', 4],
        ]);

        var options = {
          region: 'US', // Africa
          colorAxis: {colors: ['#00853f', 'black', '#e31b23']},
          backgroundColor: '#81d4fa',
          datalessRegionColor: '#f8bbd0',
          defaultColor: '#f5f5f5',
          displayMode: 'regions',
          resolution: 'metros',
        };

        var chart = new google.visualization.GeoChart(document.getElementById('geochart-colors'));
        chart.draw(data, options);
      };