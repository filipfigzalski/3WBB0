function fetchNewData() {
    // we gotta put here to code that fetches new data from the microcontroller but this is just an example
    newStepsPerHour = 600;
    newPowerGenerated = "1200 W";

    console.log(chart.data.datasets[0].data)
    fetch('http://localhost:8000/tiles/1/dataframes/', {
      method: 'GET',
      headers: {
      },
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json(); // Parse the response body as JSON
      })
      .then(data => {
        // Handle the JSON data returned from the API
        console.log(data);
        // document.getElementById("steps").textContent = data["steps"]
        // document.getElementById("power").textContent = data["power_generated"]

        chart.data.datasets[0].data.length = 0;
        chart.data.datasets[1].data.length = 0;

        var voltage;
        var steps;
        for(const element of data) {
            const stepsObj = { t: element["timestamp"], y: element["steps"] }
            const voltageObj = { t: element["timestamp"], y: element["voltage"] }
            chart.data.datasets[0].data.push(stepsObj)
            chart.data.datasets[1].data.push(voltageObj)
            steps = element["steps"];
            voltage = element["voltage"];
        }

        console.log(chart.data.datasets[0].data)
        // chart.data.datasets[0].data.push(parsedData)
        chart.update()
        document.getElementById("steps").textContent = steps*6*60;
        document.getElementById("voltage").textContent = Math.round(voltage*100)/100;
        
      })
      .catch(error => {
        // Handle any errors that occurred during the fetch
        console.error('There was a problem with the fetch operation:', error);
      });
  }

var t=setInterval(fetchNewData,1000);